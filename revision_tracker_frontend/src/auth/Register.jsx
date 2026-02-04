import { useState } from "react";
import { register } from "../api/auth";

function Register({ onSwitchToLogin }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");

    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    if (password.length < 6) {
      setError("Password must be at least 6 characters");
      return;
    }

    if (password.length > 72) {
      setError("Password is too long. Maximum length is 72 characters.");
      return;
    }

    setLoading(true);
    try {
      const data = await register(email, password);
      // Backend register returns UserRead, not access_token
      // User needs to login after registration
      if (data && data.id) {
        setError("Registration successful! Please login.");
        // Auto-switch to login after a short delay
        setTimeout(() => {
          onSwitchToLogin();
        }, 1500);
      } else {
        setError(data?.detail || "Registration failed. Please try again.");
      }
    } catch (error) {
      console.error("Registration error:", error);
      setError("Registration failed. Please try again.");
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
        <h2 className="text-2xl font-bold text-black mb-6 text-center">Register</h2>

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

        <div className="mb-4">
          <input
            type="password"
            className="w-full px-4 py-2 rounded-lg border-2 border-black text-black placeholder-gray-500 bg-white focus:outline-none focus:ring-2 focus:ring-black"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        <div className="mb-6">
          <input
            type="password"
            className="w-full px-4 py-2 rounded-lg border-2 border-black text-black placeholder-gray-500 bg-white focus:outline-none focus:ring-2 focus:ring-black"
            placeholder="Confirm Password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
          />
        </div>

        <button 
          type="submit"
          disabled={loading}
          className="w-full px-4 py-2 rounded-lg border-2 border-black text-black font-medium bg-white hover:bg-gray-100 transition-all disabled:opacity-50 disabled:cursor-not-allowed mb-4"
        >
          {loading ? "Registering..." : "Register"}
        </button>

        <div className="text-center">
          <button
            type="button"
            onClick={onSwitchToLogin}
            className="text-black underline hover:no-underline text-sm"
          >
            Already have an account? Login
          </button>
        </div>
      </form>
    </div>
  );
}

export default Register;
