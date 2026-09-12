import type { Metadata } from "next";
import { Fraunces, Outfit } from "next/font/google";
import Link from "next/link";
import "./globals.css";

const display = Fraunces({
  subsets: ["latin"],
  variable: "--fonte-display",
  display: "swap",
});

const sans = Outfit({
  subsets: ["latin"],
  variable: "--fonte-sans",
  display: "swap",
});

export const metadata: Metadata = {
  title: "Batalha Naval",
  description: "Batalha Naval — GPTech Games",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-BR" className={`${display.variable} ${sans.variable}`}>
      <body>
        <div className="atmosfera" aria-hidden="true" />
        <div className="casca">
          <header className="masthead">
            <p className="marca">GPTech Games</p>
            <Link href="/" className="logo">
              Batalha Naval
            </Link>
          </header>
          <main>{children}</main>
        </div>
      </body>
    </html>
  );
}
