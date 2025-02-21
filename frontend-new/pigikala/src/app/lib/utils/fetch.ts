import { RequestInit } from "next/dist/server/web/spec-extension/request";
import { cookies } from "next/headers";

// retrieve access token from cookie
export async function fetchAccessToken() {
  const cookieStore = await cookies();
  const accessToken = cookieStore.get("access_token");
  return accessToken ? accessToken.value : null;
}

// Used for fetching from endpoints which require JWT authorization,
// by adding the header 'Authorization: Bearer {token}' to the request.
export const fetchWithAuth = async (
  url: string,
  accessToken: string,
  options: RequestInit = {}
) => {
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
    throw new Error(`Failed to fetch from url ${url}`);
  }

  return await response.json();
};

export async function getCurrentUser() {}
