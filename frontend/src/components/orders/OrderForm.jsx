import { useState } from "react";
import Button from "../ui/Button";
import { formatCurrency } from "../../utils/format";

const emptyLine = { product_id: "", quantity: "1" };

export default function OrderForm({
  customers,
  products,
  onSubmit,
  onCancel,
  isSubmitting,
}) {
  const [customerId, setCustomerId] = useState("");
  const [lines, setLines] = useState([{ ...emptyLine }]);
  const [errors, setErrors] = useState({});

  const availableProducts = products.filter((p) => p.stock_quantity > 0);

  const estimatedTotal = lines.reduce((sum, line) => {
    const product = products.find((p) => String(p.id) === String(line.product_id));
    const qty = Number(line.quantity);
    if (!product || !qty || qty <= 0) return sum;
    return sum + Number(product.price) * qty;
  }, 0);

  const updateLine = (index, field, value) => {
    setLines((prev) =>
      prev.map((line, i) => (i === index ? { ...line, [field]: value } : line)),
    );
    setErrors((prev) => ({ ...prev, lines: undefined }));
  };

  const addLine = () => setLines((prev) => [...prev, { ...emptyLine }]);

  const removeLine = (index) => {
    if (lines.length === 1) return;
    setLines((prev) => prev.filter((_, i) => i !== index));
  };

  const validate = () => {
    const nextErrors = {};
    if (!customerId) nextErrors.customer = "Select a customer";

    const validLines = lines.filter((line) => line.product_id && Number(line.quantity) > 0);
    if (validLines.length === 0) {
      nextErrors.lines = "Add at least one product line";
    }

    const selectedProductIds = [];

    lines.forEach((line, index) => {
      if (!line.product_id && !line.quantity) return;
      const product = products.find((p) => String(p.id) === String(line.product_id));
      const qty = Number(line.quantity);
      if (!product) {
        nextErrors[`line_${index}`] = "Select a valid product";
        return;
      }
      if (selectedProductIds.includes(line.product_id)) {
        nextErrors[`line_${index}`] = "Duplicate product — use one line per product";
        return;
      }
      selectedProductIds.push(line.product_id);
      if (!qty || qty <= 0) {
        nextErrors[`line_${index}`] = "Quantity must be greater than 0";
        return;
      }
      if (qty > product.stock_quantity) {
        nextErrors[`line_${index}`] =
          `Only ${product.stock_quantity} units available for ${product.sku}`;
      }
    });

    setErrors(nextErrors);
    return Object.keys(nextErrors).length === 0;
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!validate()) return;

    const items = lines
      .filter((line) => line.product_id && Number(line.quantity) > 0)
      .map((line) => ({
        product_id: Number(line.product_id),
        quantity: Number(line.quantity),
      }));

    onSubmit({
      customer_id: Number(customerId),
      items,
    });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="mb-1 block text-sm font-medium text-slate-700">Customer</label>
        <select
          value={customerId}
          onChange={(e) => {
            setCustomerId(e.target.value);
            setErrors((prev) => ({ ...prev, customer: undefined }));
          }}
          className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:ring-2 focus:ring-brand-200"
        >
          <option value="">Select customer</option>
          {customers.map((customer) => (
            <option key={customer.id} value={customer.id}>
              {customer.full_name} ({customer.email})
            </option>
          ))}
        </select>
        {errors.customer && <p className="mt-1 text-xs text-red-600">{errors.customer}</p>}
        {customers.length === 0 && (
          <p className="mt-1 text-xs text-amber-600">Create a customer first.</p>
        )}
      </div>

      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-medium text-slate-700">Line items</h3>
          <Button type="button" variant="secondary" onClick={addLine}>
            Add line
          </Button>
        </div>

        {lines.map((line, index) => (
          <div
            key={index}
            className="grid gap-3 rounded-lg border border-slate-200 p-3 sm:grid-cols-[1fr_120px_auto]"
          >
            <select
              value={line.product_id}
              onChange={(e) => updateLine(index, "product_id", e.target.value)}
              className="rounded-lg border border-slate-300 px-3 py-2 text-sm"
            >
              <option value="">Select product</option>
              {availableProducts.map((product) => (
                <option key={product.id} value={product.id}>
                  {product.name} ({product.sku}) — {product.stock_quantity} in stock
                </option>
              ))}
            </select>
            <input
              type="number"
              min="1"
              value={line.quantity}
              onChange={(e) => updateLine(index, "quantity", e.target.value)}
              className="rounded-lg border border-slate-300 px-3 py-2 text-sm"
              placeholder="Qty"
            />
            <Button type="button" variant="secondary" onClick={() => removeLine(index)}>
              Remove
            </Button>
            {errors[`line_${index}`] && (
              <p className="text-xs text-red-600 sm:col-span-3">{errors[`line_${index}`]}</p>
            )}
          </div>
        ))}
        {errors.lines && <p className="text-xs text-red-600">{errors.lines}</p>}
      </div>

      <div className="rounded-lg bg-slate-50 px-4 py-3 text-sm">
        <span className="text-slate-500">Estimated total (server recalculates): </span>
        <span className="font-semibold text-slate-900">{formatCurrency(estimatedTotal)}</span>
      </div>

      <div className="flex justify-end gap-2">
        {onCancel && (
          <Button type="button" variant="secondary" onClick={onCancel}>
            Cancel
          </Button>
        )}
        <Button type="submit" disabled={isSubmitting || customers.length === 0}>
          {isSubmitting ? "Placing order..." : "Place Order"}
        </Button>
      </div>
    </form>
  );
}
