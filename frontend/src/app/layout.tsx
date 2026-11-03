import type { Metadata } from "next"; import "./globals.css"; import { AppProvider } from "@/context/AppContext"; import { PageShell } from "@/components/Shell";
export const metadata: Metadata = { title: "SAARTHI — Understand government services", description: "Independent, multilingual guidance to help people understand and navigate public services." };
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) { return <html lang="en"><body><AppProvider><PageShell>{children}</PageShell></AppProvider></body></html>; }
