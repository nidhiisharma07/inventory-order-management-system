import { useEffect, useState } from "react";
import Button from "../ui/Button";

const initialForm = {
  name: "",
  sku: "",
  price: "",
  stock_quantity: "0",
};

function validateForm(form) {
  const errors = {};
  if (!form.name.trim()) errors.name = "Name is required";
  if (!form.sku.trim()) errors.sku = "SKU is required";
  if (!form.price || Number(form.price) <= 0) errors.price = "Price must be greater than 0";
  if (form.stock_quantity === "" || Number(form.stock_quantity) < 0) {
    errors.stock_quantity = "Stock cannot be negative";
  }
  return errors;
}

export default function ProductForm({ product, onSubmit, onCancel, isSubmitting }) {
  const [form, setForm] = useState(initialForm);
  const [errors, setErrors] = useState({});

  useEffect(() => {
    if (product) {
      setForm({
        name: product.name,
        sku: product.sku,
        price: String(product.price),
        stock_quantity: String(product.stock_quantity),
      });
    } else {
      setForm(initialForm);
    }
    setErrors({});
  }, [product]);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((prev) => ({ ...prev, [name]: value }));
    setErrors((prev) => ({ ...prev, [name]: undefined }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    const validationErrors = validateForm(form);
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    onSubmit({
      name: form.name.trim(),
      sku: form.sku.trim(),
      price: Number(form.price),
      stock_quantity: Number(form.stock_quantity),
    });
  };

  const fieldClass = (field) =>
    `w-full rounded-lg border px-3 py-2 text-sm outline-none focus:ring-2 ${
      errors[field]
        ? "border-red-300 focus:ring-red-200"
        : "border-slate-300 focus:ring-brand-200"
    }`;

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="mb-1 block text-sm font-medium text-slate-700">Name</label>
        <input
          name="name"
          value={form.name}
          onChange={handleChange}
          className={fieldClass("name")}
          placeholder="Product name"
        />
        {errors.name && <p className="mt-1 text-xs text-red-600">{errors.name}</p>}
      </div>

      <div>
        <label className="mb-1 block text-sm font-medium text-slate-700">SKU</label>
        <input
          name="sku"
          value={form.sku}
          onChange={handleChange}
          className={fieldClass("sku")}
          placeholder="SKU-001"
        />
        {errors.sku && <p className="mt-1 text-xs text-red-600">{errors.sku}</p>}
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        <div>
          <label className="mb-1 block text-sm font-medium text-slate-700">Price</label>
          <input
            name="price"
            type="number"
            min="0"
            step="0.01"
            value={form.price}
            onChange={handleChange}
            className={fieldClass("price")}
            placeholder="0.00"
          />
          {errors.price && <p className="mt-1 text-xs text-red-600">{errors.price}</p>}
        </div>

        <div>
          <label className="mb-1 block text-sm font-medium text-slate-700">Stock</label>
          <input
            name="stock_quantity"
            type="number"
            min="0"
            value={form.stock_quantity}
            onChange={handleChange}
            className={fieldClass("stock_quantity")}
          />
          {errors.stock_quantity && (
            <p className="mt-1 text-xs text-red-600">{errors.stock_quantity}</p>
          )}
        </div>
      </div>

      <div className="flex flex-wrap justify-end gap-2 pt-2">
        {onCancel && (
          <Button type="button" variant="secondary" onClick={onCancel}>
            Cancel
          </Button>
        )}
        <Button type="submit" disabled={isSubmitting}>
          {isSubmitting ? "Saving..." : product ? "Update Product" : "Create Product"}
        </Button>
      </div>
    </form>
  );
}
