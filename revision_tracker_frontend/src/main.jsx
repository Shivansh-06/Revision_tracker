import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import ErrorBoundary from "./components/ErrorBoundary";
import "./index.css";

try {
  const rootElement = document.getElementById("root");
  if (!rootElement) {
    throw new Error("Root element not found");
  }

  ReactDOM.createRoot(rootElement).render(
    <React.StrictMode>
      <ErrorBoundary>
        <App />
      </ErrorBoundary>
    </React.StrictMode>
  );
} catch (error) {
  console.error("Failed to render app:", error);
  const errorDiv = document.createElement("div");
  errorDiv.style.cssText = "padding: 20px; color: red; background: white; min-height: 100vh;";
  errorDiv.textContent = `Error: ${error.message}`;
  document.body.appendChild(errorDiv);
}
