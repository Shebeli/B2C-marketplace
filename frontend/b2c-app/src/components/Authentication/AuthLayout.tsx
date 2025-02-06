import { Outlet } from "react-router-dom";
import { ThemeProvider } from "../Theme/ThemeContext";

// Abstract component.
const AuthLayout: React.FC = () => {
  return (
    <ThemeProvider>
      <div className="flex items-center justify-center h-screen">
        <main>
          <Outlet />
        </main>
      </div>
    </ThemeProvider>
  );
};

export default AuthLayout;
