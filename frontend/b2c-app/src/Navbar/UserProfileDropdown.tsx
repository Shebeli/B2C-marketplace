import { ProfileInfo } from "./constants";

import {
  FaShop,
  FaUser,
  FaRightFromBracket,
  FaBasketShopping,
} from "react-icons/fa6";

interface DropdownProps {
  userProfile: ProfileInfo;
  handleLogout: () => void;
}

export const UserProfileDropdown: React.FC<DropdownProps> = ({
  userProfile,
  handleLogout,
}) => {
  return (
    <div className="dropdown dropdown-end">
      <div
        tabIndex={0}
        role="button"
        className="btn btn-ghost btn-circle avatar"
      >
        <div className="w-10 rounded-full">
          <img
            alt="Tailwind CSS Navbar component"
            src={
              userProfile.pictureUrl
                ? userProfile.pictureUrl
                : "default-profile.jpg"
            }
          />
        </div>
      </div>
      <ul
        tabIndex={0}
        className="menu menu-md dropdown-content bg-base-100 rounded-box z-[1] mt-3 w-52 shadow"
      >
        <li className="text-sm my-2">وارد شده با {userProfile?.phone}</li>
        <li>
          <a>
            <FaUser className="size-4" />
            <span>اطلاعات اکانت</span>
          </a>
        </li>
        <li>
          <a>
            <FaBasketShopping className="size-4" />
            <span>پروفایل خریدار</span>
          </a>
        </li>
        <li>
          <a>
            <FaShop className="size-4" />
            <span>پروفایل فروشنده</span>
          </a>
        </li>
        <hr className="border-base-300 my-1" />
        <li className="text-error">
          <a onClick={handleLogout}>
            <FaRightFromBracket className="size-4" />
            <span>خروج از حساب</span>
          </a>
        </li>
      </ul>
    </div>
  );
};
