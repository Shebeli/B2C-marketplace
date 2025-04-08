import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";

const CODE_REQUEST_COOLDOWN = Number(process.env.CODE_REQUEST_COOLDOWN);

// caluclates the remaining timer for requesting another verification code,
// returns 0 if theres no remanining time.
export const calculateCodeRemainingTimer = (requestTimestamp: number) => {
  const now = Date.now();
  const elapsedTime = now - requestTimestamp; // in milliseconds
  // convert from minutes to milliseconds:
  const codeRequestCooldown = CODE_REQUEST_COOLDOWN * 60 * 1000;

  // If its less than two minutes since the code request, calculate the remaining timer.
  if (elapsedTime < codeRequestCooldown) {
    const timeDiff = codeRequestCooldown - elapsedTime;
    const remainingTimer = Math.floor(timeDiff / 1000);
    return remainingTimer; // in seconds
  }
  return 0;
};

export function toRelativePersianTime(date: string): string {
  dayjs.extend(relativeTime);
  dayjs.locale("fa");
  return dayjs().to(date);
}
