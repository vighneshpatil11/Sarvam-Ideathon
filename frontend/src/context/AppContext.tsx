"use client";
import { createContext, useContext, useEffect, useMemo, useState } from "react";
import type { Language } from "@/types";
import { messages, type MessageKey } from "@/i18n";
type AppContextValue = { language: Language; setLanguage: (language: Language) => void; t: (key: MessageKey) => string };
const AppContext = createContext<AppContextValue | null>(null);
export function AppProvider({ children }: { children: React.ReactNode }) {
  const [language, setLanguage] = useState<Language>("en");
  useEffect(() => { const saved = localStorage.getItem("saarthi-language"); if (saved === "en" || saved === "hi" || saved === "mr") setLanguage(saved); }, []);
  const updateLanguage = (next: Language) => { setLanguage(next); localStorage.setItem("saarthi-language", next); };
  const value = useMemo(() => ({ language, setLanguage: updateLanguage, t: (key: MessageKey) => messages[language][key] }), [language]);
  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
}
export function useApp() { const value = useContext(AppContext); if (!value) throw new Error("useApp must be used within AppProvider"); return value; }
