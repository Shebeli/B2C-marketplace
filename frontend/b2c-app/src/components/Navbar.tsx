import { MainLogo } from "../assets/MainLogo";
import ThemeController from "./Theme/ThemeController";

const Navbar: React.FC = () => {
  return (
    <div className="navbar border-b-2 border-base-300 py-3">
      <div className="flex-1">
        <a className="btn bg-base-100 border-0" href="/">
          <MainLogo width="120" />
        </a>
        <div className="mr-2">
          <ThemeController />
        </div>
        <div className="form-control mx-4">
          <input
            type="text"
            placeholder="جستجو"
            className="input input-bordered input-sm w-72 bg-base-200 h-9"
          />
        </div>
      </div>
      <div className="flex-none">
        <div className="dropdown dropdown-end mx-2">
          <div tabIndex={0} role="button" className="btn btn-ghost btn-circle">
            <div className="indicator">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-7 w-7"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"
                />
              </svg>
              <span className="badge badge-sm indicator-item">8</span>
            </div>
          </div>
          <div
            tabIndex={0}
            className="card card-compact dropdown-content bg-base-100 z-[1] mt-3 w-52 shadow"
          >
            <div className="card-body">
              <span className="text-lg font-bold">8 Items</span>
              <span className="text-info">Subtotal: $999</span>
              <div className="card-actions">
                <button className="btn btn-primary btn-block">View cart</button>
              </div>
            </div>
          </div>
        </div>
        <div className="dropdown dropdown-end">
          <div
            tabIndex={0}
            role="button"
            className="btn btn-ghost btn-circle avatar"
          >
            <div className="w-10 rounded-full">
              <img
                alt="Tailwind CSS Navbar component"
                src="https://img.daisyui.com/images/stock/photo-1534528741775-53994a69daeb.webp"
              />
            </div>
          </div>
          <ul
            tabIndex={0}
            className="menu menu-md dropdown-content bg-base-100 rounded-box z-[1] mt-3 w-52 p-2 shadow font-semibold"
          >
            <li>
              <a>پروفایل خریدار</a>
            </li>
            <li>
              <a>پروفایل فروشنده</a>
            </li>

            <li>
              <a>خروج از حساب</a>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Navbar;
