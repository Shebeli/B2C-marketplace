import { useState } from "react";
import { MainLogo } from "../../assets/MainLogo";

const VerifyLogin: React.FC = () => {
  const [phoneNumber, setPhoneNumber] = useState<string|null>(null);

  return (
    <div className="p-6 rounded-xl border-2 flex flex-col  gap-3 shadow-sm">
      <a className="btn bg-base-100 border-0 self-center" href="/">
        <MainLogo width="120" />
      </a>
        <p>
            لطفا کد تایید ارسال به شماره ی 
        </p>
      <button className="btn btn-primary self-center h-11 btn-sm mt-4 w-full  text-lg font-bold">
        تایید
      </button>
    </div>
  );
};

export default VerifyLogin;
