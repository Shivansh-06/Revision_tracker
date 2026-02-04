import React from "react";

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error("Error caught by boundary:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{ 
          minHeight: "100vh", 
          backgroundColor: "white", 
          display: "flex", 
          alignItems: "center", 
          justifyContent: "center", 
          flexDirection: "column", 
          padding: "20px" 
        }}>
          <h1 style={{ color: "black", marginBottom: "10px" }}>Something went wrong</h1>
          <p style={{ color: "black", marginBottom: "10px" }}>
            {this.state.error?.message || "An error occurred"}
          </p>
          <button
            onClick={() => {
              this.setState({ hasError: false, error: null });
              window.location.reload();
            }}
            style={{
              padding: "10px 20px",
              border: "2px solid black",
              backgroundColor: "white",
              color: "black",
              cursor: "pointer",
              borderRadius: "8px"
            }}
          >
            Reload Page
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
