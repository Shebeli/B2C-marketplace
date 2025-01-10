import React from "react";

import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Layout from "./components/Layout";
import ProductPage from "./components/ProductPage/ProductPage";
import Home from "./components/Home";
import ProductsList from "./components/ProductsList/ProductsList";

const App: React.FC = () => {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />}></Route>
          <Route path="/product-page" element={<ProductPage />}></Route>
          <Route path="/products-list" element={<ProductsList />}></Route>
          <Route path="/contact" element={<ProductPage />}></Route>
        </Routes>
      </Layout>
    </Router>
  );
};

export default App;
