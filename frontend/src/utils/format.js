export function formatCurrency(value) {
  const amount = Number(value);
  if (Number.isNaN(amount)) return "$0.00";
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(amount);
}

export const LOW_STOCK_THRESHOLD = 10;

export function isLowStock(quantity) {
  return quantity <= LOW_STOCK_THRESHOLD;
}
