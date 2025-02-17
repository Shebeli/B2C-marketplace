export function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex items-center justify-center h-screen">
      <main>{children}</main>
    </div>
  );
}
