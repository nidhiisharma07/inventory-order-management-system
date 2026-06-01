import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import ProductForm from "../components/products/ProductForm";

describe("ProductForm", () => {
  it("shows validation errors for empty submission", () => {
    render(<ProductForm onSubmit={vi.fn()} />);

    fireEvent.click(screen.getByRole("button", { name: /create product/i }));

    expect(screen.getByText("Name is required")).toBeInTheDocument();
    expect(screen.getByText("SKU is required")).toBeInTheDocument();
  });

  it("submits valid product data", () => {
    const onSubmit = vi.fn();
    render(<ProductForm onSubmit={onSubmit} />);

    fireEvent.change(screen.getByPlaceholderText("Product name"), {
      target: { value: "USB Cable" },
    });
    fireEvent.change(screen.getByPlaceholderText("SKU-001"), {
      target: { value: "usb-01" },
    });
    fireEvent.change(screen.getByPlaceholderText("0.00"), {
      target: { value: "12.5" },
    });
    fireEvent.change(screen.getByDisplayValue("0"), {
      target: { value: "25" },
    });

    fireEvent.click(screen.getByRole("button", { name: /create product/i }));

    expect(onSubmit).toHaveBeenCalledWith({
      name: "USB Cable",
      sku: "usb-01",
      price: 12.5,
      stock_quantity: 25,
    });
  });
});
