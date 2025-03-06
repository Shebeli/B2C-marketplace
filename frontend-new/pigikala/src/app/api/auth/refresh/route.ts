import { cookies } from "next/headers";
import { NextResponse } from "next/server";
import { axiosInstance } from "@/app/lib/axiosInstance";
import { API_ROUTES } from "@/app/lib/apiRoutes";

const { REFRESH } = API_ROUTES.AUTH;

// for refreshing the access token using the backend server, Django.
export async function POST() {
  const cookieStore = await cookies();
  const refreshToken = cookieStore.get("refresh_token")?.value;

  if (!refreshToken) {
    return NextResponse.json(
      { error: "Refresh token missing" },
      { status: 401 }
    );
  }

  try {
    const response = await axiosInstance.post(REFRESH, {
      refresh: refreshToken,
    });
    const { access } = response.data;
    const res = NextResponse.json({});
    res.cookies.set("access_token", access, {
      httpOnly: true,
      path: "/",
      secure: process.env.NODE_ENV === "production",
      maxAge: Number(process.env.ACCESS_TOKEN_LIFETIME),
    });
    return res;
  } catch (error) {
    // refresh token is invalid/expired.
    console.error(error);
    return NextResponse.json(
      {
        error: "Failed to retrieve a new access token from the backend server.",
      },
      { status: 500 }
    );
  }
}
