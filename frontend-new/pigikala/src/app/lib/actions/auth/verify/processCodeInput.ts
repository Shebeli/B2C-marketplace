"use server";

import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import { revalidatePath } from "next/cache";
import { API_ROUTES } from "@/app/lib/drfRoutes";
import {
  setAccessTokenCookie,
  setRefreshTokenCookie,
} from "@/app/lib/utils/fetch";

export type CodeState = {
  formError?: string | null;
  alertError?: string | null;
  prevInput?: FormData | undefined;
  throttleCooldownTimer?: number;
};

const { USER } = API_ROUTES;

export async function processVerifyCode(
  phone: string,
  prevState: CodeState,
  formData: FormData
): Promise<CodeState> {
  let verifyCode;

  try {
    verifyCode = constructCode(formData);
  } catch (error) {
    const err = error as Error;
    return { formError: err.message };
  }

  try {
    const url = new URL(USER.VERIFY_CODE, process.env.API_BASE_URL);
    const response = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        verification_code: verifyCode,
        phone: phone,
      }),
    });

    // redirects
    if (response.ok) {
      return handleSuccesfulResponse(response);
    }

    return handleErrorResponse(response);
  } catch (error) {
    console.error(
      "An unexpected error has occured when posting verify code:",
      error
    );
    return {
      alertError: "یک خطای غیر منتظره پیش آمده است, لطفا مجددا تلاش کنید.",
    };
  }
}

// Should update the related cooldown timers
async function handleErrorResponse(response: Response): Promise<CodeState> {
  if (response?.status === 429) {
    if (response.headers.get("x-rate-limit-type") === "SMS_LIMIT") {
      const data = await response.json();
      if (data.cooldown_time) {
        return {
          alertError: `کد تایید ارسال شده است. ${data.cooldown_time} ثانیه دیگر تا امکان درخواست مجدد کد.`,
        };
      } else {
        return {
          alertError: "زمان درخواست کد مشخص نیست, لطفا لحظاتی بعد تلاش کنید.",
        };
      }
    } else {
      const throttleCooldownTimer = response.headers.get("retry-after");
      return {
        alertError: `ثبت بیش از حد مجاز, ${throttleCooldownTimer} ثانیه دیگر میتوانید ثبت کد کنید.`,
        throttleCooldownTimer: Number(throttleCooldownTimer),
      };
    }
  } else if (response?.status === 400) {
    return { alertError: "کد وارد شده غلط می باشد." };
  } else {
    return { alertError: "یک خطای غیر منتظره پیش آمده. لطفا مجددا تلاش کنید." };
  }
}

async function handleSuccesfulResponse(response: Response): Promise<never> {
  const cookieStore = await cookies();
  const { access, refresh } = await response.json();

  setRefreshTokenCookie(cookieStore, refresh);
  setAccessTokenCookie(cookieStore, access);

  revalidatePath("/");
  redirect("/");
}

// constructs the digits using the formData
function constructCode(formData: FormData) {
  // validate the digits and append them to the array.
  const verificationDigits = [];
  // 5 for OTP length, should be set env variable instead
  for (let i = 0; i < 5; i++) {
    const currDigit = formData.get(`digit_${i}`)?.toString();

    // validations
    if (!currDigit) throw new Error("لطفا کد را بصورت کامل وارد نمایید");
    if (isNaN(Number(currDigit))) throw new Error("کد فقط باید عدد باشد.");

    verificationDigits.push(currDigit);
  }

  return verificationDigits.join("");
}
