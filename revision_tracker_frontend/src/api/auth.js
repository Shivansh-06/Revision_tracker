
import { apiFetch } from "./client";
export function getToken() {
  return localStorage.getItem("token");
}

export function setToken(token) {
  localStorage.setItem("token", token);
}

export function clearToken() {
  localStorage.removeItem("token");
}

export function logout() {
  clearToken();
}
/* ===============================
   AUTH
================================ */

export function login(email, password) {
  return apiFetch("/auth/login", {
    method: "POST",
    body: { email, password },
  });
}

export function register(email, password) {
  return apiFetch("/auth/register", {
    method: "POST",
    body: { email, password },
  });
}
