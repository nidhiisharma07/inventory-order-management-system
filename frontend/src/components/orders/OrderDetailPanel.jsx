import { formatCurrency } from "../../utils/format";
import Button from "../ui/Button";

export default function OrderDetailPanel({
  order,
  onClose,
  onCancel,
  isCancelling,
  canCancel = false,
}) {
  if (!order) return null;

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="mb-4 flex items-start justify-between gap-4">
        <div>
          <h2 id="order-detail-title" className="text-lg font-semibold text-slate-900">
            Order #{order.id}
          </h2>
          <p className="text-sm text-slate-500">
            {order.customer_name} · {order.customer_email}
          </p>
        </div>
        <button
          type="button"
          onClick={onClose}
          className="text-sm text-slate-500 hover:text-slate-800"
        >
          Close
        </button>
      </div>

      <div className="mb-4 flex flex-wrap gap-3 text-sm">
        <span
          className={`rounded-full px-2.5 py-0.5 font-medium ${
            order.status === "active"
              ? "bg-emerald-100 text-emerald-800"
              : "bg-slate-200 text-slate-700"
          }`}
        >
          {order.status}
        </span>
        <span className="font-semibold text-slate-900">
          Total: {formatCurrency(order.total_amount)}
        </span>
      </div>

      <div className="overflow-x-auto">
        <table className="min-w-full text-sm">
          <thead>
            <tr className="border-b border-slate-200 text-left text-slate-500">
              <th className="py-2 pr-4">Product</th>
              <th className="py-2 pr-4">SKU</th>
              <th className="py-2 pr-4">Qty</th>
              <th className="py-2 pr-4">Unit</th>
              <th className="py-2">Line total</th>
            </tr>
          </thead>
          <tbody>
            {order.items.map((item) => (
              <tr key={item.id} className="border-b border-slate-100">
                <td className="py-2 pr-4">{item.product_name}</td>
                <td className="py-2 pr-4 text-slate-600">{item.product_sku}</td>
                <td className="py-2 pr-4">{item.quantity}</td>
                <td className="py-2 pr-4">{formatCurrency(item.unit_price)}</td>
                <td className="py-2">{formatCurrency(item.line_total)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {order.status === "active" && canCancel && (
        <div className="mt-4 flex justify-end">
          <Button variant="danger" onClick={() => onCancel(order)} disabled={isCancelling}>
            {isCancelling ? "Cancelling..." : "Cancel Order"}
          </Button>
        </div>
      )}
    </div>
  );
}
