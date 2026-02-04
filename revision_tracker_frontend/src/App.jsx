import { useState, useEffect } from "react";
import Login from "./auth/Login";
import Register from "./auth/Register";
import Syllabus from "./pages/Syllabus";
import Topics from "./pages/Topics";
import RevisionQueue from "./pages/RevisionQueue";
import Navbar from "./components/Navbar";
import { getToken, logout } from "./api/auth";


function App() {
  const [token, setToken] = useState(null);
  const [page, setPage] = useState("queue");
  const [authMode, setAuthMode] = useState("login");
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    try {
      const storedToken = getToken();
      if (storedToken) {
        setToken(storedToken);
      }
    } catch (error) {
      console.error("Error getting token:", error);
      setError("Failed to load app");
    } finally {
      setIsLoading(false);
    }
  }, []);

  if (error) {
    return (
      <div style={{ minHeight: "100vh", backgroundColor: "white", display: "flex", alignItems: "center", justifyContent: "center", flexDirection: "column", padding: "20px" }}>
        <h1 style={{ color: "black", marginBottom: "10px" }}>Error</h1>
        <p style={{ color: "black" }}>{error}</p>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div style={{ minHeight: "100vh", backgroundColor: "white", display: "flex", alignItems: "center", justifyContent: "center" }}>
        <div style={{ color: "black", fontSize: "18px" }}>Loading...</div>
      </div>
    );
  }

  if (!token) {
    if (authMode === "register") {
      return <Register onSwitchToLogin={() => setAuthMode("login")} />;
    }
    return <Login onLogin={setToken} onSwitchToRegister={() => setAuthMode("register")} />;
  }

  function handleLogout() {
    logout();
    setToken(null);
    setAuthMode("login");
  }

  let content = null;

  try {
    if (page === "queue") content = <RevisionQueue />;
    else if (page === "topics") content = <Topics />;
    else if (page === "syllabus") content = <Syllabus />;
  } catch (error) {
    console.error("Error rendering content:", error);
    return (
      <div style={{ minHeight: "100vh", backgroundColor: "white", padding: "20px", color: "black" }}>
        <h1>Error rendering page</h1>
        <p>{error.message}</p>
      </div>
    );
  }

  // Safety check - if we somehow get here without content, show an error
  if (!content) {
    return (
      <div style={{ minHeight: "100vh", backgroundColor: "white", padding: "20px", color: "black" }}>
        <h1>Error: No content to display</h1>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white">
      <Navbar
        currentPage={page}
        setPage={setPage}
        onLogout={handleLogout}
      />
      <div className="container mx-auto px-4 py-6">
        {content}
      </div>
    </div>
  );
}

export default App;
