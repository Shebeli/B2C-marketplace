"use server";

import { RequestInit } from "next/dist/server/web/spec-extension/request";
import { cookies } from "next/headers";
import { ResponseCookies } from "next/dist/compiled/@edge-runtime/cookies";
import { ReadonlyRequestCookies } from "next/dist/server/web/spec-extension/adapters/request-cookies";
import { API_ROUTES } from "../apiRoutes";


// retrieve refresh token from cookies (only for server actions)
export async function getRefreshFromCookies() {
  const cookieStore = await cookies();
  const refreshToken = cookieStore.get("refresh_token");
  return refreshToken ? refreshToken.value : null;
}

// retrieve access token from cookies (only for server actions)
export async function getAccessFromCookies() {
  const cookieStore = await cookies();
  const accessToken = cookieStore.get("access_token");
  return accessToken ? accessToken.value : null;
}

// Update the cookies with access token (should be called when a newly created access token is fetched)
export async function setAccessTokenCookie(
  cookies: ReadonlyRequestCookies | ResponseCookies,
  accessToken: string
) {
  cookies.set("access_token", accessToken, {
    httpOnly: true,
    sameSite: "strict",
    secure: process.env.NODE_ENV === "production",
    path: "/",
    maxAge: Number(process.env.REFRESH_TOKEN_LIFETIME) * 60,
  });
}

// Update the cookies with access token (should be called when a newly created access token is fetched)
export async function setRefreshTokenCookie(
  cookies: ReadonlyRequestCookies | ResponseCookies,
  refreshToken: string
) {
  cookies.set("refresh_token", refreshToken, {
    httpOnly: true,
    sameSite: "strict",
    secure: process.env.NODE_ENV === "production",
    path: "/",
    maxAge: Number(process.env.REFRESH_TOKEN_LIFETIME) * 24 * 60 * 60,
  });
}

interface TokenRefreshSuccess {
  success: true;
  accessToken: string;
}

interface TokenRefershError {
  success: false;
  error: string;
  statusCode: number;
}

// Fetch a new access token from backend using the passed in refresh token,
export async function fetchNewAccessToken(
  refreshToken: string
): Promise<TokenRefershError | TokenRefreshSuccess> {
  const url = new URL(API_ROUTES.AUTH.REFRESH, process.env.API_BASE_URL);
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      refresh: refreshToken,
    }),
  });

  if (!response.ok) {
    if (response.status === 401) {
      return {
        success: false,
        error: "Refresh token is invalid or expired",
        statusCode: 401,
      };
    } else {
      return {
        success: false,
        error: `Failed to refresh token: ${await response.text()}`,
        statusCode: response.status,
      };
    }
  }

  const data = await response.json();
  return { success: true, accessToken: data.access };
}

// Retrieves a valid access token from cookies.
// If no access token is found, attempt to fetch a new access token using refresh token
export async function getOrRefreshAccessToken() {
  let accessToken = await getAccessFromCookies();
  if (!accessToken) {
    const refreshToken = await getRefreshFromCookies();
    if (!refreshToken) {
      return null;
    }

    // If refresh token exists attempt to fetch a new access token
    const result = await fetchNewAccessToken(refreshToken);
    // refresh token doesn't exist, thus the user is not authenticated.
    if (!result.success) {
      console.error("Failed to refresh the access token:", result);
      return null;
    }
    accessToken = result.accessToken;
  }
  return accessToken;
}

// Used for fetching from endpoints which require JWT authorization,
// by adding the header 'Authorization: Bearer {token}' to the request.
export const fetchWithAuth = async (
  url: string | URL,
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
  return response;
};

// Check the user's authentication status by checking if an access token can be retrieved or not.
export async function isUserAuthenticated() {
  const accessToken = await getOrRefreshAccessToken();
  return accessToken ? true : false;
}
