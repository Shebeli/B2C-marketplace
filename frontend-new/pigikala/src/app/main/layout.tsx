import { Footer } from "../ui/footer";
import Navbar from "../ui/navbar/navbar";

export default function MainLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex flex-col min-h-screen justify-between">
      <Navbar />
      <main className="w-full flex justify-center">
        {children}
      </main>
      <Footer />
    </div>
  );
}
