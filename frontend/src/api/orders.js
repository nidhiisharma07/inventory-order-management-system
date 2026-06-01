import { apiClient } from "./client";

export const ordersApi = {
  list: (params = {}) => apiClient.get("/api/v1/orders", { params }),
  getById: (id) => apiClient.get(`/api/v1/orders/${id}`),
  create: (payload) => apiClient.post("/api/v1/orders", payload),
  cancel: (id) => apiClient.delete(`/api/v1/orders/${id}`),
};

export const ORDER_SORT_OPTIONS = {
  NEWEST: "newest",
  OLDEST: "oldest",
  HIGHEST_TOTAL: "highest_total",
  LOWEST_TOTAL: "lowest_total",
};
