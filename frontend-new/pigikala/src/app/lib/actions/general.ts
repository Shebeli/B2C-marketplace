  "use server";

  import { API_ROUTES } from "../drfRoutes";
  import { redirect } from "next/navigation";
  import { revalidatePath } from "next/cache";
  import { fetchWithAuth, getAccessFromCookies } from "../utils/fetch";
  import { NavbarProfileInfo } from "../constants";
  import { cookies } from "next/headers";

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

  export async function signOut(path: string) {
    try {
      const cookieStore = await cookies();
      cookieStore.delete("access_token");
      cookieStore.delete("refresh_token");
    } catch (error) {
      console.error("Failed to logout the user with server action:", error);
      throw new Error("Failed to logout the user.");
    }

    revalidatePath(path);
    redirect(path);
  }
