import { useState } from "react";
import { login } from "../api/auth";
import { setToken } from "../api/auth";

function Login({ onLogin, onSwitchToRegister }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);

    // Validate password length (bcrypt limit is 72 bytes)
    if (password.length > 72) {
      setError("Password is too long. Maximum length is 72 characters.");
      setLoading(false);
      return;
    }

    try {
      console.log("Attempting login...");
      const data = await login(email, password);
      console.log("Login response:", data);
      
      // Check if response contains an error
      if (data.detail && !data.access_token) {
        setError(data.detail || "Login failed. Please check your credentials.");
        setLoading(false);
        return;
      }
      
      // Check if we got a valid access token
      if (data.access_token) {
        console.log("Login successful, setting token");
        setToken(data.access_token);
        onLogin(data.access_token);
      } else {
        console.error("Login failed: No access token in response", data);
        setError("Login failed. Invalid response from server.");
      }
    } catch (err) {
      console.error("Login error:", err);
      setError(err.message || "Login failed. Please check your connection and try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-white flex items-center justify-center px-4">
      <form 
        onSubmit={handleSubmit}
        className="w-full max-w-md rounded-lg border-2 border-black p-6 bg-white"
      >
        <h2 className="text-2xl font-bold text-black mb-6 text-center">Login</h2>

        {error && (
          <div className="mb-4 p-3 rounded-lg border-2 border-black bg-white text-black text-sm">
            {error}
          </div>
        )}

        <div className="mb-4">
          <input
            type="email"
            className="w-full px-4 py-2 rounded-lg border-2 border-black text-black placeholder-gray-500 bg-white focus:outline-none focus:ring-2 focus:ring-black"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

        <div className="mb-6">
          <input
            type="password"
            className="w-full px-4 py-2 rounded-lg border-2 border-black text-black placeholder-gray-500 bg-white focus:outline-none focus:ring-2 focus:ring-black"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        <button 
          type="submit"
          disabled={loading}
          className="w-full px-4 py-2 rounded-lg border-2 border-black text-black font-medium bg-white hover:bg-gray-100 transition-all disabled:opacity-50 disabled:cursor-not-allowed mb-4"
        >
          {loading ? "Logging in..." : "Login"}
        </button>

        <div className="text-center">
          <button
            type="button"
            onClick={onSwitchToRegister}
            className="text-black underline hover:no-underline text-sm"
          >
            Don't have an account? Register
          </button>
        </div>
      </form>
    </div>
  );
}

export default Login;
