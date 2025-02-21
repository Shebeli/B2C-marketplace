import Link from "next/link";
import { FaRightToBracket } from "react-icons/fa6";

export default function NavbarLoginButton() {
  return (
    <Link
      href="/auth/login"
      className="btn btn-ghost border-[1.5px] border-base-300 flex flex-row gap-1.5 items-center justify-center  font-normal"
    >
      <FaRightToBracket className="size-5" />
      <p>ورود | ثبت نام</p>
    </Link>
  );
}
