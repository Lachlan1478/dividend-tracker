import { ButtonHTMLAttributes, ReactNode } from "react";

export function Button({ children, className = "", ...props }: ButtonHTMLAttributes<HTMLButtonElement> & { children: ReactNode }) {
  return (
    <button
      {...props}
      className={`bg-blue-600 hover:bg-blue-700 text-white font-semibold px-4 py-2 rounded ${className}`}
    >
      {children}
    </button>
  );
}
