"use server";

import { API_ROUTES } from "../drfRoutes";
import { redirect } from "next/navigation";
import { revalidatePath } from "next/cache";
import { fetchAccessToken, fetchWithAuth } from "../utils/fetch";
import { NavbarProfileInfo } from "../constants";

const { USER: USER_ENDPOINTS } = API_ROUTES;

export async function fetchUserNavbarProfile(): Promise<null | NavbarProfileInfo> {
  try {
    const token = await fetchAccessToken();
    if (!token) {
      return null;
    }
    const response = await fetchWithAuth(USER_ENDPOINTS.NAVBAR_PROFILE, token);

    // can be changed to return an error message instead,
    // which displays a friendly error message of the attempt
    // to fetch user's profile info.
    if (!response.ok) {
      console.error(
        "Failed to fetch user's navbar profile:",
        response.statusText
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
    await fetch("/api/auth/logout", { method: "POST" });
  } catch (error) {
    console.error("Failed to logout the user with server action:", error);
    throw new Error("Failed to logout the user.");
  }

  revalidatePath(path);
  redirect(path);
}

