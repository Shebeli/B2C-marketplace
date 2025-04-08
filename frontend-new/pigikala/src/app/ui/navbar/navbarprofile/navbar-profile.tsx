import NavbarLoginButton from "./login-button";
import NavbarProfileDropdown from "./profile";
import { getUserNavbarProfile } from "@/app/lib/services/api/fetch/navbar/fetchNavbar";

export default async function NavbarProfile() {
  const navbarProfileData = await getUserNavbarProfile();

  if (navbarProfileData) {
    return <NavbarProfileDropdown profileInfo={navbarProfileData} />;
  }
  return <NavbarLoginButton />;
}
