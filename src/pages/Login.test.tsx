import { render, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi, beforeEach, Mock } from 'vitest';
import { BrowserRouter } from 'react-router-dom';
import Login from './Login';
import { supabase } from '@/integrations/supabase/client';

// Mock dependencies
vi.mock('@/integrations/supabase/client', () => ({
  supabase: {
    auth: {
      signUp: vi.fn(),
      resetPasswordForEmail: vi.fn(),
    },
  },
}));

const mockNavigate = vi.fn();
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useNavigate: () => mockNavigate,
  };
});

const mockLogin = vi.fn();
vi.mock('@/contexts/AuthContext', () => ({
  useAuth: () => ({
    login: mockLogin,
  }),
}));

const mockToast = vi.fn();
vi.mock('@/hooks/use-toast', () => ({
  useToast: () => ({
    toast: mockToast,
  }),
}));

const renderLogin = () => {
  const user = userEvent.setup();
  const { container } = render(
    <BrowserRouter>
      <Login />
    </BrowserRouter>
  );
  return { user, container };
};

describe('Login Page', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should handle successful login', async () => {
    mockLogin.mockResolvedValueOnce({});
    const { user } = renderLogin();

    const loginTab = screen.getByRole('tabpanel', { name: 'Login' });

    await user.type(within(loginTab).getByLabelText('Email'), 'test@example.com');
    await user.type(within(loginTab).getByLabelText('Password'), 'password123');
    await user.click(within(loginTab).getByRole('button', { name: 'Sign In' }));

    await waitFor(() => {
      expect(mockLogin).toHaveBeenCalledWith('test@example.com', 'password123');
      expect(mockNavigate).toHaveBeenCalledWith('/dashboard');
    });
  });

  it('should handle successful sign-up', async () => {
    (supabase.auth.signUp as Mock).mockResolvedValueOnce({ error: null });
    const { user } = renderLogin();

    await user.click(screen.getByRole('tab', { name: 'Sign Up' }));

    const signupTab = await screen.findByRole('tabpanel', { name: 'Sign Up' });

    await user.type(within(signupTab).getByLabelText('Email'), 'newuser@example.com');
    await user.type(within(signupTab).getByLabelText('Password'), 'newpassword123');
    await user.type(within(signupTab).getByLabelText('Confirm Password'), 'newpassword123');

    await user.click(within(signupTab).getByRole('button', { name: 'Sign Up' }));

    await waitFor(() => {
      expect(supabase.auth.signUp).toHaveBeenCalledWith({
        email: 'newuser@example.com',
        password: 'newpassword123',
        options: {
          emailRedirectTo: expect.any(String),
        },
      });
    });
  });

  it('should show an error if sign-up passwords do not match', async () => {
    const { user } = renderLogin();

    await user.click(screen.getByRole('tab', { name: 'Sign Up' }));

    const signupTab = await screen.findByRole('tabpanel', { name: 'Sign Up' });

    await user.type(within(signupTab).getByLabelText('Email'), 'test@example.com');
    await user.type(within(signupTab).getByLabelText('Password'), 'password123');
    await user.type(within(signupTab).getByLabelText('Confirm Password'), 'password456');

    await user.click(within(signupTab).getByRole('button', { name: 'Sign Up' }));

    await waitFor(() => {
      expect(mockToast).toHaveBeenCalledWith({
        title: "Passwords don't match",
        description: "Please make sure both passwords are the same.",
        variant: "destructive",
      });
    });
  });

  it('should handle password reset requests', async () => {
    (supabase.auth.resetPasswordForEmail as Mock).mockResolvedValueOnce({ error: null });
    const { user } = renderLogin();

    await user.click(screen.getByRole('tab', { name: 'Reset' }));

    const resetTab = await screen.findByRole('tabpanel', { name: 'Reset' });

    await user.type(within(resetTab).getByLabelText('Email'), 'reset@example.com');
    await user.click(within(resetTab).getByRole('button', { name: 'Send Reset Link' }));

    await waitFor(() => {
      expect(supabase.auth.resetPasswordForEmail).toHaveBeenCalledWith('reset@example.com', {
        redirectTo: expect.stringContaining('/reset-password'),
      });
    });
  });
});