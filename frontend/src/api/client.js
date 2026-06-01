import axios from "axios";
import { clearToken, getToken } from "../utils/authStorage";

const API_URL = import.meta.env.VITE_API_URL;
const REQUEST_TIMEOUT_MS = Number(import.meta.env.VITE_API_TIMEOUT_MS || 15000);
const MAX_RETRIES = Number(import.meta.env.VITE_API_MAX_RETRIES || 2);

function extractErrorMessage(error) {
  const detail = error.response?.data?.detail;
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) {
    return detail.map((item) => item.msg || JSON.stringify(item)).join(", ");
  }
  return error.message || "An unexpected error occurred";
}

function isRetryable(error) {
  if (!error.response) return true;
  const status = error.response.status;
  return status >= 500 || status === 429;
}

function wait(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export const apiClient = axios.create({
  baseURL: API_URL,
  timeout: REQUEST_TIMEOUT_MS,
  headers: {
    "Content-Type": "application/json",
  },
});

apiClient.interceptors.request.use((config) => {
  const token = getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const config = error.config;
    config.__retryCount = config.__retryCount || 0;

    if (config.__retryCount < MAX_RETRIES && isRetryable(error)) {
      config.__retryCount += 1;
      await wait(300 * config.__retryCount);
      return apiClient(config);
    }

    if (error.response?.status === 401) {
      const isAuthRoute = config?.url?.includes("/auth/login")
        || config?.url?.includes("/auth/register");

      if (!isAuthRoute) {
        clearToken();
        const onLoginPage = window.location.pathname.startsWith("/login")
          || window.location.pathname.startsWith("/register");
        if (!onLoginPage) {
          window.location.href = "/login";
        }
      }
    }

    return Promise.reject(new Error(extractErrorMessage(error)));
  },
);
