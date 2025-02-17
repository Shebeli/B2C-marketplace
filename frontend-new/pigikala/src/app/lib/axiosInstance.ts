import axios from "axios";

const headers: Record<string, string | boolean> = {
  "Content-Type": "application/json",
};
// this axios instance is only used by server actions to work with
// the backend server (Django)
const axiosInstance = axios.create({
  baseURL: process.env.DJANGO_API_BASE_URL,
  headers,
});

// Interceptor in case of 401 errors:

// If the refresh token is valid, do a request to URL path "api/auth/refresh"
// and set a new access token in cookies.

// If the refresh token is invalid (which shouldn't happen since nextjs authentication middleware
// should block it), return a reject promise and attempt to logout the user
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
        // attempt to set a new access token in cookies,
        // and update the header using the response.
        const response = await axios.post("api/auth/refresh");
        const newAccessToken = response.data.access;
        originalRequest.headers["Authorization"] = `Bearer ${newAccessToken}`;
        return axiosInstance(originalRequest);
      } catch (refreshError) {
        console.error(
          "Attempt for getting a new access token has failed:",
          refreshError
        );
        await axios.post("/api/auth/logout");
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

export { axiosInstance };
