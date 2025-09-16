"use client";

import { useState } from "react";
import useAuth from "@/hooks/useAuth";

export default function AuthPage() {
  const { signIn, signUp, loading, user } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isSignUp, setIsSignUp] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    setIsSubmitting(true);
    
    try {
      if (isSignUp) {
        const { error } = await signUp(email, password);
        if (error) {
          console.error("Sign up error:", error.message);
          setError(error.message);
        } else {
          setSuccess("Sign up successful! Check your email for verification link.");
        }
      } else {
        const { error } = await signIn(email, password);
        if (error) {
          console.error("Sign in error:", error.message);
          if (error.message.includes("Invalid login credentials")) {
            setError("Invalid email or password. Please check your credentials and try again.");
          } else if (error.message.includes("Email not confirmed")) {
            setError("Please verify your email address before signing in.");
          } else {
            setError(error.message);
          }
        } else {
          setSuccess("Sign in successful! Welcome back.");
          
          setEmail("");
          setPassword("");
        }
      }
    } catch (err) {
      setError("An unexpected error occurred. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  // Show success message if user is authenticated
  if (user && !loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="space-y-4 p-6 border rounded max-w-md text-center">
          <div className="p-3 bg-green-100 border border-green-400 text-green-700 rounded">
            ✅ Successfully signed in!
          </div>
          <p className="text-gray-600">Welcome, {user.email}!</p>
          <p className="text-sm text-gray-500">
            Email verified: {user.emailVerified ? "✅ Yes" : "❌ No"}
          </p>
        </div>
      </div>
    );
  }

  if (loading) return (
    <div className="min-h-screen flex items-center justify-center">
      <div>Loading...</div>
    </div>
  );

  return (
    <div className="min-h-screen flex items-center justify-center">
      <form onSubmit={handleSubmit} className="space-y-4 p-6 border rounded max-w-md">
        <h1 className="text-xl font-semibold">{isSignUp ? "Sign Up" : "Sign In"}</h1>
        
        {error && (
          <div className="p-3 bg-red-100 border border-red-400 text-red-700 rounded">
            ❌ {error}
          </div>
        )}
        
        {success && (
          <div className="p-3 bg-green-100 border border-green-400 text-green-700 rounded">
            ✅ {success}
          </div>
        )}
        
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
          disabled={isSubmitting}
        />
        
        <input
          type="password"
          placeholder="Password (min 6 characters)"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          minLength={6}
          required
          disabled={isSubmitting}
        />
        
        <button 
          type="submit" 
          className="w-full p-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed"
          disabled={isSubmitting}
        >
          {isSubmitting ? "Processing..." : (isSignUp ? "Sign Up" : "Sign In")}
        </button>
        
        <button
          type="button"
          onClick={() => {
            setIsSignUp(!isSignUp);
            setError("");
            setSuccess("");
          }}
          className="w-full text-blue-500 hover:underline"
          disabled={isSubmitting}
        >
          {isSignUp ? "Already have an account? Sign In" : "Need an account? Sign Up"}
        </button>
      </form>
    </div>
  );
}