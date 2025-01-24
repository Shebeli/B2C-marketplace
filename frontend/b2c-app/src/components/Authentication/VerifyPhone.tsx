import { useEffect, useRef, useState } from "react";
import { MainLogo } from "../../assets/MainLogo";
import { phoneNumberValidator } from "@persian-tools/persian-tools";

const VerifyPhone: React.FC = () => {
  const [submittedPhone, setSubmittedPhone] = useState<string | null>(null);
  const [isSessionValid, setSessionIsValid] = useState<boolean>(true);
  const [verificationCode, setVerificationCode] = useState<string[]>(
    Array(5).fill("")
  );
  const [isFormInvalid, setIsFormInvalid] = useState<boolean>(false);
  const inputsRef = useRef<HTMLInputElement[]>([]);

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>): void => {
    if (verificationCode.some((element) => element === "")) {
      e.preventDefault();
      setIsFormInvalid(true);
      return;
    }
    e.preventDefault();
    setIsFormInvalid(false);
    console.log(
      `Phone verification code form submitted: ${verificationCode.join("")}`
    );
  };

  const handleInputChange =
    (index: number) => (e: React.ChangeEvent<HTMLInputElement>) => {
      const newValue = e.target.value;
      if (newValue.length == 1 || newValue === "") {
        setVerificationCode((prev) =>
          prev.map((item, i) => (i === index ? newValue : item))
        );
        if (index < inputsRef.current.length - 1) {
          inputsRef.current[index + 1].focus();
        }
      }
    };

  useEffect(() => {
    const phone = localStorage.getItem("inputPhone");
    const phoneTimeStamp = localStorage.getItem("inputPhoneTimeStamp");
    if (!phoneTimeStamp) {
      setSessionIsValid(false);
      return;
    }
    if (phone) {
      // validate OTP's age.
      setSubmittedPhone(phone);
      const now = Date.now();
      const submittedTimeStamp = new Date(phoneTimeStamp).getTime();
      const codeExpiriation = 15 * 60 * 1000; // in milliseconds

      // is code expired
      if (now - submittedTimeStamp >= codeExpiriation) {
        setSessionIsValid(false);
        return;
      }
      // is phone valid
      if (!phoneNumberValidator(phone)) {
        setSessionIsValid(false);
        return;
      }
    }
  }, []);

  useEffect(() => {
    if (verificationCode.every((element) => element !== "") && !isFormInvalid) {
      const constructedCode = verificationCode.join("");
      console.log(
        `The code is constructed: ${constructedCode}, should be sent to server for verification.`
      );
    }
  }, [verificationCode, isFormInvalid]);

  return (
    <div className="p-6 rounded-xl border-2 flex flex-col  gap-3 shadow-sm">
      <a className="btn bg-base-100 border-0 self-center" href="/">
        <MainLogo width="120" />
      </a>

      {isSessionValid ? (
        <div className="flex flex-col gap-2 items-center text-lg">
          <p className="mb-2">
            {" "}
            لطفا کد تایید ارسال شده به شماره {submittedPhone} را وارد نمایید:
          </p>
          {isFormInvalid && (
            <p className="text-error font-medium">
              لطفا کد را بصورت کامل وارد نمایید
            </p>
          )}
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
                  className={`input input-bordered w-12 text-2xl ${
                    isFormInvalid ? "input-error" : ""
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
              className="btn btn-primary h-11 btn-sm mt-4 w-full  text-lg font-bold "
              type="submit"
            >
              تایید
            </button>
          </form>
        </div>
      ) : (
        <div className="text-lg flex flex-col items-center">
          <p> زمان هویت سنجی تلفن منقضی شده است. </p>
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
