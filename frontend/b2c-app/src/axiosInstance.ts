import axios from "axios";
import { navigateTo } from "./navigation";
import { API_ROUTES } from "./apiRoutes";

const AUTH = API_ROUTES.AUTH;

const headers: Record<string, string> = {
  "Content-Type": "application/json",
};

const accessToken = localStorage.getItem("accessToken");
if (accessToken) {
  headers["Authorization"] = `Bearer ${localStorage.getItem("accessToken")}`;
}

const axiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers,
});

const handleExpiredRefreshToken = () => {
  localStorage.removeItem("accessToken");
  localStorage.removeItem("refreshToken");
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
      try {
        const { data } = await axiosInstance.post(AUTH.REFRESH_TOKEN, {
          refresh: refreshToken,
        });
        const newAccesstoken = data.access;
        localStorage.setItem("accessToken", newAccesstoken);
        setAuthToken(newAccesstoken);

        // recreate the request object
        originalRequest.headers = {
          ...originalRequest.headers,
          Authorization: `Bearer ${newAccesstoken}`,
        };
        
        return axiosInstance(originalRequest);
      } catch (refreshError) {
        console.error("Token refresh failed:", refreshError);
        handleExpiredRefreshToken();
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

export { axiosInstance, setAuthToken };
