import { NavbarProfileInfo } from "../../types/ui/general-types";
import { getAccessFromCookies } from "../../fetch/fetch-auth";
import { API_ROUTES } from "../../apiRoutes";
import { fetchWithAuth } from "../../fetch/fetch-auth";

const { USER: USER_ENDPOINTS } = API_ROUTES;

export async function getUserNavbarProfile(): Promise<null | NavbarProfileInfo> {
  const accessToken = await getAccessFromCookies();
  if (!accessToken) return null;

  const url = new URL(USER_ENDPOINTS.NAVBAR_PROFILE, process.env.API_BASE_URL);
  try {
    const response = await fetchWithAuth(url, accessToken);

    if (!response.ok) {
      const resData = await response.text();
      console.error(
        "Invalid response for fetching user's navbar profile:",
        response.status,
        resData
      );
      return null;
    }
    return await response.json();
  } catch (err) {
    console.error("Failed to fetch user's navbar profile:", err);
    return null;
  }
}
