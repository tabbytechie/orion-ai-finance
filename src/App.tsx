/**
 * Main Application Component (App.tsx)
 *
 * This file serves as the root of the React application. It sets up all the
 * necessary context providers, defines the application's routing structure,
 * and orchestrates the overall layout.
 *
 * Key Responsibilities:
 * - Initializes and provides global contexts (QueryClient, Theme, Auth, Tooltip).
 * - Configures React Router for navigation between different pages.
 * - Uses a `ProtectedLayout` to wrap routes that require user authentication.
 * - Handles redirects and not-found pages gracefully.
 */
import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { ThemeProvider } from "./contexts/ThemeContext";
import { AuthProvider } from "./contexts/AuthContext";
import { ProtectedLayout } from "./components/layout/ProtectedLayout";
import Dashboard from "./pages/Dashboard";
import Transactions from "./pages/Transactions";
import Insights from "./pages/Insights";
import Profile from "./pages/Profile";
import Settings from "./pages/Settings";
import Login from "./pages/Login";
import NotFound from "./pages/NotFound";

// Initialize a new QueryClient for data fetching and caching.
const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <ThemeProvider>
      <AuthProvider>
        <TooltipProvider>
          {/* Toaster components for displaying notifications */}
          <Toaster />
          <Sonner />

          <BrowserRouter>
            <Routes>
              {/* Public route for login */}
              <Route path="/login" element={<Login />} />

              {/* Protected routes that require authentication */}
              <Route path="/dashboard" element={<ProtectedLayout><Dashboard /></ProtectedLayout>} />
              <Route path="/transactions" element={<ProtectedLayout><Transactions /></ProtectedLayout>} />
              <Route path="/insights" element={<ProtectedLayout><Insights /></ProtectedLayout>} />
              <Route path="/profile" element={<ProtectedLayout><Profile /></ProtectedLayout>} />
              <Route path="/settings" element={<ProtectedLayout><Settings /></ProtectedLayout>} />

              {/* Redirect root path to the dashboard */}
              <Route path="/" element={<Navigate to="/dashboard" replace />} />

              {/* Catch-all route for 404 Not Found pages */}
              <Route path="*" element={<NotFound />} />
            </Routes>
          </BrowserRouter>
        </TooltipProvider>
      </AuthProvider>
    </ThemeProvider>
  </QueryClientProvider>
);

export default App;