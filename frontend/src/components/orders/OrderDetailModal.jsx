import OrderDetailPanel from "./OrderDetailPanel";

export default function OrderDetailModal({
  order,
  onClose,
  onCancel,
  isCancelling,
  canCancel,
}) {
  if (!order) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 p-4"
      role="dialog"
      aria-modal="true"
      aria-labelledby="order-detail-title"
    >
      <div className="max-h-[90vh] w-full max-w-2xl overflow-y-auto">
        <OrderDetailPanel
          order={order}
          onClose={onClose}
          onCancel={onCancel}
          isCancelling={isCancelling}
          canCancel={canCancel}
        />
      </div>
    </div>
  );
}
