import { NextRequest, NextResponse } from "next/server";
import axios from "axios";

export async function middleware(req: NextRequest) {
  const accessToken = req.cookies.get("access_token")?.value;
  const refreshToken = req.cookies.get("refresh_token")?.value;
  const protectedRoutes = ["/dashboard"]; // not implemented yet

  // no access token but refresh token, attempt to fetch a new access token
  if (!accessToken && refreshToken) {
    try {
      await axios.post(
        `${req.nextUrl.origin}/api/auth/refresh`
      );
      return NextResponse.next();
    } catch (error) {
      console.error(
        "Error on attempting to fetch a new access token via middleware:",
        error
      );
      const response = NextResponse.redirect(new URL("/login", req.url));
      response.cookies.delete("access_token");
      response.cookies.delete("refresh_token");
      return response;
    }
  }

  // no access token and the requested url is a protected page, redirect to login page
  if (protectedRoutes.includes(req.nextUrl.pathname) && !accessToken) {
    return NextResponse.redirect(new URL("/login", req.url));
  }

  return NextResponse.next();
}
