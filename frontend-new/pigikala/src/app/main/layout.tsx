import Navbar from "../ui/navbar/navbarprofile/navbar";
import { Footer } from "../ui/footer";

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
