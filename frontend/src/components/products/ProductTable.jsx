import Button from "../ui/Button";
import { formatCurrency, isLowStock } from "../../utils/format";

export default function ProductTable({ products, onEdit, onDelete, isDeletingId }) {
  return (
    <div className="overflow-x-auto rounded-xl border border-slate-200 bg-white shadow-sm">
      <table className="min-w-full divide-y divide-slate-200 text-sm">
        <thead className="bg-slate-50">
          <tr>
            <th className="px-4 py-3 text-left font-medium text-slate-600">Name</th>
            <th className="px-4 py-3 text-left font-medium text-slate-600">SKU</th>
            <th className="px-4 py-3 text-left font-medium text-slate-600">Price</th>
            <th className="px-4 py-3 text-left font-medium text-slate-600">Stock</th>
            <th className="px-4 py-3 text-right font-medium text-slate-600">Actions</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100">
          {products.map((product) => (
            <tr key={product.id} className="hover:bg-slate-50">
              <td className="px-4 py-3 font-medium text-slate-900">{product.name}</td>
              <td className="px-4 py-3 text-slate-600">{product.sku}</td>
              <td className="px-4 py-3">{formatCurrency(product.price)}</td>
              <td className="px-4 py-3">
                <span
                  className={`inline-flex rounded-full px-2.5 py-0.5 text-xs font-medium ${
                    isLowStock(product.stock_quantity)
                      ? "bg-amber-100 text-amber-800"
                      : "bg-emerald-100 text-emerald-800"
                  }`}
                >
                  {product.stock_quantity}
                  {isLowStock(product.stock_quantity) ? " · Low" : ""}
                </span>
              </td>
              <td className="px-4 py-3">
                <div className="flex justify-end gap-2">
                  <Button variant="secondary" onClick={() => onEdit(product)}>
                    Edit
                  </Button>
                  <Button
                    variant="danger"
                    onClick={() => onDelete(product)}
                    disabled={isDeletingId === product.id}
                  >
                    {isDeletingId === product.id ? "Deleting..." : "Delete"}
                  </Button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
