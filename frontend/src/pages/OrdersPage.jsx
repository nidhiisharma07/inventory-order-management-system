import { useCallback, useEffect, useState } from "react";
import toast from "react-hot-toast";
import { customersApi } from "../api/customers";
import { ORDER_SORT_OPTIONS, ordersApi } from "../api/orders";
import { productsApi } from "../api/products";
import OrderDetailModal from "../components/orders/OrderDetailModal";
import OrderForm from "../components/orders/OrderForm";
import OrdersTable from "../components/orders/OrdersTable";
import OrdersToolbar from "../components/orders/OrdersToolbar";
import Button from "../components/ui/Button";
import EmptyState from "../components/ui/EmptyState";
import LoadingSpinner from "../components/ui/LoadingSpinner";
import Pagination from "../components/ui/Pagination";
import { useAuth } from "../context/AuthContext";
import { useDebounce } from "../hooks/useDebounce";
import { formatCurrency } from "../utils/format";

const DEFAULT_LIMIT = 10;

export default function OrdersPage() {
  const { isAdmin } = useAuth();
  const [orders, setOrders] = useState([]);
  const [customers, setCustomers] = useState([]);
  const [products, setProducts] = useState([]);
  const [catalogLoading, setCatalogLoading] = useState(true);

  const [page, setPage] = useState(1);
  const [limit, setLimit] = useState(DEFAULT_LIMIT);
  const [search, setSearch] = useState("");
  const [sort, setSort] = useState(ORDER_SORT_OPTIONS.NEWEST);
  const debouncedSearch = useDebounce(search, 400);

  const [total, setTotal] = useState(0);
  const [ordersLoading, setOrdersLoading] = useState(true);

  const [showForm, setShowForm] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isCancelling, setIsCancelling] = useState(false);
  const [selectedOrder, setSelectedOrder] = useState(null);
  const [loadingDetail, setLoadingDetail] = useState(false);

  useEffect(() => {
    const loadCatalog = async () => {
      setCatalogLoading(true);
      try {
        const [customersRes, productsRes] = await Promise.all([
          customersApi.list(),
          productsApi.list(),
        ]);
        setCustomers(customersRes.data.items);
        setProducts(productsRes.data.items);
      } catch (error) {
        toast.error(error.message);
      } finally {
        setCatalogLoading(false);
      }
    };
    loadCatalog();
  }, []);

  const fetchOrders = useCallback(async () => {
    setOrdersLoading(true);
    try {
      const { data } = await ordersApi.list({
        page,
        limit,
        search: debouncedSearch || undefined,
        sort,
      });
      setOrders(data.data);
      setTotal(data.total);
    } catch (error) {
      toast.error(error.message);
    } finally {
      setOrdersLoading(false);
    }
  }, [page, limit, debouncedSearch, sort]);

  useEffect(() => {
    fetchOrders();
  }, [fetchOrders]);

  useEffect(() => {
    setPage(1);
  }, [debouncedSearch, sort, limit]);

  const handleCreateOrder = async (payload) => {
    setIsSubmitting(true);
    try {
      const { data } = await ordersApi.create(payload);
      toast.success(`Order #${data.id} placed — total ${formatCurrency(data.total_amount)}`);
      setShowForm(false);
      setPage(1);
      await fetchOrders();
      setSelectedOrder(data);
    } catch (error) {
      toast.error(error.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleViewOrder = async (orderId) => {
    setLoadingDetail(true);
    try {
      const { data } = await ordersApi.getById(orderId);
      setSelectedOrder(data);
    } catch (error) {
      toast.error(error.message);
    } finally {
      setLoadingDetail(false);
    }
  };

  const handleCancelOrder = async (order) => {
    if (!window.confirm(`Cancel order #${order.id} and restore stock?`)) return;
    setIsCancelling(true);
    try {
      const { data } = await ordersApi.cancel(order.id);
      toast.success("Order cancelled — inventory restored");
      setSelectedOrder(data);
      await fetchOrders();
    } catch (error) {
      toast.error(error.message);
    } finally {
      setIsCancelling(false);
    }
  };

  const hasFilters = Boolean(debouncedSearch);
  const isInitialEmpty = !ordersLoading && total === 0 && !hasFilters;

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Orders</h1>
          <p className="mt-1 text-sm text-slate-500">
            Search, sort, and browse orders with server-side pagination.
          </p>
        </div>
        <Button onClick={() => setShowForm((prev) => !prev)} disabled={catalogLoading}>
          {showForm ? "Hide Form" : "New Order"}
        </Button>
      </div>

      {showForm && !catalogLoading && (
        <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="mb-4 text-lg font-semibold text-slate-900">Create Order</h2>
          <OrderForm
            customers={customers}
            products={products}
            onSubmit={handleCreateOrder}
            onCancel={() => setShowForm(false)}
            isSubmitting={isSubmitting}
          />
        </div>
      )}

      {loadingDetail && <LoadingSpinner label="Loading order details..." />}

      {selectedOrder && !loadingDetail && (
        <OrderDetailModal
          order={selectedOrder}
          onClose={() => setSelectedOrder(null)}
          onCancel={handleCancelOrder}
          isCancelling={isCancelling}
          canCancel={isAdmin}
        />
      )}

      <OrdersToolbar
        search={search}
        onSearchChange={setSearch}
        sort={sort}
        onSortChange={setSort}
      />

      <div className="rounded-xl border border-slate-200 bg-white shadow-sm">
        {ordersLoading ? (
          <LoadingSpinner label="Loading orders..." />
        ) : isInitialEmpty ? (
          <div className="p-6">
            <EmptyState
              title="No orders yet"
              description="Create a customer and products, then place your first order."
            />
          </div>
        ) : orders.length === 0 ? (
          <div className="p-6">
            <EmptyState
              title="No matching orders"
              description="Try a different search term or clear filters."
            />
          </div>
        ) : (
          <>
            <OrdersTable orders={orders} onView={handleViewOrder} />
            <Pagination
              page={page}
              limit={limit}
              total={total}
              onPageChange={setPage}
              onLimitChange={setLimit}
            />
          </>
        )}
      </div>
    </div>
  );
}
