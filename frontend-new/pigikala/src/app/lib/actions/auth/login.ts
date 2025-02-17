"use server";

import { cookies } from "next/headers";
import { API_ROUTES } from "../../drfRoutes";
import { redirect } from "next/navigation";
import { phoneNumberValidator } from "@persian-tools/persian-tools";
import { usernamePattern } from "../../constants";

const { USER: USER_ENDPOINTS } = API_ROUTES;
const codeRequestCooldown = Number(process.env.CODE_REQUEST_COOLDOWN); // in minutes

// formErrors for client-side errors
// alertError for server-side errors such as failed API fetch request
export type LoginState = {
  formError?: string | null;
  alertError?: string | null;
};

export async function processLoginInput(
  prevState: LoginState,
  formData: FormData
) {
  const userInput = formData.get("loginInput")?.toString();
  if (!userInput) {
    return {
      formError: "لطفا شماره تلفن یا نام کاربری خود را وارد کنید.",
      alertError: null,
    };
  }

  if (phoneNumberValidator(userInput)) {
    const alertError = await requestVerificationCode(userInput);
    if (alertError) {
      const error = {
        ...alertError,
        formError: null,
      };
      return error;
    }
    redirect("/auth/verify-phone");
  } else if (usernamePattern.test(userInput)) {
    redirect("/auth/login-with-password"); // username should also be passed, but how?
  } else {
    return {
      formError: "نام کاربری یا شماره تلفن وارد شده صحیح نمی باشد",
      alertError: null,
    };
  }
}

export async function requestVerificationCode(phone: string) {
  const cookieStore = await cookies();

  try {
    const response = await fetch(USER_ENDPOINTS.LOGIN, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ phone }),
    });

    if (response.ok) {
      return handleSuccesfulRequest(phone, cookieStore);
    }

    // if the response failed due to rate limiting, somehow the code request cooldown
    // tracker was removed from the cookie, so update the cookie with remaining cooldown
    if (response.status === 429) {
      if (response.headers.get("x-rate-limit-type") === "SMS_LIMIT") {
        return handleRateLimit(response, phone, cookieStore);
      } else {
        // throttled
        return {
          alertError: `درخواست بیش از حد مجاز. ${response.headers.get(
            "retry-after"
          )} ثانیه دیگر میتوانید درخواست کد کنید.`,
        };
      }
    } else {
      console.error("Unexpected OTP request error:", response);
      return { alertError: "یک خطای غیر منتظره پیش آمده" };
    }
  } catch (error) {
    console.error("Unexpected OTP error:", error);
    return { alertError: "یک خطای غیر منتظره پیش آمده" };
  }
}

async function handleSuccesfulRequest(
  phone: string,
  cookieStore: Awaited<ReturnType<typeof cookies>>
) {
  const nowTimestamp = Date.now();
  cookieStore.set("requestedTimestamp", String(nowTimestamp), {
    maxAge: codeRequestCooldown * 60,
    httpOnly: true,
  });
  cookieStore.set("inputtedPhone", phone, {
    maxAge: codeRequestCooldown * 60,
    httpOnly: true,
  });
}

// response status is 429 and SMS_RATE_LIMIT is present in the headers
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
}
