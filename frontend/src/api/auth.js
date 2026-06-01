import { apiClient } from "./client";

export const authApi = {
  register: (payload) => apiClient.post("/api/v1/auth/register", payload),
  login: (payload) => apiClient.post("/api/v1/auth/login", payload),
  me: () => apiClient.get("/api/v1/auth/me"),
};
