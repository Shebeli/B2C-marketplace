import { MainLogo } from "../assets/MainLogo";
import { FaRightToBracket } from "react-icons/fa6";
import ThemeController from "../components/Theme/ThemeController";
import { useEffect, useState } from "react";
import { axiosInstance } from "../axiosInstance";
import { AxiosResponse } from "axios";
import { navigateTo } from "../navigation";
import { ProfileInfo } from "./constants";
import { UserProfileDropdown } from "./UserProfileDropdown";

const Navbar: React.FC = () => {
  const [userProfile, setUserProfile] = useState<ProfileInfo | null>(null);
  const [loading, setLoading] = useState(true);

  const handleLogout = () => {
    localStorage.removeItem("refreshToken");
    localStorage.removeItem("accessToken");
    setUserProfile(null);
    navigateTo("/");
  };

  useEffect(() => {
    console.log("meow");
    if (!localStorage.getItem("accessToken")) {
      setLoading(false);
      return;
    }

    const fetchProfile = async (): Promise<void> => {
      try {
        const response: AxiosResponse<ProfileInfo> = await axiosInstance.get(
          "/api/user/account/navbar_info/"
        );
        console.log(response.data);
        setUserProfile(response.data);
      } catch (err) {
        console.error(err);
        setUserProfile(null);
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, []);

  const renderNavbarProfile = () => {
    if (loading)
      return <div className="skeleton w-10 h-10 rounded-full "></div>;

    if (userProfile)
      return (
        <UserProfileDropdown
          userProfile={userProfile}
          handleLogout={handleLogout}
        />
      );
    return (
      <a
        href="/login"
        className="btn btn-ghost border-[1.5px] border-base-300 flex flex-row gap-1.5 items-center justify-center  font-normal"
      >
        <FaRightToBracket className="size-5" />
        <p>ورود | ثبت نام</p>
      </a>
    );
  };

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
            className="input input-bordered input-sm lg:w-72 md:w-52 w-32 bg-base-200 h-9"
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
        {renderNavbarProfile()}
      </div>
    </div>
  );
};

export default Navbar;
