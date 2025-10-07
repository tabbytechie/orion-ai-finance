import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { PasswordInput } from './PasswordInput';
import { Label } from './label';

describe('PasswordInput', () => {
  it('should render an input with type="password" by default', () => {
    render(
      <>
        <Label htmlFor="password">Password</Label>
        <PasswordInput id="password" />
      </>
    );
    const input = screen.getByLabelText('Password');
    expect(input).toBeInTheDocument();
    expect(input).toHaveAttribute('type', 'password');
  });

  it('should toggle the input type to "text" when the eye icon is clicked', () => {
    render(
      <>
        <Label htmlFor="password">Password</Label>
        <PasswordInput id="password" />
      </>
    );
    const input = screen.getByLabelText('Password');
    const toggleButton = screen.getByRole('button');

    // Initially, the input type should be "password"
    expect(input).toHaveAttribute('type', 'password');

    // Click the button to show the password
    fireEvent.click(toggleButton);
    expect(input).toHaveAttribute('type', 'text');

    // Click the button again to hide the password
    fireEvent.click(toggleButton);
    expect(input).toHaveAttribute('type', 'password');
  });

  it('should display the EyeOff icon when the password is visible', () => {
    render(<PasswordInput />);
    const toggleButton = screen.getByRole('button');

    // Initially, the Eye icon should be visible
    expect(screen.getByTestId('eye-icon')).toBeInTheDocument();
    expect(screen.queryByTestId('eye-off-icon')).not.toBeInTheDocument();

    // Click the button to show the password
    fireEvent.click(toggleButton);
    expect(screen.queryByTestId('eye-icon')).not.toBeInTheDocument();
    expect(screen.getByTestId('eye-off-icon')).toBeInTheDocument();
  });
});