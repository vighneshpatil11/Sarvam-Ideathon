"use client";

import Link from "next/link";
import { useRef, useState, useCallback, useEffect } from "react";
import {
  ArrowUp,
  Bot,
  ExternalLink,
  Mic,
  MicOff,
  RotateCcw,
  ShieldAlert,
  Sparkles,
  Volume2,
  VolumeX,
  UserRound,
  Loader2,
  Send,
} from "lucide-react";
import { SourceList } from "@/components/UI";
import { DEMO_MODE } from "@/lib/config";
import { sendAssistantMessage } from "@/lib/api/assistant";
import { demoAssistantReply } from "@/data/demo/assistant";
import { useApp } from "@/context/AppContext";
import type { AssistantResponse, Language } from "@/types";

type Message = { role: "user" | "assistant"; text: string; data?: AssistantResponse };

function bcp47ToAppLang(bcp47: string): Language {
  if (bcp47.startsWith("mr")) return "mr";
  if (bcp47.startsWith("hi")) return "hi";
  return "en";
}

function langToBcp47(lang: Language): string {
  if (lang === "mr") return "mr-IN";
  if (lang === "hi") return "hi-IN";
  return "en-IN";
}

export function AssistantWidget({ standalone = false }: { standalone?: boolean }) {
  const { language, setLanguage, t } = useApp();
  const bcp47 = langToBcp47(language);

  const initialGreeting =
    language === "mr"
      ? "नमस्कार! मी सारथी (SAARTHI) - आपले सरकार एआय सहाय्यक. तुम्हाला महाराष्ट्र शासनाच्या कोणत्याही सेवेबद्दल (उदा. अधिवास दाखला, उत्पन्न दाखला, जात प्रमाणपत्र, रेशन कार्ड, ७/१२ उतारा इत्यादी) माहिती हवी असल्यास विचारा किंवा बोला."
      : language === "hi"
      ? "नमस्ते! मैं सारथी (SAARTHI) - आपले सरकार एआय सहायक हूँ। आपको महाराष्ट्र सरकार की किसी भी सेवा की जानकारी चाहिए तो पूछें या बोलें।"
      : "Hello! I am SAARTHI - Aaple Sarkar AI Voice Assistant. Speak or type to ask about any Maharashtra government service.";

  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      text: DEMO_MODE ? demoAssistantReply : initialGreeting,
    },
  ]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [voiceOutput, setVoiceOutput] = useState(true);
  const [listening, setListening] = useState(false);
  const [transcribing, setTranscribing] = useState(false);
  
  // Rate-limiting and playback loading state
  const [playingAudio, setPlayingAudio] = useState(false);
  const [audioLoading, setAudioLoading] = useState(false);
  const currentAudioRef = useRef<HTMLAudioElement | null>(null);

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const chunksRef = useRef<BlobPart[]>([]);
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (messages.length === 1 && messages[0].role === "assistant") {
      setMessages([{ role: "assistant", text: initialGreeting }]);
    }
  }, [language]);

  const speak = async (text: string, langCode = bcp47) => {
    // If already loading or speaking, prevent duplicate requests (Rate-limit)
    if (audioLoading || playingAudio) {
      if (currentAudioRef.current) {
        currentAudioRef.current.pause();
        currentAudioRef.current = null;
      }
      setPlayingAudio(false);
    }

    setAudioLoading(true);
    try {
      const res = await fetch("/api/tts", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, languageCode: langCode }),
      });
      const data = await res.json();
      if (!data.success) {
        console.error("TTS error:", data.error);
        return;
      }
      const raw = atob(data.audio);
      const bytes = new Uint8Array(raw.length);
      for (let i = 0; i < raw.length; i++) bytes[i] = raw.charCodeAt(i);
      const blob = new Blob([bytes], { type: "audio/wav" });
      const url = URL.createObjectURL(blob);
      const audio = new Audio(url);
      currentAudioRef.current = audio;

      audio.onplay = () => {
        setAudioLoading(false);
        setPlayingAudio(true);
      };
      audio.onended = () => {
        setPlayingAudio(false);
        URL.revokeObjectURL(url);
        currentAudioRef.current = null;
      };
      audio.onerror = () => {
        setAudioLoading(false);
        setPlayingAudio(false);
      };

      await audio.play();
    } catch (err) {
      console.error("TTS playback error:", err);
    } finally {
      setAudioLoading(false);
    }
  };

  const executeSend = async (messageText: string, currentLang = language) => {
    const trimmed = messageText.trim();
    if (!trimmed || busy) return;

    setInput("");
    setError("");
    setMessages((v) => [...v, { role: "user", text: trimmed }]);
    setBusy(true);

    try {
      const data: AssistantResponse = DEMO_MODE
        ? {
            answer: demoAssistantReply,
            sources: [],
            warnings: ["Demo mode: no live government knowledge base is connected."],
          }
        : await sendAssistantMessage(trimmed, currentLang, sessionId);

      if (data.session_id) setSessionId(data.session_id);
      setMessages((v) => [...v, { role: "assistant", text: data.answer, data }]);
      if (voiceOutput) {
        await speak(data.answer, langToBcp47(currentLang));
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : "Message could not be sent.");
    } finally {
      setBusy(false);
      window.setTimeout(() => endRef.current?.scrollIntoView({ behavior: "smooth" }), 50);
    }
  };

  const startRecording = async () => {
    if (!navigator.mediaDevices) {
      setError("Audio recording is not supported in this browser.");
      return;
    }
    setError("");

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      streamRef.current = stream;
      chunksRef.current = [];

      const recorder = new MediaRecorder(stream);
      mediaRecorderRef.current = recorder;

      recorder.ondataavailable = (e) => {
        if (e.data.size > 0) chunksRef.current.push(e.data);
      };

      recorder.onstop = async () => {
        setListening(false);
        setTranscribing(true);
        stream.getTracks().forEach((t) => t.stop());

        try {
          const rawMime = recorder.mimeType || "audio/webm";
          const cleanMime = rawMime.split(";")[0];
          const ext = cleanMime.includes("mp3")
            ? "mp3"
            : cleanMime.includes("wav")
            ? "wav"
            : "webm";

          const blob = new Blob(chunksRef.current, { type: cleanMime });
          const formData = new FormData();
          formData.append("file", blob, `recording.${ext}`);
          formData.append("language", bcp47);

          const res = await fetch("/api/stt", { method: "POST", body: formData });
          const data = await res.json();

          if (data.success && data.text) {
            const detectedLang = data.detectedLanguage || bcp47;
            const appLang = bcp47ToAppLang(detectedLang);
            if (appLang !== language) {
              setLanguage(appLang);
            }
            // Auto submit answer as soon as user stops speech
            await executeSend(data.text, appLang);
          } else {
            setError(data.error || "Could not transcribe audio.");
          }
        } catch {
          setError("Failed to send audio for transcription.");
        } finally {
          setTranscribing(false);
        }
      };

      recorder.start();
      setListening(true);
    } catch {
      setError("Microphone access was blocked. Allow microphone permission in your browser.");
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== "inactive") {
      mediaRecorderRef.current.stop();
    }
    streamRef.current?.getTracks().forEach((t) => t.stop());
    setListening(false);
  };

  const toggleMicrophone = () => {
    if (listening) {
      stopRecording();
    } else {
      startRecording();
    }
  };

  const handleFormSubmit = (e?: React.FormEvent) => {
    e?.preventDefault();
    void executeSend(input);
  };

  return (
    <div className={`chat-layout ${standalone ? "standalone-layout" : ""}`}>
      <section className="chat-panel" aria-label="SAARTHI Aaple Sarkar Assistant">
        <div className="chat-topline">
          <span className="chat-avatar"><Bot /></span>
          <div className="chat-agent-name">
            <b>{language === "mr" ? "आपले सरकार एआय मार्गदर्शक" : "Aaple Sarkar Voice Assistant"}</b>
            <small>
              <span className="online-dot" />
              {DEMO_MODE
                ? "Demo Mode"
                : language === "mr"
                ? "सर्व ३० शासकीय सेवांशी जोडलेले"
                : "Connected to 30 Aaple Sarkar Services"}
            </small>
          </div>
          <span className="chat-language">{language.toUpperCase()}</span>
        </div>

        <div className="chat-messages" aria-live="polite">
          {messages.map((m, i) => (
            <div className={`chat-message ${m.role}`} key={i}>
              <span className="message-avatar">
                {m.role === "assistant" ? <Bot size={17} /> : <UserRound size={17} />}
              </span>
              <div className="message-content">
                <p>{m.text}</p>
                {m.data?.warnings?.map((w, j) => (
                  <div className="warning-note" key={j}>
                    <ShieldAlert size={15} />
                    {w}
                  </div>
                ))}
                {m.data?.sources?.length ? <SourceList sources={m.data.sources} /> : null}
                {m.data?.related_services?.map((s) => (
                  <Link className="related-link" href={`/services/${s.slug}`} key={s.slug}>
                    {s.name} <ExternalLink size={13} />
                  </Link>
                ))}
                {m.role === "assistant" && voiceOutput && (
                  <button
                    className="message-speak-button"
                    type="button"
                    onClick={() => speak(m.text, langToBcp47(language))}
                    disabled={audioLoading}
                    aria-label="Play reply"
                    style={{ display: "inline-flex", alignItems: "center", gap: "0.4rem" }}
                  >
                    {audioLoading ? (
                      <>
                        <Loader2 size={14} className="animate-spin" />
                        <span>{language === "mr" ? "आवाज लोड होत आहे..." : "Loading audio..."}</span>
                      </>
                    ) : playingAudio ? (
                      <>
                        <VolumeX size={14} />
                        <span>{language === "mr" ? "थांबवा (Stop Audio)" : "Stop Audio"}</span>
                      </>
                    ) : (
                      <>
                        <Volume2 size={14} />
                        <span>{language === "mr" ? "ऐका (Listen)" : "Listen"}</span>
                      </>
                    )}
                  </button>
                )}
              </div>
            </div>
          ))}
          {busy && (
            <div className="chat-message assistant">
              <span className="message-avatar"><Bot size={17} /></span>
              <div className="typing-indicator">
                <i /><i /><i />
              </div>
            </div>
          )}
          <div ref={endRef} />
        </div>

        {error && (
          <div className="chat-error" role="alert">
            {error}
            <button onClick={() => setError("")}>
              <RotateCcw size={14} /> {language === "mr" ? "रद्द करा" : "Dismiss"}
            </button>
          </div>
        )}

        {/* Global Audio / STT Progress Indicators */}
        {(transcribing || audioLoading || listening) && (
          <div
            style={{
              padding: "0.4rem 1rem",
              background: "var(--color-canvas-subtle, #f6f8fa)",
              borderTop: "1px solid var(--color-border-default, #e1e4e8)",
              display: "flex",
              alignItems: "center",
              gap: "0.6rem",
              fontSize: "0.85rem",
              color: "var(--color-fg-muted, #586069)",
            }}
          >
            {listening ? (
              <>
                <span className="online-dot" style={{ background: "#cf222e" }} />
                <span>
                  {language === "mr"
                    ? "माईक चालू आहे... बोलून झाल्यावर खाली लाल बटण दाबा."
                    : "Listening... Click the red button when finished."}
                </span>
              </>
            ) : transcribing ? (
              <>
                <Loader2 size={15} className="animate-spin" />
                <span>
                  {language === "mr"
                    ? "आवाज प्रक्रिया सुरू आहे (Transcribing)... कृपया थांबा."
                    : "Transcribing your voice... Please wait."}
                </span>
              </>
            ) : audioLoading ? (
              <>
                <Loader2 size={15} className="animate-spin" />
                <span>
                  {language === "mr"
                    ? "सर्वम बुलबुल आवाज तयार होत आहे... (Loading speech)..."
                    : "Generating voice with Sarvam Bulbul..."}
                </span>
              </>
            ) : null}
          </div>
        )}

        <div className="voice-toolbar">
          <button
            className={`voice-option ${listening ? "active pulse-mic" : ""}`}
            type="button"
            onClick={toggleMicrophone}
            disabled={transcribing || busy}
            aria-pressed={listening}
          >
            {transcribing ? (
              <Loader2 size={18} className="animate-spin" />
            ) : listening ? (
              <MicOff size={18} />
            ) : (
              <Mic size={18} />
            )}
            <span>
              {transcribing
                ? language === "mr"
                  ? "आवाज प्रक्रिया सुरू आहे..."
                  : "Transcribing voice…"
                : listening
                ? language === "mr"
                  ? "थांबवा (उत्तर लगेच मिळेल)"
                  : "Stop & Get Answer"
                : language === "mr"
                  ? "माईक दाबा व मराठीत बोला"
                  : "Speak to Aaple Sarkar AI"}
            </span>
          </button>

          <button
            className={`voice-option ${voiceOutput ? "active" : ""}`}
            type="button"
            onClick={() => setVoiceOutput((v) => !v)}
            aria-pressed={voiceOutput}
          >
            {voiceOutput ? <Volume2 size={18} /> : <VolumeX size={18} />}
            <span>
              {voiceOutput
                ? language === "mr"
                  ? "आवाज उत्तर चालू"
                  : "Voice replies ON"
                : language === "mr"
                  ? "आवाज उत्तर बंद"
                  : "Voice replies OFF"}
            </span>
          </button>
        </div>

        <form className="chat-composer" onSubmit={handleFormSubmit}>
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={
              language === "mr"
                ? "आपले सरकार सेवेबद्दल येथे प्रश्न लिहा किंवा वर माईक दाबून बोला..."
                : "Type your query about Aaple Sarkar or click mic to speak..."
            }
            rows={2}
            aria-label="Your message"
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                void handleFormSubmit();
              }
            }}
          />
          <button disabled={!input.trim() || busy} aria-label={t("send")}>
            <Send size={18} />
          </button>
        </form>
      </section>

      <aside className="assistant-aside">
        <div className="aside-card">
          <span className="aside-icon"><Sparkles /></span>
          <h3>{language === "mr" ? "वारंवार विचारले जाणारे प्रश्न" : "Frequently Asked Questions"}</h3>
          <p>
            {language === "mr"
              ? "खालीलपैकी कोणत्याही प्रश्नावर क्लिक करा किंवा थेट माईकद्वारे विचारा:"
              : "Click any prompt or speak your question directly:"}
          </p>
          {(language === "mr"
            ? [
                "अधिवास प्रमाणपत्रासाठी कोणती कागदपत्रे लागतात?",
                "उत्पन्नाचा दाखला कसा काढायचा आणि फी किती आहे?",
                "जात प्रमाणपत्रासाठी कोणते पुरावे आवश्यक आहेत?",
                "नवीन रेशन कार्डसाठी अर्ज कसा करावा?",
                "डिजिटल ७/१२ उतारा आणि फेरफार कसा मिळवायचा?",
              ]
            : [
                "What documents are required for a Domicile Certificate?",
                "How to apply for an Income Certificate and what is the fee?",
                "What documents are needed for a Caste Certificate?",
                "How to apply for a new Ration Card in Maharashtra?",
                "How to download a digital 7/12 Satbara extract online?",
              ]
          ).map((q) => (
            <button
              className="prompt-button"
              key={q}
              onClick={() => {
                setInput(q);
                void executeSend(q);
              }}
            >
              {q}
              <ArrowUp size={14} />
            </button>
          ))}
        </div>

        <div className="aside-card privacy-card">
          <ShieldAlert />
          <h3>{language === "mr" ? "सुरक्षितता व गोपनीयता" : "Information Security"}</h3>
          <p>
            {language === "mr"
              ? "कृपया पासवर्ड, ओटीपी, बँक खात्याचे तपशील किंवा वैयक्तिक गोपनीय माहिती देऊ नका."
              : "Do not enter passwords, OTPs, Aadhaar/PAN, or bank account credentials."}
          </p>
        </div>
      </aside>
    </div>
  );
}
