import { useCallback, useEffect, useState } from "react";
import toast from "react-hot-toast";
import { customersApi } from "../api/customers";
import CustomerForm from "../components/customers/CustomerForm";
import EmptyState from "../components/ui/EmptyState";
import LoadingSpinner from "../components/ui/LoadingSpinner";
import Button from "../components/ui/Button";
import { useAuth } from "../context/AuthContext";

export default function CustomersPage() {
  const { isAdmin } = useAuth();
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [deletingId, setDeletingId] = useState(null);

  const fetchCustomers = useCallback(async () => {
    setLoading(true);
    try {
      const { data } = await customersApi.list();
      setCustomers(data.items);
    } catch (error) {
      toast.error(error.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchCustomers();
  }, [fetchCustomers]);

  const handleCreate = async (payload) => {
    setIsSubmitting(true);
    try {
      await customersApi.create(payload);
      toast.success("Customer created");
      await fetchCustomers();
    } catch (error) {
      toast.error(error.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDelete = async (customer) => {
    if (!window.confirm(`Delete ${customer.full_name}?`)) return;
    setDeletingId(customer.id);
    try {
      await customersApi.remove(customer.id);
      toast.success("Customer deleted");
      await fetchCustomers();
    } catch (error) {
      toast.error(error.message);
    } finally {
      setDeletingId(null);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Customers</h1>
        <p className="mt-1 text-sm text-slate-500">
          Customers are required before placing orders.
        </p>
      </div>

      <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="mb-4 text-lg font-semibold text-slate-900">New Customer</h2>
        <CustomerForm onSubmit={handleCreate} isSubmitting={isSubmitting} />
      </div>

      {loading ? (
        <LoadingSpinner label="Loading customers..." />
      ) : customers.length === 0 ? (
        <EmptyState
          title="No customers yet"
          description="Add a customer to start creating orders."
        />
      ) : (
        <div className="overflow-x-auto rounded-xl border border-slate-200 bg-white shadow-sm">
          <table className="min-w-full divide-y divide-slate-200 text-sm">
            <thead className="bg-slate-50">
              <tr>
                <th className="px-4 py-3 text-left font-medium text-slate-600">Name</th>
                <th className="px-4 py-3 text-left font-medium text-slate-600">Email</th>
                <th className="px-4 py-3 text-left font-medium text-slate-600">Phone</th>
                <th className="px-4 py-3 text-right font-medium text-slate-600">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {customers.map((customer) => (
                <tr key={customer.id} className="hover:bg-slate-50">
                  <td className="px-4 py-3 font-medium">{customer.full_name}</td>
                  <td className="px-4 py-3 text-slate-600">{customer.email}</td>
                  <td className="px-4 py-3 text-slate-600">{customer.phone || "—"}</td>
                  <td className="px-4 py-3 text-right">
                    {isAdmin ? (
                      <Button
                        variant="danger"
                        onClick={() => handleDelete(customer)}
                        disabled={deletingId === customer.id}
                      >
                        {deletingId === customer.id ? "Deleting..." : "Delete"}
                      </Button>
                    ) : (
                      <span className="text-xs text-slate-400">—</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
