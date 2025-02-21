import { getCodeRequestData } from "@/app/lib/actions/auth/verify/verifyPhone";
import VerifyPhoneClient from "@/app/ui/verify";
import { isCodeRequestValid } from "@/app/lib/utils/helpers";
import { calculateCodeRemainingTimer } from "@/app/lib/utils/time";

export default async function VerifyPhone() {
  const codeRequestData = await getCodeRequestData();

  // safeguarding against invalid session
  if (!isCodeRequestValid(codeRequestData)) {
    return (
      <div className="text-lg flex flex-col items-center">
        <p> زمان تایید تلفن منقضی شده است. </p>
        <p>
          {" "}
          می توانید{" "}
          <a className="link link-info" href="/auth/login">
            {" "}
            در این لینک
          </a>{" "}
          اقدام به ورود مجدد نمایید.
        </p>
      </div>
    );
  }

  return (
    <VerifyPhoneClient
      inputtedPhone={codeRequestData.phone}
      cooldownTimer={calculateCodeRemainingTimer(
        codeRequestData.requestTimestamp
      )} // should be in seconds
    />
  );
}
