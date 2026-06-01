import { useCallback, useEffect, useState } from "react";
import toast from "react-hot-toast";
import { productsApi } from "../api/products";
import ProductForm from "../components/products/ProductForm";
import ProductTable from "../components/products/ProductTable";
import EmptyState from "../components/ui/EmptyState";
import LoadingSpinner from "../components/ui/LoadingSpinner";
import Button from "../components/ui/Button";
import { useAuth } from "../context/AuthContext";

export default function ProductsPage() {
  const { isAdmin } = useAuth();
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isDeletingId, setIsDeletingId] = useState(null);
  const [editingProduct, setEditingProduct] = useState(null);
  const [showForm, setShowForm] = useState(false);

  const fetchProducts = useCallback(async () => {
    setLoading(true);
    try {
      const { data } = await productsApi.list();
      setProducts(data.items);
    } catch (error) {
      toast.error(error.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchProducts();
  }, [fetchProducts]);

  const handleCreateOrUpdate = async (payload) => {
    setIsSubmitting(true);
    try {
      if (editingProduct) {
        await productsApi.update(editingProduct.id, payload);
        toast.success("Product updated successfully");
      } else {
        await productsApi.create(payload);
        toast.success("Product created successfully");
      }
      setEditingProduct(null);
      setShowForm(false);
      await fetchProducts();
    } catch (error) {
      toast.error(error.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDelete = async (product) => {
    if (!window.confirm(`Delete "${product.name}"?`)) return;

    setIsDeletingId(product.id);
    try {
      await productsApi.remove(product.id);
      toast.success("Product deleted");
      await fetchProducts();
    } catch (error) {
      toast.error(error.message);
    } finally {
      setIsDeletingId(null);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Products</h1>
          <p className="mt-1 text-sm text-slate-500">
            Manage catalog items, pricing, and inventory levels.
          </p>
        </div>
        {isAdmin && (
          <Button
            onClick={() => {
              setEditingProduct(null);
              setShowForm((prev) => !prev);
            }}
          >
            {showForm && !editingProduct ? "Hide Form" : "Add Product"}
          </Button>
        )}
      </div>

      {!isAdmin && (
        <p className="rounded-lg bg-slate-100 px-4 py-2 text-sm text-slate-600">
          Staff can view and update products. Only admins can create new products.
        </p>
      )}

      {((showForm && isAdmin) || editingProduct) && (
        <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="mb-4 text-lg font-semibold text-slate-900">
            {editingProduct ? "Edit Product" : "New Product"}
          </h2>
          <ProductForm
            product={editingProduct}
            onSubmit={handleCreateOrUpdate}
            onCancel={() => {
              setEditingProduct(null);
              setShowForm(false);
            }}
            isSubmitting={isSubmitting}
          />
        </div>
      )}

      {loading ? (
        <LoadingSpinner label="Loading products..." />
      ) : products.length === 0 ? (
        <EmptyState
          title="No products yet"
          description="Create your first product to start tracking inventory."
        />
      ) : (
        <ProductTable
          products={products}
          onEdit={(product) => {
            setEditingProduct(product);
            setShowForm(true);
          }}
          onDelete={handleDelete}
          isDeletingId={isDeletingId}
        />
      )}
    </div>
  );
}
