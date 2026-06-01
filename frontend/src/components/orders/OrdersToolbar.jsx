import SearchInput from "../ui/SearchInput";

const SORT_OPTIONS = [
  { value: "newest", label: "Newest first" },
  { value: "oldest", label: "Oldest first" },
  { value: "highest_total", label: "Highest total" },
  { value: "lowest_total", label: "Lowest total" },
];

export default function OrdersToolbar({
  search,
  onSearchChange,
  sort,
  onSortChange,
}) {
  return (
    <div className="flex flex-col gap-3 rounded-xl border border-slate-200 bg-white p-4 shadow-sm sm:flex-row sm:items-center">
      <SearchInput
        value={search}
        onChange={onSearchChange}
        placeholder="Search by customer, email, or order #"
        className="flex-1"
      />
      <label className="flex shrink-0 flex-col gap-1 text-sm text-slate-600 sm:w-52">
        Sort by
        <select
          value={sort}
          onChange={(e) => onSortChange(e.target.value)}
          className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 focus:ring-2 focus:ring-brand-200"
        >
          {SORT_OPTIONS.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      </label>
    </div>
  );
}
