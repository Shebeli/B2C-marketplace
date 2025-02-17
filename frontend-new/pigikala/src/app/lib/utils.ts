import { phoneNumberValidator } from "@persian-tools/persian-tools";
import { usernamePattern } from "./constants";

export function isValidPhoneorUsername(input: string): boolean {
  const isPhone = phoneNumberValidator(input);
  const isUsername = usernamePattern.test(input);

  return isPhone || isUsername;
}
