"use client";

import { MainLogo } from "../../assets/MainLogo";
import TemporaryAlert from "@/app/ui/alert/alert";
import { LoginState, processLoginInput } from "@/app/lib/actions/auth/login";
import { useActionState } from "react";

export default function Login() {
  const initialState: LoginState = { formError: null, alertError: null };
  const [state, formAction, pending] = useActionState(
    processLoginInput,
    initialState
  );

  return (
    <>
      {state.alertError && (
        <TemporaryAlert
          key={Date.now()} // ??
          message={state.alertError}
          type="error"
          duration={4000}
        />
      )}
      <h1 className="text-xl mb-4 font-semibold">ورود | ثبت نام</h1>
      <p className="mb-2">لطفا نام کاربری یا شماره تلفن خود را وارد نمایید</p>
      {state.formError && (
        <div className=" text-error text-[13px] font-bold">
          <span>{state.formError}</span>
        </div>
      )}
      <form action={formAction}>
        <label
          className={`input input-bordered input-info input-md flex items-center gap-2 ${
            state.formError ? "input-error" : ""
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
            defaultValue={state.prevInput}
            type="text"
            id="loginInput"
            name="loginInput"
            className=" overflow-visible"
            placeholder="نام کاربری یا شماره تلفن"
          />
        </label>
        <button
          className="btn btn-primary self-center h-11 btn-sm mt-4 w-full  text-lg font-bold"
          type="submit"
          disabled={pending}
        >
          ورود
        </button>
      </form>
    </>
  );
}
