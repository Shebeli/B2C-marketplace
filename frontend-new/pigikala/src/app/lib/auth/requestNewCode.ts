"use server";

import { redirect } from "next/navigation";
import { cookies } from "next/headers";
import { API_ROUTES } from "../apiRoutes";
import { CodeState } from "./verify/processCodeInput";

const { USER: USER_ENDPOINTS } = API_ROUTES;
const codeRequestCooldown = Number(process.env.CODE_REQUEST_COOLDOWN); // in minutes
const CODE_LIFESPAN = Number(process.env.CODE_LIFETIME); // in minutes

// on void return type, it means the request was succesful
// on CodeState return type, it means that there was an issue requesting the code
export async function requestVerificationCode(
  phone: string
): Promise<CodeState | void> {
  const cookieStore = await cookies();

  try {
    const url = new URL(USER_ENDPOINTS.LOGIN, process.env.API_BASE_URL);
    const response = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ phone }),
    });

    if (response.ok) {
      return handleSuccesfulRequest(phone, cookieStore);
    }

    // if the response failed due to rate limiting,it means somehow the code request cooldown
    // tracker cookie does not exist, so update the cookieStore with remaining cooldown
    if (response.status === 429) {
      if (response.headers.get("x-rate-limit-type") === "SMS_LIMIT") {
        return handleRateLimit(response, phone, cookieStore);
      } else {
        // throttled
        return {
          alertError: "درخواست بیش از حد مجاز. لحظاتی بعد تلاش کنید.",
        };
      }
    } else {
      console.error("Unexpected OTP request error:", response);
      return {
        alertError: "یک خطلای غیر منتظره پیش آمده, لطفا بعدا تلاش کنید.",
      };
    }
  } catch (error) {
    console.error("Unexpected OTP error:", error);
    return { alertError: "یک خطای غیر منتظره پیش آمده, لطفا بعدا تلاش کنید." };
  }
}

// for adding new cookies tracking the code submition
async function handleSuccesfulRequest(
  phone: string,
  cookieStore: Awaited<ReturnType<typeof cookies>>
) {
  const nowTimestamp = Date.now();

  cookieStore.set("requestedCodeTimestamp", String(nowTimestamp), {
    maxAge: CODE_LIFESPAN * 60,
    httpOnly: true,
  });
  cookieStore.set("inputtedPhone", phone, {
    maxAge: CODE_LIFESPAN * 60,
    httpOnly: true,
  });
}

// Add cookies for tracking the rate limit, and redirect to verify page
async function handleRateLimit(
  response: Response,
  phone: string,
  cookieStore: Awaited<ReturnType<typeof cookies>>
) {
  const now = Date.now();
  const { cooldownTime } = await response.json(); // in seconds
  const requestTimestamp =
    now - (codeRequestCooldown * 60 - cooldownTime) * 1000;

  cookieStore.set("requestedCodeTimestamp", String(requestTimestamp), {
    maxAge: cooldownTime,
    httpOnly: true,
  });
  cookieStore.set("inputtedPhone", phone, {
    maxAge: cooldownTime,
    httpOnly: true,
  });

  redirect("/auth/verify");
}
