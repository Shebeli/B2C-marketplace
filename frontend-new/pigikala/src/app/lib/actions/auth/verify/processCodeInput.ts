import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import { revalidatePath } from "next/cache";
import { API_ROUTES } from "@/app/lib/drfRoutes";

// cache the result for better UX
async function handleErrorResponse(response: Response) {
  if (response?.status === 429) {
    if (response.headers.get("x-rate-limit-type") === "SMS_LIMIT") {
      const data = await response.json();
      if (data.cooldown_time) {
        return {
          alertError: `کد تایید ارسال شده است. ${data.cooldown_time} ثانیه دیگر تا امکان درخواست مجدد کد.`,
        };
      }
    } else {
      return {
        alertError: `درخواست بیش از حد مجاز. ${response.headers.get(
          "retry-after"
        )} ثانیه دیگر میتوانید درخواست کد کنید.`,
      };
    }
  } else if (response?.status === 400) {
    return { alertError: "فرمت تلفن وارد شده غلط می باشد." };
  } else {
    return { alertError: "یک خطای غیر منتظره پیش آمده. لطفا مجددا تلاش کنید." };
  }
}

async function handleSuccesfulResponse(response: Response): Promise<never> {
  const cookieStore = await cookies();

  const { access, refresh } = await response.json();
  cookieStore.set("refresh_token", refresh, {
    httpOnly: true,
    path: "/",
    secure: process.env.NODE_ENV === "production",
    maxAge: Number(process.env.REFRESH_TOKEN_LIFESPAN),
  });
  cookieStore.set("access_token", access, {
    httpOnly: true,
    path: "/",
    secure: process.env.NODE_ENV === "production",
    maxAge: Number(process.env.ACCESS_TOKEN_LIFESPAN),
  });

  revalidatePath("/");
  redirect("/");
}

function constructCode(formData: FormData) {
  // validate the digits and append them to the array.
  const verificationDigits = [];
  for (let i = 0; i < Number(process.env.OTPLength); i++) {
    const currDigit = formData.get(`digit_${i}`)?.toString();

    // validations
    if (!currDigit) return { formError: "لطفا کد را بصورت کامل وارد نمایید" };
    if (isNaN(Number(currDigit))) return { formError: "کد فقط باید عدد باشد." };

    verificationDigits.push(currDigit);
  }

  // construct the code
  return verificationDigits.join("");
}

export type CodeState = {
  formError?: string | null;
  alertError?: string | null;
};

const { USER } = API_ROUTES;

export async function processCodeInput(
  prevState: CodeState,
  formData: FormData,
  inputtedPhone: string
) {
  const verifyCode = constructCode(formData);
  try {
    const response = await fetch(USER.VERIFY_CODE, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        verification_code: verifyCode,
        phone: inputtedPhone,
      }),
    });

    if (response.ok) {
      handleSuccesfulResponse(response);
    }

    handleErrorResponse(response);
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
