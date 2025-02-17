"use server";

import { cookies } from "next/headers";
import { phoneNumberValidator } from "@persian-tools/persian-tools";
import { API_ROUTES } from "../../../drfRoutes";
import { redirect } from "next/navigation";
import { revalidatePath } from "next/cache";

// const codeRequestCooldown = Number(process.env.CODE_REQUEST_COOLDOWN); // in minutes
const codeLifespan = Number(process.env.CODE_LIFESPAN); // in minutes
const { USER } = API_ROUTES;

export interface CodeRequestInfo {
  phone: string | undefined;
  requestTimestamp: number | undefined;
}

export interface ValidatedCodeRequestInfo {
  phone: string;
  requestTimestamp: number;
}

// get requested code timestamp and inputted phone data from cookies
export async function getCodeRequestData(): Promise<CodeRequestInfo> {
  const cookieStore = await cookies();

  const requestTimestamp = Number(
    cookieStore.get("requestedCodeTimestamp")?.value
  );
  const phone = cookieStore.get("inputtedPhone")?.value;

  return { phone, requestTimestamp };
}

// For verifying the verify-phone component session
export function isCodeRequestValid(
  codeRequestData: CodeRequestInfo
): codeRequestData is ValidatedCodeRequestInfo {
  const { requestTimestamp, phone } = codeRequestData;

  if (!requestTimestamp || !phone) {
    return false;
  }
  // is phone valid
  if (!phoneNumberValidator(phone)) {
    return false;
  }

  // validate requested code's lifespan.
  const now = Date.now();
  const submittedCodeTimestamp = new Date(requestTimestamp).getTime();
  const elapsedTime = now - submittedCodeTimestamp;

  // if elapsed time is shorter than code, then the code request is still valid
  return elapsedTime <= codeLifespan * 60 * 1000;
}

