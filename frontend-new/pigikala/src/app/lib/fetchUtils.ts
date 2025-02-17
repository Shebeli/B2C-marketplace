import { RequestInit } from "next/dist/server/web/spec-extension/request";
import { cookies } from "next/headers";

// utility function to retrieve access token from cookie
export async function fetchAccessToken() {
  const cookieStore = await cookies();
  const accessToken = cookieStore.get("access_token");
  return accessToken ? accessToken.value : null;
}

// For any fetches from the backend while authenticated.
// This function should be only called within server actions.
export const fetchWithAuth = async (url: string, options: RequestInit = {}) => {
  const accessToken = await fetchAccessToken();

  if (!accessToken) {
    throw new Error("No access token was found within cookie");
  }

  const headers = {
    ...options.headers,
    Authorization: `Bearer ${accessToken}`,
    "Content-Type": "application/json",
  };

  const finalOptions: RequestInit = {
    ...options,
    headers,
  };

  const response = await fetch(url, finalOptions);

  if (!response.ok) {
    throw new Error(`Faled to fetch from url ${url}`);
  }

  return await response.json();
};
