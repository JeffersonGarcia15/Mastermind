const BASE_URL = "http://localhost:5000/api/v2";

async function request(endpoint, options = {}) {
  const headers = options.headers || {};
  headers["Content-Type"] = headers["Content-Type"] || "application/json";
  return fetch(`${BASE_URL}${endpoint}`, {
    ...options,
    headers,
    credentials: "include",
  }).then((res) => res.json());
}

// Auth
export function login(username, password) {
  return request("/auth/login", {
    method: "POST",
    body: JSON.stringify({ username, password }),
  });
}

export function signup(username, password) {
  return request("/auth/signup", {
    method: "POST",
    body: JSON.stringify({ username, password }),
  });
}

export function logout() {
  return request("/auth/logout", {
    method: "POST",
  });
}

export function authenticate() {
  return request("/auth/");
}
