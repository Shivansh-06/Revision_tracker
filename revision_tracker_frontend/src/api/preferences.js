import { apiFetch } from "./client";

/* ===============================
   PRIORITY MODES
================================ */

export function getPriorityModes(token) {
  return apiFetch("/priority-modes", { token });
}

export function setPriorityMode(token, mode) {
  return apiFetch("/revisions/priority-mode", {
    method: "POST",
    token,
    body: { mode },
  });
}
