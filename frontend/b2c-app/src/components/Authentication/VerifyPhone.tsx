import { useEffect, useRef, useState, useCallback, useMemo } from "react";
import { MainLogo } from "../../assets/MainLogo";
import { phoneNumberValidator } from "@persian-tools/persian-tools";
import { useNavigate } from "react-router-dom";
import { AxiosError, isAxiosError } from "axios";
import { axiosInstance, setAuthToken } from "../../axiosInstance";
import { formatCooldownTime } from "./utils";
import TemporaryAlert from "../TemporaryAlert";
import { Alert, alertTypes } from "../alertConstants";

interface ErrorSMSLimitResponse {
  cooldown_time?: number;
}

const codeRequestCooldown = import.meta.env.VITE_CODE_REQUEST_COOLDOWN; // in minutes
const codeLifespan = import.meta.env.VITE_CODE_LIFESPAN; // in minutes

const VerifyPhone: React.FC = () => {
  const navigate = useNavigate();

  const submittedPhone = useMemo(() => {
    const phone = localStorage.getItem("inputtedPhone");
    return phone ? phone : null;
  }, []);
  const [requestedCodeTimestamp, setRequestedCodeTimestamp] = useState<
    number | null
  >(() => {
    const timeStamp = Number(localStorage.getItem("requestedCodeTimestamp"));
    return timeStamp ? timeStamp : null;
  });

  const [throttleCooldownTimer, setThrottleCooldownTimer] = useState<number>(0);
  const [requestCooldownTimer, setRequestCooldownTimer] = useState<number>(0); // In seconds
  const [isSessionValid, setSessionIsValid] = useState<boolean>(true);
  const [verificationCode, setVerificationCode] = useState<string[]>(
    Array(5).fill("")
  );
  const [isLoading, setIsLoading] = useState(false);
  const [alertMsg, setAlert] = useState<Alert | null>(null);
  const [formError, setFormError] = useState<string | null>(null);
  const inputsRef = useRef<HTMLInputElement[]>([]);

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>): void => {
    setIsLoading(true);
    setFormError(null);
    if (verificationCode.some((element) => element === "")) {
      e.preventDefault();
      setFormError("لطفا کد را بصورت کامل وارد نمایید.");
      setIsLoading(false);
      return;
    }
    e.preventDefault();
    // setFormError("لطفا کد را بصورت کامل وارد نمایید.");
    sendCodeForVerification(verificationCode.join(""));
  };

  const handleInputChange =
    (index: number) => (e: React.ChangeEvent<HTMLInputElement>) => {
      const newValue = e.target.value;
      if (newValue.length == 1 || newValue === "") {
        setVerificationCode((prev) =>
          prev.map((item, i) => (i === index ? newValue : item))
        );
        if (index < inputsRef.current.length - 1 && e.target.value !== "") {
          console.log(e.target.value);
          inputsRef.current[index + 1].focus();
        }
      }
    };

  const handleCodeRequest = (e: React.MouseEvent<HTMLAnchorElement>): void => {
    e.preventDefault();
    setIsLoading(true);
    requestNewCode(submittedPhone!);
  };

  const updateAlert = (message: string, type: (typeof alertTypes)[number]) => {
    setAlert(null);
    setTimeout(() => setAlert({ message, type }), 0);
  };

  const handleCodeRequestError = (error: AxiosError) => {
    if (error.response?.status === 429) {
      if (error.response.headers["x-rate-limit-type"] === "SMS_LIMIT") {
        const data = error.response.data as ErrorSMSLimitResponse;
        if (data.cooldown_time) {
          updateAlert(
            `کد تایید ارسال شده است. ${data.cooldown_time} ثانیه دیگر تا امکان درخواست مجدد کد.`,
            "error"
          );
        }
      } else {
        updateAlert(
          `درخواست بیش از حد مجاز. ${error.response.headers["retry-after"]} ثانیه دیگر میتوانید درخواست کد کنید.`,
          "error"
        );
      }
    } else if (error.response?.status === 400) {
      updateAlert("فرمت تلفن وارد شده غلط می باشد.", "error");
    } else {
      updateAlert(
        "یک خطای غیر منتظره پیش آمده. لطفا مجددا تلاش کنید.",
        "error"
      );
    }
  };

  const requestNewCode = async (phone: string): Promise<void> => {
    try {
      await axiosInstance.post("api/user/login/request_code/", {
        phone,
      });
      const nowTimestamp = Date.now();
      setRequestedCodeTimestamp(nowTimestamp);
      localStorage.setItem("requestedCodeTimestamp", String(Date.now()));
    } catch (error) {
      if (isAxiosError(error)) {
        handleCodeRequestError(error);
      }
    } finally {
      setIsLoading(false);
    }
  };

  const sendCodeForVerification = useCallback(
    async (code: string): Promise<void> => {
      try {
        const response = await axiosInstance.post(
          "api/user/login/verify_code/",
          {
            phone: submittedPhone,
            verification_code: code,
          }
        );
        const { access, refresh } = response.data;

        localStorage.setItem("access_token", access);
        localStorage.setItem("refresh_token", refresh);
        localStorage.removeItem("inputtedPhone");
        localStorage.removeItem("requestedCodeTimestamp");
        setAuthToken(access);
        navigate("/");
      } catch (error) {
        if (isAxiosError(error)) {
          if (error.response?.status == 400) {
            setFormError("کد وارد شده غلط می باشد");
          } else if (error.response?.status == 429) {
            updateAlert(
              `درخواست بیش از حد مجاز. ${error.response.headers["retry-after"]} ثانیه دیگر میتوانید ثبت کد کنید.`,
              "error"
            );
            setThrottleCooldownTimer(Number(error.response.headers["retry-after"]));
          } else {
            updateAlert(
              "یک خطای غیر منتظره پیش آمده, لطفا مجددا تلاش کنید.",
              "error"
            );
          }
        } else {
          updateAlert(
            "یک خطای غیر منتظره پیش آمده, لطفا مجددا تلاش کنید.",
            "error"
          );
        }
      } finally {
        setIsLoading(false);
      }
    },
    [submittedPhone, navigate]
  );

  // Check if the location states are valid
  useEffect(() => {
    if (!requestedCodeTimestamp || !submittedPhone) {
      setSessionIsValid(false);
      return;
    }
    // is phone valid
    if (!phoneNumberValidator(submittedPhone)) {
      setSessionIsValid(false);
      return;
    }

    // validate requested code's lifespan.
    const now = Date.now();
    const submittedCodeTimestamp = new Date(requestedCodeTimestamp).getTime();
    const timeDiff = now - submittedCodeTimestamp;
    if (timeDiff > codeLifespan * 60 * 1000) {
      setSessionIsValid(false);
      return;
    }
  }, [submittedPhone, requestedCodeTimestamp]);

  // Tick tock for code request cooldown
  useEffect(() => {
    let timer: ReturnType<typeof setInterval>;
    if (requestCooldownTimer > 0) {
      timer = setInterval(
        () => setRequestCooldownTimer((prev) => prev - 1),
        1000
      );
    }

    return () => clearInterval(timer);
  }, [requestCooldownTimer]);

  // Tick tock for throttle cooldown
  useEffect(() => {
    let timer: ReturnType<typeof setInterval>;
    if (throttleCooldownTimer > 0) {
      timer = setInterval(
        () => setThrottleCooldownTimer((prev) => prev - 1),
        1000
      );
    }
    return () => clearInterval(timer);
  }, [throttleCooldownTimer]);

  // Calculate and set code request cooldown time
  useEffect(() => {
    if (requestCooldownTimer !== 0) {
      return;
    }
    const now = Date.now();
    const timeDiff = now - requestedCodeTimestamp!;
    // If its less than two minutes since the code request, set the timer
    if (timeDiff < codeRequestCooldown * 60 * 1000) {
      const newRequestCooldownTimer =
        codeRequestCooldown * 60 * 1000 - timeDiff;
      setRequestCooldownTimer(Math.floor(newRequestCooldownTimer / 1000));
    }
  }, [requestCooldownTimer, requestedCodeTimestamp]);

  // Try to submit the code automatically when all the inputs are filled and theres no form errors.
  useEffect(() => {
    if (verificationCode.every((element) => element !== "") && !formError) {
      const code = verificationCode.join("");
      sendCodeForVerification(code);
    }
  }, [verificationCode, formError, sendCodeForVerification]);

  return (
    <div className="p-6 rounded-xl border-2 flex flex-col  gap-3 shadow-sm">
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
};

export default VerifyPhone;
