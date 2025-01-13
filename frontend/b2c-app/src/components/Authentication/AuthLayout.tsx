import { Outlet } from "react-router-dom";
// Abstract component used as a parent component by other auth components like login component.
const AuthLayout: React.FC = () => {
  return (
    <div className="flex items-center justify-center h-screen">
      <main>
        <Outlet />
      </main>
    </div>
  );
};

export default AuthLayout;
