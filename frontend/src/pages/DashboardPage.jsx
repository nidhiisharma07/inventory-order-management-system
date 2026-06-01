import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import toast from "react-hot-toast";
import { dashboardApi } from "../api/dashboard";
import { productsApi } from "../api/products";
import LoadingSpinner from "../components/ui/LoadingSpinner";
import { formatCurrency, isLowStock, LOW_STOCK_THRESHOLD } from "../utils/format";

export default function DashboardPage() {
  const [stats, setStats] = useState({
    totalProducts: 0,
    lowStockCount: 0,
    totalInventoryValue: 0,
    totalOrders: 0,
    totalRevenue: 0,
  });
  const [recentOrders, setRecentOrders] = useState([]);
  const [lowStockProducts, setLowStockProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadDashboard = async () => {
      try {
        const [productsRes, dashboardRes] = await Promise.all([
          productsApi.list(),
          dashboardApi.getStats(),
        ]);
        const items = productsRes.data.items;
        const dashboard = dashboardRes.data;
        const lowStock = items.filter((p) => isLowStock(p.stock_quantity));
        const inventoryValue = items.reduce(
          (sum, p) => sum + Number(p.price) * p.stock_quantity,
          0,
        );

        setStats({
          totalProducts: items.length,
          lowStockCount: lowStock.length,
          totalInventoryValue: inventoryValue,
          totalOrders: dashboard.total_orders,
          totalRevenue: dashboard.total_revenue,
        });
        setRecentOrders(dashboard.recent_orders);
        setLowStockProducts(lowStock.slice(0, 5));
      } catch (error) {
        toast.error(error.message);
      } finally {
        setLoading(false);
      }
    };

    loadDashboard();
  }, []);

  if (loading) {
    return <LoadingSpinner label="Loading dashboard..." />;
  }

  const cards = [
    { label: "Total Products", value: stats.totalProducts },
    { label: "Total Orders", value: stats.totalOrders },
    { label: "Total Revenue", value: formatCurrency(stats.totalRevenue) },
    {
      label: `Low Stock (≤ ${LOW_STOCK_THRESHOLD})`,
      value: stats.lowStockCount,
      accent: stats.lowStockCount > 0 ? "text-amber-600" : "text-emerald-600",
    },
    {
      label: "Inventory Value",
      value: formatCurrency(stats.totalInventoryValue),
    },
  ];

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Dashboard</h1>
        <p className="mt-1 text-sm text-slate-500">
          Business overview — orders, revenue, inventory health.
        </p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5">
        {cards.map((card) => (
          <div
            key={card.label}
            className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm"
          >
            <p className="text-sm text-slate-500">{card.label}</p>
            <p className={`mt-2 text-2xl font-bold ${card.accent || "text-slate-900"}`}>
              {card.value}
            </p>
          </div>
        ))}
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-lg font-semibold text-slate-900">Recent Orders</h2>
            <Link
              to="/orders"
              className="text-sm font-medium text-brand-600 hover:text-brand-700"
            >
              View all →
            </Link>
          </div>

          {recentOrders.length === 0 ? (
            <p className="text-sm text-slate-500">No orders placed yet.</p>
          ) : (
            <ul className="divide-y divide-slate-100">
              {recentOrders.map((order) => (
                <li
                  key={order.id}
                  className="flex items-center justify-between py-3 text-sm"
                >
                  <div>
                    <p className="font-medium text-slate-900">Order #{order.id}</p>
                    <p className="text-slate-500">{order.customer_name}</p>
                  </div>
                  <div className="text-right">
                    <p className="font-medium">{formatCurrency(order.total_amount)}</p>
                    <p className="text-xs capitalize text-slate-500">{order.status}</p>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>

        <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-lg font-semibold text-slate-900">Low Stock Alerts</h2>
            <Link
              to="/products"
              className="text-sm font-medium text-brand-600 hover:text-brand-700"
            >
              Manage products →
            </Link>
          </div>

          {lowStockProducts.length === 0 ? (
            <p className="text-sm text-slate-500">
              All products are above the low stock threshold.
            </p>
          ) : (
            <ul className="divide-y divide-slate-100">
              {lowStockProducts.map((product) => (
                <li
                  key={product.id}
                  className="flex items-center justify-between py-3 text-sm"
                >
                  <div>
                    <p className="font-medium text-slate-900">{product.name}</p>
                    <p className="text-slate-500">{product.sku}</p>
                  </div>
                  <span className="rounded-full bg-amber-100 px-2.5 py-0.5 text-xs font-medium text-amber-800">
                    {product.stock_quantity} left
                  </span>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}
