"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { ArrowLeft, CheckCircle2, FileCheck2 } from "lucide-react";
import { PageIntro, Disclaimer, ErrorState, EmptyState, SourceList } from "@/components/UI";
import { DEMO_MODE } from "@/lib/config";
import { demoDocuments } from "@/data/demo/service-details";
import { getDocuments } from "@/lib/api/documents";
import { useApp } from "@/context/AppContext";
import type { ServiceDocument } from "@/types";

export default function DocumentsPage() {
  const { slug } = useParams<{ slug: string }>();
  const { language } = useApp();
  const [docs, setDocs] = useState<ServiceDocument[]>(DEMO_MODE ? demoDocuments : []);
  const [checked, setChecked] = useState<string[]>([]);
  const [loading, setLoading] = useState(!DEMO_MODE);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!DEMO_MODE) {
      setLoading(true);
      setError("");
      getDocuments(slug, language)
        .then((r) => setDocs(r.documents || []))
        .catch((e) => setError(e.message))
        .finally(() => setLoading(false));
    }
  }, [slug, language]);

  function toggle(id: string) {
    setChecked((v) => (v.includes(id) ? v.filter((x) => x !== id) : [...v, id]));
  }

  const serviceTitle = slug.replaceAll("-", " ");

  return (
    <div className="container page-container">
      <div className="breadcrumbs">
        <Link href={`/services/${slug}`}>{serviceTitle}</Link>
        <span>/</span>
        <span>{language === "mr" ? "कागदपत्र यादी" : "Documents"}</span>
      </div>

      <PageIntro
        eyebrow={language === "mr" ? "तयारी करा" : "GET PREPARED"}
        title={language === "mr" ? "आवश्यक कागदपत्रांची यादी" : "Document checklist"}
        description={
          language === "mr"
            ? "अर्ज करताना लागणारी आवश्यक कागदपत्रे तपासा. ही चेकलिस्ट तुमच्या सोयीसाठी आहे."
            : "Use this checklist to keep track of what you have prepared for official submission under the Maharashtra RTS Act."
        }
      />

      <div className="checklist-summary">
        <FileCheck2 />
        <span>
          <b>
            {language === "mr"
              ? `${docs.length} पैकी ${checked.length} कागदपत्रे तयार`
              : `${checked.length} of ${docs.length} checked`}
          </b>
          <small>
            {language === "mr"
              ? "तुमची चेकलिस्ट फक्त वैयक्तिक स्मरणपत्रासाठी आहे."
              : "Your checklist is a personal reminder to ensure no documents are missed."}
          </small>
        </span>
      </div>

      {loading ? (
        <div className="skeleton-card wide" />
      ) : error ? (
        <ErrorState message={error} />
      ) : docs.length ? (
        <div className="document-list">
          {docs.map((doc) => (
            <label
              className={`document-row ${checked.includes(doc.id) ? "is-checked" : ""}`}
              key={doc.id}
            >
              <input
                type="checkbox"
                checked={checked.includes(doc.id)}
                onChange={() => toggle(doc.id)}
              />
              <span className="custom-check">
                <CheckCircle2 />
              </span>
              <span className="document-copy">
                <b>{doc.name}</b>
                {doc.description && <small>{doc.description}</small>}
                {doc.condition && <small>Condition: {doc.condition}</small>}
                {doc.notes?.map((note, i) => (
                  <small key={i}>{note}</small>
                ))}
              </span>
              <span className="requirement-tag">
                {doc.required === false
                  ? language === "mr"
                    ? "ऐच्छिक"
                    : "Conditional"
                  : language === "mr"
                  ? "अनिवार्य"
                  : "Required"}
              </span>
              <SourceList sources={doc.sources} />
            </label>
          ))}
        </div>
      ) : (
        <EmptyState
          title={language === "mr" ? "कागदपत्रांची यादी उपलब्ध नाही" : "No document requirements available"}
          message={
            language === "mr"
              ? "या सेवेसाठी कागदपत्रे तपासली जात आहेत."
              : "The document requirements are being loaded from verified official sources."
          }
        />
      )}

      <div className="privacy-note">
        <CheckCircle2 size={17} />
        <p>
          {language === "mr"
            ? "आयटम तपासल्याने केवळ हे पृष्ठ अपडेट होते. सारथी कोणतेही कागदपत्रे किंवा ओळख क्रमांक अपलोड किंवा संग्रहित करत नाही."
            : "Checking an item only updates this page. SAARTHI does not upload, store, or verify personal documents or identity numbers."}
        </p>
      </div>

      <Disclaimer />
      <Link href={`/services/${slug}`} className="back-link">
        <ArrowLeft size={16} /> {language === "mr" ? "सेवेकडे परत जा" : "Back to service"}
      </Link>
    </div>
  );
}
