import { phoneNumberValidator } from "@persian-tools/persian-tools";
import { MainLogo } from "../../assets/MainLogo";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import { axiosInstance } from "../../axiosInstance";
import TemporaryAlert from "../TemporaryAlert";
import { isAxiosError } from "axios";

const codeRequestCooldown = import.meta.env.VITE_CODE_REQUEST_COOLDOWN; // in minutes

const Login: React.FC = () => {
  const navigate = useNavigate();
  const usernamePattern = /^(?=[a-zA-Z])(?=(?:[^a-zA-Z]*[a-zA-Z]){3})\w{4,}$/;
  const [alertMsg, setAlertMsg] = useState<string | null>(null);
  const [isInputInvalid, setIsInputInvalid] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState(false);

  const requestVerificationCode = async (phone: string): Promise<void> => {
    try {
      await axiosInstance.post("api/user/login/request_code/", {
        phone,
      });
      const nowTimestamp = new Date().getTime();
      localStorage.setItem("requestedCodeTimestamp", String(nowTimestamp));
      localStorage.setItem("inputtedPhone", phone);
      navigate("/verify-phone");
    } catch (error) {
      if (isAxiosError(error)) {
        if (error.response?.status === 429) {
          if (error.response.headers["x-rate-limit-type"] === "SMS_LIMIT") {
            const now = Date.now();
            const cooldownTime = error.response.data["cooldown_time"];
            const requestTimestamp =
              now - (codeRequestCooldown * 60 - cooldownTime) * 1000;
            localStorage.setItem(
              "requestedCodeTimestamp",
              String(requestTimestamp)
            );
            localStorage.setItem("inputtedPhone", phone);
            navigate("/verify-phone");
          } else {
            setAlertMsg(
              `درخواست بیش از حد مجاز. ${error.response.headers["retry-after"]} ثانیه دیگر میتوانید درخواست کد کنید.`
            );
          }
        } else if (error.response?.status === 400) {
          setAlertMsg("فرمت تلفن وارد شده غلط می باشد.");
        } else {
          setAlertMsg("یک خطای غیر منتظره پیش آمده, لطفا مجددا تلاش کنید.");
        }
      } else {
        setAlertMsg("یک خطای غیر منتظره پیش آمده, لطفا مجددا تلاش کنید.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleUsernameSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    setAlertMsg(null);
    setIsLoading(true);
    event.preventDefault();

    const userInput = (event.currentTarget.userInput as HTMLInputElement).value;
    if (phoneNumberValidator(userInput)) {
      requestVerificationCode(userInput);
    } else if (usernamePattern.test(userInput)) {
      navigate("/login-with-password", { state: { userInput } });
    } else {
      setIsInputInvalid(true);
      setIsLoading(false);
    }
  };

  return (
    <div className="p-6 rounded-xl border-[2.5px] border-base-300 flex flex-col  gap-3">
      {alertMsg && (
        <TemporaryAlert message={alertMsg!} type="error" duration={5000} />
      )}

      <a className="btn bg-base-100 border-0 self-center" href="/">
        <MainLogo width="120" />
      </a>
      <h1 className="text-xl mb-4 font-semibold">ورود</h1>
      <p className="mb-2">لطفا نام کاربری یا شماره تلفن خود را وارد نمایید</p>
      {isInputInvalid && (
        <div className=" text-error text-[13px] font-bold">
          <span>نام کاربری یا شماره تلفن وارد شده صحیح نمی باشد</span>
        </div>
      )}
      <form onSubmit={handleUsernameSubmit}>
        <label
          className={`input input-bordered input-info input-md flex items-center gap-2 ${
            isInputInvalid ? "input-error" : ""
          }`}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 16 16"
            fill="currentColor"
            className="h-4 w-4 opacity-85"
          >
            <path d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6ZM12.735 14c.618 0 1.093-.561.872-1.139a6.002 6.002 0 0 0-11.215 0c-.22.578.254 1.139.872 1.139h9.47Z" />
          </svg>
          <input
            type="text"
            id="userInput"
            name="userInput"
            className=" overflow-visible"
            placeholder="نام کاربری یا شماره تلفن"
          />
        </label>
        <button
          className="btn btn-primary self-center h-11 btn-sm mt-4 w-full  text-lg font-bold"
          type="submit"
          disabled={isLoading}
        >
          ورود
        </button>
      </form>
    </div>
  );
};

export default Login;
