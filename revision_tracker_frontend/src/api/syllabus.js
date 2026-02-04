import { apiFetch } from "./client";

/* ===============================
   SYLLABUS PARSING
================================ */

export function parseSyllabus(token, text, subject = null) {
  return apiFetch("/syllabus/parse", {
    method: "POST",
    token,
    body: { text, subject },
  });
}

/* ===============================
   BULK INSERT TOPICS
================================ */

export function bulkCreateTopics(token, topics) {
  // Backend expects array directly, not wrapped in object
  return apiFetch("/topics/bulk", {
    method: "POST",
    token,
    body: topics, // Send array directly
  });
}
