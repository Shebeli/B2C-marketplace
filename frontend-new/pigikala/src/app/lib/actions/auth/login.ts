"use server";

import { requestVerificationCode } from "./requestNewCode";
import { redirect } from "next/navigation";
import { phoneNumberValidator } from "@persian-tools/persian-tools";
import { usernamePattern } from "../../constants/ui/general-constants";

// formErrors for client-side form errors
// alertError for server-side errors such as failed API fetch request
export type LoginState = {
  formError?: string | null;
  alertError?: string | null;
  prevInput?: string | undefined;
};

export async function processLoginInput(
  prevState: LoginState,
  formData: FormData
): Promise<LoginState> {
  const userInput = formData.get("loginInput")?.toString();
  if (!userInput) {
    return {
      formError: "لطفا شماره تلفن یا نام کاربری خود را وارد کنید.",
      prevInput: userInput,
    };
  }

  if (phoneNumberValidator(userInput)) {
    const error = await requestVerificationCode(userInput);
    if (error) {
      return {
        ...error,
        prevInput: userInput,
      };
    }
    redirect("/auth/verify");
  } else if (usernamePattern.test(userInput)) {
    redirect("/auth/login-with-password"); // username should also be passed, but how?
  } else {
    return {
      formError: "نام کاربری یا شماره تلفن وارد شده صحیح نمی باشد",
      prevInput: userInput,
    };
  }
}
