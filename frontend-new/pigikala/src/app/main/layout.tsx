import { Footer } from "../ui/footer";
import Navbar from "../ui/navbar/navbar";

export default function MainLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="items-center justify-center flex flex-col">
      <Navbar />
      <main>{children}</main>
      <Footer />
    </div>
  );
}
