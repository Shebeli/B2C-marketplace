"use server";

import { cookies } from "next/headers";

// const codeRequestCooldown = Number(process.env.CODE_REQUEST_COOLDOWN); // in minutes

export interface CodeRequestInfo {
  phone: string | undefined;
  requestTimestamp: number | undefined;
}

export interface ValidatedCodeRequestInfo {
  phone: string;
  requestTimestamp: number;
}

// retrieve requested code timestamp and inputted phone data from cookies
export async function getCodeRequestData(): Promise<CodeRequestInfo> {
  const cookieStore = await cookies();

  const requestTimestamp = Number(
    cookieStore.get("requestedCodeTimestamp")?.value
  );
  const phone = cookieStore.get("inputtedPhone")?.value;

  return { phone, requestTimestamp };
}

