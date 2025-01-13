import React from "react";

import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Layout from "./components/Layout";
import ProductPage from "./components/ProductPage/ProductPage";
import Home from "./components/Home";
import ProductsList from "./components/ProductsList/ProductsList";
import AuthLayout from "./components/Authentication/AuthLayout";
import Login from "./components/Authentication/Login";
import VerifyLogin from "./components/Authentication/Register";

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<Home />} />
          <Route path="/product-page" element={<ProductPage />} />
          <Route path="/products-list" element={<ProductsList />} />
          <Route path="/contact" element={<ProductPage />} />
        </Route>
        <Route element={<AuthLayout />}>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<VerifyLogin/>}/>
        </Route>
      </Routes>
    </Router>
  );
};

export default App;
