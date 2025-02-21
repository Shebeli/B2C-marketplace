"use server";

import { cookies } from "next/headers";
import { phoneNumberValidator } from "@persian-tools/persian-tools";

// const codeRequestCooldown = Number(process.env.CODE_REQUEST_COOLDOWN); // in minutes
const codeLifespan = Number(process.env.CODE_LIFESPAN); // in minutes

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

