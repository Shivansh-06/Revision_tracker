const BASE_URL = "http://localhost:8000";

// Create a timeout promise
function timeoutPromise(ms) {
  return new Promise((_, reject) => {
    setTimeout(() => reject(new Error("Request timeout")), ms);
  });
}

export async function apiFetch(
  endpoint,
  { method = "GET", token, body } = {}
) {
  try {
    // Add timeout to prevent hanging (10 seconds)
    const fetchPromise = fetch(`${BASE_URL}${endpoint}`, {
      method,
      headers: {
        "Content-Type": "application/json",
        ...(token && { Authorization: `Bearer ${token}` }),
      },
      ...(body && { body: JSON.stringify(body) }),
    });

    const res = await Promise.race([
      fetchPromise,
      timeoutPromise(10000) // 10 second timeout
    ]);

    if (!res.ok) {
      let errorData;
      try {
        errorData = await res.json();
      } catch {
        const text = await res.text();
        errorData = { detail: text || `HTTP ${res.status}: ${res.statusText}` };
      }
      return errorData; // Return error object instead of throwing
    }

    return res.json();
  } catch (error) {
    console.error("API fetch error:", error);
    // Return error object with detail
    if (error.message === "Request timeout") {
      return { detail: "Request timed out. Please check if the backend server is running." };
    }
    if (error.message.includes("Failed to fetch") || error.message.includes("NetworkError")) {
      return { detail: `Cannot connect to server. Please ensure the backend is running on ${BASE_URL}` };
    }
    return { detail: error.message || "Network error. Please try again." };
  }
}
