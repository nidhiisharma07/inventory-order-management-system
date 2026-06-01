import { apiClient } from "./client";

export const customersApi = {
  list: () => apiClient.get("/api/v1/customers"),
  getById: (id) => apiClient.get(`/api/v1/customers/${id}`),
  create: (payload) => apiClient.post("/api/v1/customers", payload),
  remove: (id) => apiClient.delete(`/api/v1/customers/${id}`),
};
