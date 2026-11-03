"use client";

import { useApp } from "@/context/AppContext";
import { AssistantWidget } from "@/components/AssistantWidget";
import { Disclaimer } from "@/components/UI";
import { Sparkles, Mic, Volume2, ShieldCheck, Languages } from "lucide-react";

export default function HomePage() {
  const { language, setLanguage } = useApp();

  return (
    <div className="container page-container" style={{ paddingTop: "1.5rem", maxWidth: "1150px" }}>
      {/* Focused Hero Header */}
      <header className="page-intro" style={{ marginBottom: "1.25rem", textAlign: "center" }}>
        <div className="eyebrow" style={{ justifyContent: "center", display: "inline-flex", gap: "0.5rem" }}>
          <Sparkles size={16} />
          {language === "mr"
            ? "आपले सरकार · सर्वम एआय व्हॉइस असिस्टंट"
            : "AAPLE SARKAR · SARVAM AI VOICE ASSISTANT"}
        </div>
        
        <h1 style={{ fontSize: "2.35rem", marginTop: "0.4rem", marginBottom: "0.6rem", lineHeight: "1.25" }}>
          {language === "mr" ? (
            <>
              आपले सरकार सेवांसाठी <em style={{ fontStyle: "normal", color: "var(--color-primary, #0969da)" }}>व्हॉइस असिस्टंट</em>
            </>
          ) : (
            <>
              Voice Assistant for <em style={{ fontStyle: "normal", color: "var(--color-primary, #0969da)" }}>Aaple Sarkar Services</em>
            </>
          )}
        </h1>

        <p style={{ maxWidth: "780px", margin: "0 auto", fontSize: "1.05rem", color: "var(--color-fg-muted, #57606a)" }}>
          {language === "mr"
            ? "माईक बटण दाबून मराठीत बोला. उत्पन्नाचा दाखला, अधिवास (Domicile), जात प्रमाणपत्र, डिजिटल ७/१२ उतारा आणि ३०+ शासकीय सेवांची माहिती, कागदपत्रे व नियम त्वरित जाणून घ्या."
            : "Speak or type naturally in English, Marathi, or Hindi. Get verified document checklists, statutory RTS timelines, fees, and official links for 30+ Maharashtra public services."}
        </p>

        {/* Feature Badges */}
        <div style={{ display: "flex", justifyContent: "center", gap: "1rem", flexWrap: "wrap", marginTop: "0.85rem", fontSize: "0.88rem" }}>
          <span style={{ display: "inline-flex", alignItems: "center", gap: "0.4rem", padding: "0.25rem 0.75rem", borderRadius: "999px", background: "var(--color-canvas-subtle, #f6f8fa)", border: "1px solid var(--color-border-default, #d0d7de)" }}>
            <Mic size={15} color="#0969da" />
            {language === "mr" ? "माईक थांबवताच थेट उत्तर" : "Instant Answer on Stop Speech"}
          </span>
          <span style={{ display: "inline-flex", alignItems: "center", gap: "0.4rem", padding: "0.25rem 0.75rem", borderRadius: "999px", background: "var(--color-canvas-subtle, #f6f8fa)", border: "1px solid var(--color-border-default, #d0d7de)" }}>
            <Volume2 size={15} color="#1a7f37" />
            {language === "mr" ? "सर्वम बुलबुल मराठी आवाज" : "Sarvam Bulbul Marathi & English Voice"}
          </span>
          <span style={{ display: "inline-flex", alignItems: "center", gap: "0.4rem", padding: "0.25rem 0.75rem", borderRadius: "999px", background: "var(--color-canvas-subtle, #f6f8fa)", border: "1px solid var(--color-border-default, #d0d7de)" }}>
            <ShieldCheck size={15} color="#8250df" />
            {language === "mr" ? "लोकसेवा हक्क अधिनियम (RTS)" : "Verified RTS Act Rules"}
          </span>
        </div>
      </header>

      {/* Language Selection Banner directly above Chatbot */}
      <div
        style={{
          background: "linear-gradient(135deg, rgba(9, 105, 218, 0.08) 0%, rgba(130, 80, 223, 0.08) 100%)",
          border: "1px solid var(--color-border-default, #d0d7de)",
          borderRadius: "12px",
          padding: "0.75rem 1.25rem",
          marginBottom: "1.25rem",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          flexWrap: "wrap",
          gap: "0.75rem",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: "0.6rem" }}>
          <Languages size={20} color="#0969da" />
          <span style={{ fontSize: "0.95rem", fontWeight: 500 }}>
            {language === "mr"
              ? "कोणत्या भाषेत संभाषण करायचे आहे?"
              : "Which language would you prefer to converse in?"}
          </span>
        </div>

        <div style={{ display: "flex", gap: "0.5rem" }}>
          <button
            type="button"
            onClick={() => setLanguage("en")}
            style={{
              padding: "0.35rem 0.9rem",
              borderRadius: "6px",
              fontSize: "0.88rem",
              fontWeight: language === "en" ? 600 : 400,
              cursor: "pointer",
              border: language === "en" ? "2px solid #0969da" : "1px solid #d0d7de",
              background: language === "en" ? "#0969da" : "#ffffff",
              color: language === "en" ? "#ffffff" : "#24292f",
              transition: "all 0.15s ease",
            }}
          >
            English
          </button>

          <button
            type="button"
            onClick={() => setLanguage("mr")}
            style={{
              padding: "0.35rem 0.9rem",
              borderRadius: "6px",
              fontSize: "0.88rem",
              fontWeight: language === "mr" ? 600 : 400,
              cursor: "pointer",
              border: language === "mr" ? "2px solid #0969da" : "1px solid #d0d7de",
              background: language === "mr" ? "#0969da" : "#ffffff",
              color: language === "mr" ? "#ffffff" : "#24292f",
              transition: "all 0.15s ease",
            }}
          >
            मराठी (Marathi)
          </button>
        </div>
      </div>

      {/* The Central Voice Assistant */}
      <main style={{ marginBottom: "2rem" }}>
        <AssistantWidget standalone={true} />
      </main>

      {/* Footer Disclaimer */}
      <footer style={{ marginTop: "1rem" }}>
        <Disclaimer />
      </footer>
    </div>
  );
}
