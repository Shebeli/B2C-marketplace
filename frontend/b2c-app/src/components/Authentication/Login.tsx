import { phoneNumberValidator } from "@persian-tools/persian-tools";
import { MainLogo } from "../../assets/MainLogo";
import { useNavigate } from "react-router-dom";
import {useState } from "react";

const Login: React.FC = () => {
  const navigate = useNavigate();
  const usernamePattern = /^(?=[a-zA-Z])(?=(?:[^a-zA-Z]*[a-zA-Z]){3})\w{4,}$/;
  const username = useState<string | null>(null);
  const [isInputInvalid, setIsInputInvalid] = useState<boolean>(false);

  const handleUsernameSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const userInput = (event.currentTarget.username as HTMLInputElement).value;
    if (phoneNumberValidator(userInput)) {
      const timestamp = new Date().toISOString();
      localStorage.setItem("inputPhoneTimeStamp", timestamp);
      localStorage.setItem("inputPhone", userInput);
      navigate("/verify-phone");
    } else if (usernamePattern.test(userInput)) {
      navigate("/login-with-password", { state: { username } });
    } else {
      setIsInputInvalid(true);
    }
  };

  return (
    <div className="p-6 rounded-xl border-2 flex flex-col  gap-3 shadow-sm">
      <a className="btn bg-base-100 border-0 self-center" href="/">
        <MainLogo width="120" />
      </a>
      <h1 className="text-xl mb-4 font-semibold">ورود</h1>
      <p className="mb-2">لطفا نام کاربری یا شماره تلفن خود را وارد نمایید</p>
      {isInputInvalid && (
        <div className=" text-error text-[13px] font-bold">
          <span>نام کاربری یا شماره تلفن وارد شده نا معتبر می باشد</span>
        </div>
      )}
      <form onSubmit={handleUsernameSubmit}>
        <label
          className={`input input-bordered flex items-center gap-2 ${
            isInputInvalid ? "input-error" : ""
          }`}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 16 16"
            fill="currentColor"
            className="h-4 w-4 opacity-70"
          >
            <path d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6ZM12.735 14c.618 0 1.093-.561.872-1.139a6.002 6.002 0 0 0-11.215 0c-.22.578.254 1.139.872 1.139h9.47Z" />
          </svg>
          <input
            type="text"
            id="username"
            name="username"
            className="grow"
            placeholder="نام کاربری یا شماره تلفن"
          />
        </label>
        <button
          className="btn btn-primary self-center h-11 btn-sm mt-4 w-full  text-lg font-bold"
          type="submit"
        >
          ورود
        </button>
      </form>
    </div>
  );
};

export default Login;
