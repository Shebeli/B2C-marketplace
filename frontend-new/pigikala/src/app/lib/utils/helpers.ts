import { phoneNumberValidator } from "@persian-tools/persian-tools";
import { usernamePattern } from "../constants";
import {
  CodeRequestInfo,
  ValidatedCodeRequestInfo,
} from "../actions/auth/verify/verifyPhone";
import { startTransition } from "react";

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

// validate if the code request is expired or not
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

  // (theoritically these lines shouldn't exectute since the cookies
  // should expire due to max age of the phone and requestTimestamp cookies
  // being set to env variable CODE_LIFESPAN, and thus variables 'requestTimestamp'
  // and 'phone' should be undefined if they are expired)
  const now = Date.now();
  const submittedCodeTimestamp = new Date(requestTimestamp).getTime();
  const elapsedTime = now - submittedCodeTimestamp;

  // convert to milliseconds
  const codeLifespan = Number(process.env.CODE_LIFETIME) * 60 * 1000;
  // if elapsed time is shorter than code, then the code request is still valid
  return elapsedTime <= codeLifespan;
}

// to prevent the fields getting reset upon submitting a form, use this event handler
// instead of passing the actionForm to form, pass this action to event listener "onSubmit"
export const handleFormSubmit =
  (formAction: (formData: FormData) => void) =>
  (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    startTransition(() => formAction(formData));
  };
