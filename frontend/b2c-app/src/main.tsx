import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import ProductPage from "./Product/ProductPage.tsx";
import ThemeController from "./ThemeController.tsx";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <div className="items-start justify-center min-h-screen flex">
      <div>
        <div className="pt-2 px-2 self-center justify-self-center flex">
          <ThemeController />
        </div>
        <ProductPage />
      </div>
    </div>
  </StrictMode>
);
