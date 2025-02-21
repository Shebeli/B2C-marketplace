import { phoneNumberValidator } from "@persian-tools/persian-tools";
import { usernamePattern } from "../constants";
import {
  CodeRequestInfo,
  ValidatedCodeRequestInfo,
} from "../actions/auth/verify/verifyPhone";

const codeLifespan = Number(process.env.CODE_LIFETIME);

export function isValidPhoneorUsername(input: string): boolean {
  const isPhone = phoneNumberValidator(input);
  const isUsername = usernamePattern.test(input);

  return isPhone || isUsername;
}

// formats inputted seconds to: minutes:seconds (e.g. 120 -> 02:00)
export const formatCooldownTime = (seconds: number): string => {
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = seconds % 60;
  return `${String(minutes).padStart(2, "0")}:${String(
    remainingSeconds
  ).padStart(2, "0")}`;
};

// For verifying the verify phone component session
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
