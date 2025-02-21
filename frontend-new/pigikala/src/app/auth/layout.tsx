import { MainLogo } from "../assets/MainLogo";

export default function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex items-center justify-center h-screen">
      <main>
        <div className="p-6 rounded-xl border-[2.5px] border-base-300 flex flex-col  gap-3 shadow-sm">
          <MainLogo width={120}/>
          {children}
        </div>
      </main>
    </div>
  );
}
