import { NextRequest, NextResponse } from "next/server";
import {
  fetchNewAccessToken,
  setAccessTokenCookie,
} from "@/app/lib/fetch/fetchAuth";

export async function middleware(req: NextRequest) {
  let accessToken = req.cookies.get("access_token")?.value;
  const refreshToken = req.cookies.get("refresh_token")?.value;
  const protectedRoutes = ["/dashboard"]; // not implemented yet
  const authRoutes = ["/auth/:path"];

  // Check if the path is in auth section, redirect the user to home page instead
  if (req.nextUrl.pathname.startsWith("/auth/") && accessToken) {
    return NextResponse.redirect(new URL("/", req.url));
  }

  // no access token but refresh token exists, attempt to fetch a new access token.
  // race condition can happen where the access token which is just about to be expired,
  // gets validated here in the middleware but when access token is accessed afterwards,
  // the token is already expired.
  if (!accessToken && refreshToken) {
    const result = await fetchNewAccessToken(refreshToken);
    const res = NextResponse.next();

    if (result.success) {
      accessToken = result.accessToken;
      setAccessTokenCookie(res.cookies, accessToken);
    }
    return res;
  }

  // no access token and the requested url is a protected page, redirect to login page
  if (req.nextUrl.pathname.startsWith("/dashboard/") && !accessToken) {
    return NextResponse.redirect(new URL("/login", req.url));
  }

  return NextResponse.next();
}
// ewewewewewe
export const config = {
  // https://nextjs.org/docs/app/building-your-application/routing/middleware#matcher
  matcher: ["/((?!api|_next/static|_next/image|.*\\.png$).*)"],
};
