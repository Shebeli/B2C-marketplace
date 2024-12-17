import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import ProductPage from "./Product/ProductPage.tsx";
import App from "./App.tsx";
import ThemeController from "./ThemeController.tsx";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <div className="justify-items-center">
      <div className="pt-2 px-2">
        <ThemeController />
      </div>
      <div className="">
        <ProductPage />
      </div>
    </div>
  </StrictMode>
);
