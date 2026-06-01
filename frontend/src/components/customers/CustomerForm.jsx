import { useState } from "react";
import Button from "../ui/Button";

const initialForm = { full_name: "", email: "", phone: "" };

function validateForm(form) {
  const errors = {};
  if (!form.full_name.trim()) errors.full_name = "Name is required";
  if (!form.email.trim()) errors.email = "Email is required";
  else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
    errors.email = "Enter a valid email";
  }
  return errors;
}

export default function CustomerForm({ onSubmit, isSubmitting }) {
  const [form, setForm] = useState(initialForm);
  const [errors, setErrors] = useState({});

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
      full_name: form.full_name.trim(),
      email: form.email.trim(),
      phone: form.phone.trim() || null,
    });
    setForm(initialForm);
  };

  const fieldClass = (field) =>
    `w-full rounded-lg border px-3 py-2 text-sm outline-none focus:ring-2 ${
      errors[field]
        ? "border-red-300 focus:ring-red-200"
        : "border-slate-300 focus:ring-brand-200"
    }`;

  return (
    <form onSubmit={handleSubmit} className="grid gap-4 sm:grid-cols-2">
      <div className="sm:col-span-2">
        <label className="mb-1 block text-sm font-medium text-slate-700">Full name</label>
        <input
          name="full_name"
          value={form.full_name}
          onChange={handleChange}
          className={fieldClass("full_name")}
          placeholder="Customer name"
        />
        {errors.full_name && (
          <p className="mt-1 text-xs text-red-600">{errors.full_name}</p>
        )}
      </div>
      <div>
        <label className="mb-1 block text-sm font-medium text-slate-700">Email</label>
        <input
          name="email"
          type="email"
          value={form.email}
          onChange={handleChange}
          className={fieldClass("email")}
          placeholder="email@company.com"
        />
        {errors.email && <p className="mt-1 text-xs text-red-600">{errors.email}</p>}
      </div>
      <div>
        <label className="mb-1 block text-sm font-medium text-slate-700">Phone</label>
        <input
          name="phone"
          value={form.phone}
          onChange={handleChange}
          className={fieldClass("phone")}
          placeholder="Optional"
        />
      </div>
      <div className="sm:col-span-2 flex justify-end">
        <Button type="submit" disabled={isSubmitting}>
          {isSubmitting ? "Saving..." : "Add Customer"}
        </Button>
      </div>
    </form>
  );
}
