import { useEffect, useState } from "react";

/**
 * Delays updating a value until the user stops typing.
 * WHY: Prevents firing an API request on every keystroke.
 */
export function useDebounce(value, delayMs = 400) {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delayMs);
    return () => clearTimeout(timer);
  }, [value, delayMs]);

  return debouncedValue;
}
