// "use client";

import { useRef, useState, useEffect } from "react";
import {
  isCodeRequestValid,
  getCodeRequestData,
} from "@/app/lib/actions/auth/verify/verifyPhone";
import VerifyPhoneClient from "@/app/ui/verify";

const codeRequestCooldown = Number(process.env.VITE_CODE_REQUEST_COOLDOWN); // in minutes
const codeLifespan = process.env.VITE_CODE_LIFESPAN; // in minutes

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
          <a className="link link-info" href="/login">
            {" "}
            در این لینک
          </a>{" "}
          اقدام به ورود مجدد نمایید.
        </p>
      </div>
    );
  }

  const initialState: LoginState = { formError: null, alertError: null };
  const [state, formAction, pending] = useActionState(
    processLoginInput,
    initialState
  );
  
  // const [requestedCodeTimestamp, setRequestedCodeTimestamp] = use;
  const [verificationDigits, setVerificationDigits] = useState<string[]>;
  const [requestCooldownTimer, setRequestCooldownTimer] = useState<number>(0); // in seconds
  const [throttleCooldownTimer, setThrottleCooldownTimer] = useState<number>(0); // in seconds

  const now = Date.now();
  const elapsedTime = now - codeRequestData.requestTimestamp;
  // If its less than two minutes since the code request, set a new cooldown timer
  let newCooldownTimer;
  if (elapsedTime < codeRequestCooldown * 60 * 1000) {
    const newRequestCooldownTimer =
      codeRequestCooldown * 60 * 1000 - elapsedTime;
    newCooldownTimer = Math.floor(newRequestCooldownTimer / 1000);
  }

  return (
    <VerifyPhoneClient
      phone={codeRequestData.phone}
      requestTimestamp={codeRequestData.requestTimestamp}
      cooldownTimer={newCooldownTimer}
    />
  );
}
