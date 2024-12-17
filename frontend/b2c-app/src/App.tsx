import { useState } from "react";

function App() {
  const [count, setCount] = useState(0);

  return (
    <>
      <label className="flex cursor-pointer gap-2">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
        </svg>

        <input
          type="checkbox"
          value="night"
          className="toggle theme-controller"
        />
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <circle cx="12" cy="12" r="5" />
          <path d="M12 1v2M12 21v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4M1 12h2M21 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4" />
        </svg>
      </label>
      <div className="card card-normal bg-base-300 w-2/3 shadow-xl place-self-center">
        <figure className="bg-content">
          <img
            src="src/assets/sample_images/product-main-image.webp"
            alt="Laptop"
            className="h-48 w-48"
          />
        </figure>
        <div className="card-body items-center text-center">
          <h1 className="card-title">{count} :شمارش فعلی</h1>
          <p>.یک اپلیکیشن برای شمردن کانتر</p>
          <div className="card-actions">
            <button
              className="btn btn-primary btn-sm"
              onClick={() => setCount((count) => count + 1)}
            >
              افزایش کانتر
            </button>
            <button
              className="btn btn-secondary btn-sm"
              onClick={() => setCount((count) => count - 1)}
            >
              کاهش کانتر
            </button>
            <button
              className="btn btn-accent btn-sm"
              onClick={() => setCount((count) => count * 2)}
            >
              2 برابر
            </button>
            <button
              className="btn btn-neutral btn-sm"
              onClick={() =>
                setCount((count) => (count !== 0 ? count / 2 : count))
              }
            >
              2 تقسیم بر
            </button>
            <button className="btn btn-sm" onClick={() => setCount(0)}>
              ریست کانتر
            </button>
          </div>
        </div>
      </div>
    </>
  );
}

export default App;
