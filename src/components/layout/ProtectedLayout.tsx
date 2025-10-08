/**
 * Protected Layout Component
 *
 * This component wraps pages that require authentication, providing a consistent
 * layout and protecting them from unauthenticated access. It combines the
 * `ProtectedRoute` and `Layout` components into a single, reusable wrapper.
 */
import { FC, ReactNode } from "react";
import { ProtectedRoute } from "../ProtectedRoute";
import { Layout } from "./Layout";

interface ProtectedLayoutProps {
  children: ReactNode;
}

export const ProtectedLayout: FC<ProtectedLayoutProps> = ({ children }) => {
  return (
    <ProtectedRoute>
      <Layout>
        {children}
      </Layout>
    </ProtectedRoute>
  );
};