const TOKEN_KEY = "inventory_access_token";

/**
 * sessionStorage clears when the tab closes — slightly safer than localStorage
 * for SPAs without httpOnly cookie support.
 */
export function getToken() {
  return sessionStorage.getItem(TOKEN_KEY);
}

export function setToken(token) {
  sessionStorage.setItem(TOKEN_KEY, token);
}

export function clearToken() {
  sessionStorage.removeItem(TOKEN_KEY);
}
