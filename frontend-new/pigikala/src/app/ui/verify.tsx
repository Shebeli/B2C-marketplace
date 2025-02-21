"use client";

import { useState, useEffect, useRef } from "react";
import { CodeState } from "../lib/actions/auth/verify/processCodeInput";
import { processVerifyCode } from "../lib/actions/auth/verify/processCodeInput";
import { useActionState } from "react";
import { MainLogo } from "../assets/MainLogo";
import TemporaryAlert from "./alert/alert";
import { formatCooldownTime } from "../lib/utils/helpers";
import { requestVerificationCode } from "../lib/actions/auth/requestNewCode";
import { alertTypes } from "../lib/constants";

interface VerifyPhoneProps {
  inputtedPhone: string;
  cooldownTimer: number;
}

interface AlertData {
  msg: string;
  type: (typeof alertTypes)[number];
}

const CODE_REQUEST_COOLDOWN = Number(process.env.CODE_REQUEST_COOLDOWN);

export default function VerifyPhoneClient({
  inputtedPhone,
  cooldownTimer,
}: VerifyPhoneProps) {
  const [requestCooldownTimer, setRequestCooldownTimer] =
    useState<number>(cooldownTimer); // in seconds
  const [throttleCooldownTimer, setThrottleCooldownTimer] = useState<number>(0); // in seconds
  const [verificationDigits, setVerificationDigits] = useState<string[]>(
    Array(5).fill("")
  );
  const inputsRef = useRef<HTMLInputElement[]>([]);
  const formRef = useRef<HTMLFormElement>(null);
  const [alert, setAlert] = useState<AlertData | null>(null);

  // form action
  const initialState: CodeState = { formError: null, alertError: null };
  const processCodeInputWithPhone = processVerifyCode.bind(null, inputtedPhone);
  const [state, formAction, pending] = useActionState(
    processCodeInputWithPhone,
    initialState
  );

  const handleNewCodeRequest = async () => {
    // note that on succesful request, function requestVerificationCode WILL
    // update the cookies with the new code request timestamp.

    const result = await requestVerificationCode(inputtedPhone);
    if (result?.alertError) {
      setAlert({ msg: result.alertError, type: "error" });
      return;
    }
    // set the cooldown timer
    setRequestCooldownTimer(CODE_REQUEST_COOLDOWN * 60);
    setAlert({
      msg: "کد مجددا با موفقیت به شماره تلفن وارد شده ارسال شد.",
      type: "info",
    });
  };

  // changes the focus to next field once a field has been inputted.
  // Also update the verificationDigits on change.
  const handleInputChange =
    (index: number) => (e: React.ChangeEvent<HTMLInputElement>) => {
      // change the focus to the next field if its not the last index and a value has been inputted
      if (index < inputsRef.current.length - 1 && e.target.value !== "") {
        inputsRef.current[index + 1].focus();
      }

      // update the verificationDigits state
      if (e.target.value !== "") {
        setVerificationDigits(
          verificationDigits.map((prev, i) =>
            i === index ? e.target.value : prev
          )
        );
      }
    };

  // Timer for code request cooldown
  useEffect(() => {
    if (requestCooldownTimer === 0) return;
    const timer = setInterval(
      () => setRequestCooldownTimer((prev) => prev - 1),
      1000
    );
    return () => clearInterval(timer);
  }, [requestCooldownTimer]);

  // Timer for throttle cooldown
  useEffect(() => {
    if (throttleCooldownTimer === 0) return;
    const timer = setInterval(
      () => setThrottleCooldownTimer((prev) => prev - 1),
      1000
    );
    return () => clearInterval(timer);
  }, [throttleCooldownTimer]);

  // If verification digits fields are fully inputted and there
  // are no form errors, submit the form.
  useEffect(() => {
    if (
      verificationDigits.every((element) => element !== "") &&
      !state.formError
    ) {
      formRef.current?.submit();
    }
  }, [state.formError, verificationDigits]);

  return (
    <div>
      {state.alertError && (
        <TemporaryAlert
          message={state.alertError}
          type="error"
          duration={5000}
        />
      )}
      {alert && (
        <TemporaryAlert message={alert.msg} type={alert.type} duration={5000} />
      )}
      <div className="flex flex-col gap-2 items-center">
        <p className="mb-2">
          {" "}
          لطفا کد ارسال شده به شماره {inputtedPhone} را وارد نمایید
        </p>
        {state.formError && (
          <p className="text-error font-medium">{state.formError}</p>
        )}
        <form
          ref={formRef}
          className="flex flex-col items-center"
          action={formAction}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              (e.currentTarget as HTMLFormElement).submit();
            }
          }}
        >
          <div className="flex gap-1.5 flex-row-reverse">
            {Array.from({ length: 5 }, (_, index) => (
              <input
                key={index}
                type="text"
                id={`digit_${index}`}
                maxLength={1}
                ref={(element) => {
                  inputsRef.current[index] = element!;
                }}
                onChange={handleInputChange(index)}
                className={`input input-bordered input-info w-12 text-2xl ${
                  state.formError ? "input-error" : ""
                }`}
                inputMode="numeric"
                pattern="[0-9]*"
                onKeyDown={(e) => {
                  if (e.key === "Tab" || e.key === "Shift") {
                    return;
                  }
                  if (e.key === "Backspace") {
                    return;
                  }
                  if (!/^\d$/.test(e.key)) {
                    e.preventDefault();
                  }
                }}
              ></input>
            ))}
          </div>
          <button
            className={`btn btn-primary h-11 btn-sm mt-4 w-full text-lg font-bold ${
              pending || throttleCooldownTimer !== 0 ? "btn-disabled" : ""
            }`}
            type="submit"
          >
            {throttleCooldownTimer === 0
              ? "تایید"
              : `امکان ثبت در ${throttleCooldownTimer}`}
          </button>
          {requestCooldownTimer !== 0 ? (
            <p className="text-sm mt-2">
              {formatCooldownTime(requestCooldownTimer)} تا امکان درخواست کد
              مجدد
            </p>
          ) : (
            <a
              className={`text-sm mt-2 link link-info ${
                pending ? "cursor-not-allowed" : ""
              }`}
              onClick={(e) => {
                if (pending) {
                  e.preventDefault();
                  return;
                }
                handleNewCodeRequest();
              }}
            >
              درخواست کد مجدد
            </a>
          )}
        </form>
      </div>
    </div>
  );
}
