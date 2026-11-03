"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { ArrowLeft, ArrowUpRight, CircleCheck, ListOrdered } from "lucide-react";
import { PageIntro, Disclaimer, ErrorState, EmptyState, SourceList } from "@/components/UI";
import { DEMO_MODE } from "@/lib/config";
import { getGuide } from "@/lib/api/guides";
import { demoSteps } from "@/data/demo/service-details";
import { safeExternalUrl } from "@/lib/utils";
import { useApp } from "@/context/AppContext";
import type { ApplicationStep, Source } from "@/types";

export default function GuidePage() {
  const { slug } = useParams<{ slug: string }>();
  const { language } = useApp();
  const [steps, setSteps] = useState<ApplicationStep[]>(DEMO_MODE ? demoSteps : []);
  const [sources, setSources] = useState<Source[]>([]);
  const [loading, setLoading] = useState(!DEMO_MODE);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!DEMO_MODE) {
      setLoading(true);
      setError("");
      getGuide(slug, language)
        .then((r) => {
          setSteps(r.steps || []);
          setSources(r.sources || []);
        })
        .catch((e) => setError(e.message))
        .finally(() => setLoading(false));
    }
  }, [slug, language]);

  const serviceTitle = slug.replaceAll("-", " ");

  return (
    <div className="container page-container">
      <div className="breadcrumbs">
        <Link href={`/services/${slug}`}>{serviceTitle}</Link>
        <span>/</span>
        <span>{language === "mr" ? "अर्ज प्रक्रिया" : "Application guide"}</span>
      </div>

      <PageIntro
        eyebrow={language === "mr" ? "अधिकृत पायऱ्या" : "NEXT STEPS"}
        title={language === "mr" ? "अर्ज कसा करावा (सविस्तर मार्गदर्शक)" : "Application guide"}
        description={
          language === "mr"
            ? "महाराष्ट्र शासनाच्या आपले सरकार पोर्टलवर अर्ज करण्यासाठी खालील अधिकृत पायऱ्यांचे पालन करा."
            : "Follow the verified official steps and links to submit your application on the Maharashtra Aaple Sarkar portal."
        }
      />

      <div className="guide-intro">
        <ListOrdered />
        <p>
          {language === "mr"
            ? "सर्व प्रक्रिया महाराष्ट्र लोकसेवा हमी कायद्यानुसार (RTS) कायदेशीररित्या निर्धारित मुदतीत पूर्ण केली जाते."
            : "Only verified portal URLs are shown. Fees and timelines are guaranteed under the Maharashtra Right to Public Services Act (RTS)."}
        </p>
      </div>

      {loading ? (
        <div className="skeleton-card wide" />
      ) : error ? (
        <ErrorState message={error} />
      ) : steps.length ? (
        <div className="steps-list">
          {steps.map((step, i) => {
            const url = safeExternalUrl(step.action_url);
            return (
              <article className="guide-step" key={`${step.step_number}-${i}`}>
                <span className="step-index">{step.step_number || i + 1}</span>
                <div>
                  <h3>{step.title}</h3>
                  {step.description && <p>{step.description}</p>}
                  {url && (
                    <a
                      className="official-link"
                      href={url}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      {step.action_label || (language === "mr" ? "अधिकृत पोर्टल उघडा" : "Open official portal")}
                      <ArrowUpRight size={15} />
                    </a>
                  )}
                  <SourceList sources={step.sources} />
                </div>
              </article>
            );
          })}
        </div>
      ) : (
        <EmptyState
          title={language === "mr" ? "अर्ज प्रक्रिया उपलब्ध नाही" : "Application steps are not available"}
          message={
            language === "mr"
              ? "या सेवेसाठी मार्गदर्शक सूचना लोड केल्या जात आहेत."
              : "No application instructions or official links have been supplied for this service yet."
          }
        />
      )}

      <SourceList sources={sources} />

      <div className="official-reminder">
        <CircleCheck />
        <div>
          <b>
            {language === "mr"
              ? "आपले सरकार पोर्टलवर थेट अर्ज करा"
              : "Complete the application on the official portal"}
          </b>
          <p>
            {language === "mr"
              ? "सारथी (SAARTHI) हा तुमचा डिजिटल मार्गदर्शक आहे. अंतिम प्रमाणपत्र सक्षम अधिकाऱ्यांकडून दिले जाते."
              : "SAARTHI is an educational guidance assistant. The competent government department issues all official decisions and certificates."}
          </p>
        </div>
      </div>

      <Disclaimer />
      <Link href={`/services/${slug}`} className="back-link">
        <ArrowLeft size={16} /> {language === "mr" ? "सेवेकडे परत जा" : "Back to service"}
      </Link>
    </div>
  );
}
