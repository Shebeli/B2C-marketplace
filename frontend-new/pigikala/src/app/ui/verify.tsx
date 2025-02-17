"use client";
import { useState, useEffect } from "react";

interface VerifyPhoneProps {
  phone: string;
  requestTimestamp: number;
  cooldownTimer: number | undefined;
}

const codeRequestCooldown = Number(process.env.CODE_REQUEST_COOLDOWN); // in minutes
const codeLifespan = Number(process.env.CODE_LIFESPAN); // in minutes

export default function VerifyPhoneClient({
  phone,
  requestTimeStamp,
  cooldownTimer,
}: VerifyPhoneProps) {
  const [requestCooldownTimer, setRequestCooldownTimer] = useState<number>(0); // in seconds
  const [throttleCooldownTimer, setThrottleCooldownTimer] = useState<number>(0); // in seconds

  // Tick tock for code request cooldown
  useEffect(() => {
    if (requestCooldownTimer === 0) return;
    const timer = setInterval(() =>
      setRequestCooldownTimer((prev) => prev - 1)
    );
    return () => clearInterval(timer);
  }, [requestCooldownTimer]);

  // Tick tock for throttle cooldown
  useEffect(() => {
    if (throttleCooldownTimer === 0) return;
    const timer = setInterval(() =>
      setRequestCooldownTimer((prev) => prev - 1)
    );
    return () => clearInterval(timer);
  }, [throttleCooldownTimer]);

  return (
    <div className="p-6 rounded-xl border-[2.5px] border-base-300 flex flex-col  gap-3 shadow-sm">
      {alertMsg && (
        <TemporaryAlert
          message={alertMsg.message}
          type={alertMsg.type}
          duration={5000}
        />
      )}

      <a className="btn bg-base-100 border-0 self-center" href="/">
        <MainLogo width="120" />
      </a>

      {isSessionValid ? (
        <div className="flex flex-col gap-2 items-center">
          <p className="mb-2">
            {" "}
            لطفا کد تایید ارسال شده به شماره {submittedPhone} را وارد نمایید
          </p>
          {formError && <p className="text-error font-medium">{formError}</p>}
          <form
            className="flex flex-col items-center"
            onSubmit={handleSubmit}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                e.preventDefault();
                handleSubmit(e as unknown as React.FormEvent<HTMLFormElement>);
              }
            }}
          >
            <div className="flex gap-1.5 flex-row-reverse">
              {Array.from({ length: 5 }, (_, index) => (
                <input
                  key={index}
                  type="text"
                  maxLength={1}
                  ref={(element) => (inputsRef.current[index] = element!)}
                  onChange={handleInputChange(index)}
                  className={`input input-bordered input-info w-12 text-2xl ${
                    formError ? "input-error" : ""
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
                isLoading || throttleCooldownTimer !== 0 ? "btn-disabled" : ""
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
                  isLoading ? "cursor-not-allowed" : ""
                }`}
                onClick={(e) => {
                  if (isLoading) {
                    e.preventDefault();
                    return;
                  }
                  handleCodeRequest(e);
                }}
              >
                درخواست کد مجدد
              </a>
            )}
          </form>
        </div>
      ) : (
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
      )}
    </div>
  );
}
