import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "BSOP | Autonomous Recruitment Intelligence",
  description: "Enterprise-grade autonomous AI recruiting workforce platform.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="min-h-screen bg-[#09090b] selection:bg-blue-500/30">
          {children}
        </div>
      </body>
    </html>
  );
}
