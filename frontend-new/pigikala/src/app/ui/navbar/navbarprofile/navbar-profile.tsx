import { fetchUserNavbarProfile } from "@/app/lib/actions/general";
import NavbarLoginButton from "./login-button";
import NavbarProfileDropdown from "./profile";

export default async function NavbarProfile() {
  const navbarProfileData = await fetchUserNavbarProfile();

  if (navbarProfileData) {
    return <NavbarProfileDropdown profileInfo={navbarProfileData} />;
  }
  return <NavbarLoginButton />;
}
