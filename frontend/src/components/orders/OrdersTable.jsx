import Button from "../ui/Button";
import { formatCurrency } from "../../utils/format";

export default function OrdersTable({ orders, onView }) {
  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-slate-200 text-sm">
        <thead className="bg-slate-50">
          <tr>
            <th className="px-4 py-3 text-left font-medium text-slate-600">Order</th>
            <th className="px-4 py-3 text-left font-medium text-slate-600">Customer</th>
            <th className="px-4 py-3 text-left font-medium text-slate-600">Status</th>
            <th className="px-4 py-3 text-left font-medium text-slate-600">Items</th>
            <th className="px-4 py-3 text-left font-medium text-slate-600">Total</th>
            <th className="px-4 py-3 text-right font-medium text-slate-600">Actions</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100">
          {orders.map((order) => (
            <tr key={order.id} className="hover:bg-slate-50">
              <td className="px-4 py-3 font-medium">#{order.id}</td>
              <td className="px-4 py-3">{order.customer_name}</td>
              <td className="px-4 py-3">
                <span
                  className={`rounded-full px-2.5 py-0.5 text-xs font-medium ${
                    order.status === "active"
                      ? "bg-emerald-100 text-emerald-800"
                      : "bg-slate-200 text-slate-700"
                  }`}
                >
                  {order.status}
                </span>
              </td>
              <td className="px-4 py-3">{order.item_count}</td>
              <td className="px-4 py-3">{formatCurrency(order.total_amount)}</td>
              <td className="px-4 py-3 text-right">
                <Button variant="secondary" onClick={() => onView(order.id)}>
                  View
                </Button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
