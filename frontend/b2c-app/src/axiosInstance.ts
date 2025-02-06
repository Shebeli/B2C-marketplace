import axios from "axios";
import { navigateTo } from "./navigation";

const baseURL = import.meta.env.VITE_API_BASE_URL;

const axiosInstance = axios.create({
  baseURL: baseURL,
  headers: {
    "Content-Type": "application/json",
  },
});

const handleTokenExpiration = () => {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  navigateTo("/login");
};

const setAuthToken = (token: string) => {
  if (token) {
    axiosInstance.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  } else {
    delete axiosInstance.defaults.headers.common["Authorization"];
  }
};

axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (
      error.response &&
      error.response.status == 401 &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true;
      const refreshToken = localStorage.getItem("refresh_token");
      if (!refreshToken) {
        handleTokenExpiration();
        return Promise.reject(error);
      }
      try {
        const { data } = await axiosInstance.post("api/user/token/refresh", {
          refresh: refreshToken,
        });
        const newAccesstoken = data.access;
        localStorage.setItem("access_token", newAccesstoken);
        setAuthToken(newAccesstoken);
        originalRequest.headers["Authorization"] = `Bearer ${newAccesstoken}`;
        return axiosInstance(originalRequest);
      } catch (refreshError) {
        console.error("Token refresh failed:", refreshError);
        handleTokenExpiration();
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

export { axiosInstance, setAuthToken };
