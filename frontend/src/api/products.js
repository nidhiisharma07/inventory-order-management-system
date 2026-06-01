import { apiClient } from "./client";

export const productsApi = {
  list: () => apiClient.get("/api/v1/products"),
  getById: (id) => apiClient.get(`/api/v1/products/${id}`),
  create: (payload) => apiClient.post("/api/v1/products", payload),
  update: (id, payload) => apiClient.put(`/api/v1/products/${id}`, payload),
  remove: (id) => apiClient.delete(`/api/v1/products/${id}`),
};
