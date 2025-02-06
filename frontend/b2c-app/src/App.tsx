import React, { ReactNode, useEffect } from "react";

import {
  BrowserRouter as Router,
  Route,
  Routes,
  useNavigate,
} from "react-router-dom";
import Layout from "./components/Layout";
import ProductPage from "./components/ProductPage/ProductPage";
import Home from "./components/Home";
import ProductsList from "./components/ProductsList/ProductsList";
import AuthLayout from "./components/Authentication/AuthLayout";
import Login from "./components/Authentication/Login";
import VerifyPhone from "./components/Authentication/VerifyPhone";
import { setNavigate } from "./navigation";

interface NavigationSetupProps {
  children: ReactNode;
}

const NavigationSetup: React.FC<NavigationSetupProps> = ({ children }) => {
  const navigate = useNavigate();
  useEffect(() => {
    setNavigate(navigate);
  }, [navigate]);

  return <>{children}</>;
};

const App: React.FC = () => {
  return (
    <Router>
      <NavigationSetup>
        <Routes>
          <Route element={<Layout />}>
            <Route path="/" element={<Home />} />
            <Route path="/product-page" element={<ProductPage />} />
            <Route path="/products-list" element={<ProductsList />} />
            <Route path="/contact" element={<ProductPage />} />
          </Route>
          <Route element={<AuthLayout />}>
            <Route path="/login" element={<Login />} />
            <Route path="/verify-phone" element={<VerifyPhone />} />
          </Route>
        </Routes>
      </NavigationSetup>
    </Router>
  );
};

export default App;
