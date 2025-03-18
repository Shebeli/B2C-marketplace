import Image from "next/image";
import {
  FaShop,
  FaUser,
  FaRightFromBracket,
  FaBasketShopping,
} from "react-icons/fa6";
import { NavbarProfileInfo } from "@/app/lib/types/ui/general-types";
import { DEFAULT_PROFILE_IMAGE_URL } from "@/app/lib/constants/assets";
import { signOut } from "@/app/lib/actions/general";

export default function NavbarProfileDropdown({
  profileInfo,
}: {
  profileInfo: NavbarProfileInfo | null;
}) {
  return (
    <div className="dropdown dropdown-end">
      <div
        tabIndex={0}
        role="button"
        aria-label="User profile dropdown"
        className="btn btn-ghost btn-circle avatar"
      >
        <div className="w-10 rounded-full">
          <Image
            width={40}
            height={40}
            alt="User Profile Image"
            src={
              profileInfo && profileInfo.pictureUrl
                ? profileInfo.pictureUrl
                : DEFAULT_PROFILE_IMAGE_URL
            }
          />
        </div>
      </div>
      <ul
        tabIndex={0}
        className="menu menu-md dropdown-content bg-base-100 rounded-box z-1 mt-3 w-52 shadow-sm"
      >
        <li className="text-sm my-2">وارد شده با {profileInfo?.phone}</li>
        <li>
          <a aria-label="Account information">
            <FaUser className="size-4" />
            <span>اطلاعات اکانت</span>
          </a>
        </li>
        <li>
          <a aria-label="Buyer profile">
            <FaBasketShopping className="size-4" />
            <span>پروفایل خریدار</span>
          </a>
        </li>
        <li>
          <a aria-label="Seller profile">
            <FaShop className="size-4" />
            <span>پروفایل فروشنده</span>
          </a>
        </li>
        <hr className="border-base-300 my-1" />
        <li className="text-error">
          <form
            action={async () => {
              "use server";
              await signOut("/");
            }}
          >
            <button className="flex gap-2" aria-label="Sign out">
              <FaRightFromBracket className="size-4" />
              <span>خروج از حساب</span>
            </button>
          </form>
        </li>
      </ul>
    </div>
  );
}
