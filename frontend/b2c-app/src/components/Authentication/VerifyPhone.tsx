import { useEffect, useState } from "react";
import { MainLogo } from "../../assets/MainLogo";
import { phoneNumberValidator } from "@persian-tools/persian-tools";

const VerifyPhone: React.FC = () => {
  const [submittedPhone, setSubmittedPhone] = useState<string | null>(null);
  const [isSessionValid, setSessionIsValid] = useState<boolean>(true);

  useEffect(() => {
    const phone = localStorage.getItem("inputPhone");
    const phoneTimeStamp = localStorage.getItem("inputPhoneTimeStamp");
    if (!phoneTimeStamp) {
      setSessionIsValid(false);
      return;
    }
    if (phone) {
      // validate OTP's age.
      setSubmittedPhone(submittedPhone);
      const now = Date.now();
      const tenMinutes = 10 * 60 * 1000; // in milliseconds
      const submittedTimeStamp = new Date(phoneTimeStamp);

      if (now - submittedTimeStamp.getTime() >= tenMinutes) {
        setSessionIsValid(false);
      }
      if (!phoneNumberValidator(submittedPhone)) {
        setSessionIsValid(false);
      }
    }
  }, []);

  return (
    <div className="p-6 rounded-xl border-2 flex flex-col  gap-3 shadow-sm">
      <a className="btn bg-base-100 border-0 self-center" href="/">
        <MainLogo width="120" />
      </a>

      {isSessionValid ? (
        <div>
          <p> لطفا کد تایید ارسال به شماره را وارد نمایید: {submittedPhone}</p>
          <button className="btn btn-primary self-center h-11 btn-sm mt-4 w-full  text-lg font-bold">
            تایید
          </button>
        </div>
      ) : (
        <p className="text-sm text-error font-bold">
          زمان هویت سنجی تلفن وارد شده منقضی شده است. لطفا مجددا شماره تلفن خود
          را در
          <a className="link" href="/login">
            این لینک
          </a>
          وارد نمایید
        </p>
      )}
    </div>
  );
};

export default VerifyPhone;
