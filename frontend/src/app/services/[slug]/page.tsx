"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import {
  ArrowRight,
  ClipboardCheck,
  FileText,
  ListOrdered,
  MessageCircle,
  MapPin,
  Building2,
  Clock,
  IndianRupee,
  ExternalLink,
} from "lucide-react";
import { PageIntro, Disclaimer, ErrorState, SourceList } from "@/components/UI";
import { DEMO_MODE } from "@/lib/config";
import { getService } from "@/lib/api/services";
import { getDemoService } from "@/data/demo/service-details";
import { useApp } from "@/context/AppContext";
import type { Service } from "@/types";

export default function ServiceDetailPage() {
  const { slug } = useParams<{ slug: string }>();
  const { language } = useApp();
  const [service, setService] = useState<Service | undefined>(DEMO_MODE ? getDemoService(slug) : undefined);
  const [loading, setLoading] = useState(!DEMO_MODE);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!DEMO_MODE) {
      setLoading(true);
      setError("");
      getService(slug, language)
        .then(setService)
        .catch((e) => setError(e.message))
        .finally(() => setLoading(false));
    }
  }, [slug, language]);

  if (loading) {
    return (
      <div className="container page-container">
        <div className="skeleton-line" />
        <div className="skeleton-card wide" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="container page-container">
        <ErrorState message={error} />
      </div>
    );
  }

  if (!service) {
    return (
      <div className="container page-container">
        <PageIntro
          title={language === "mr" ? "सेवा आढळली नाही" : "Service not found"}
          description={
            language === "mr"
              ? "ही सेवा सध्या डिरेक्टरीमध्ये उपलब्ध नाही."
              : "This service is not available in the connected service directory."
          }
        />
        <Link href="/services" className="button button-primary">
          {language === "mr" ? "सर्व सेवांकडे परत जा" : "Back to services"}
        </Link>
      </div>
    );
  }

  const dept = service.department?.name || service.department_name || "Revenue Department";
  const portalUrl = service.official_portal_url || "https://aaplesarkar.mahaonline.gov.in";

  return (
    <div className="container page-container">
      <div className="breadcrumbs">
        <Link href="/services">{language === "mr" ? "सेवा" : "Services"}</Link>
        <span>/</span>
        <span>{service.name}</span>
      </div>

      <PageIntro
        eyebrow={language === "mr" ? "अधिकृत सेवा माहिती" : "SERVICE OVERVIEW"}
        title={service.name}
        description={
          service.description ||
          service.short_description ||
          "Official government service under Maharashtra Right to Public Services Act (RTS)."
        }
      />

      <div className="detail-layout">
        <div className="detail-main">
          {/* Statutory RTS Fact Cards */}
          <div className="detail-facts">
            <div>
              <Building2 />
              <span>
                <small>{language === "mr" ? "सक्षम विभाग" : "Department"}</small>
                <b>{dept}</b>
              </span>
            </div>

            <div>
              <IndianRupee />
              <span>
                <small>{language === "mr" ? "अधिकृत शासकीय शुल्क" : "Statutory Fee"}</small>
                <b>₹{Number(service.statutory_fee_inr || 33.6).toFixed(2)}</b>
              </span>
            </div>

            <div>
              <Clock />
              <span>
                <small>{language === "mr" ? "विहित मुदत (RTS कायदा)" : "RTS Act Timeline"}</small>
                <b>
                  {service.processing_days || 15} {language === "mr" ? "कामकाजाचे दिवस" : "working days"}
                </b>
              </span>
            </div>

            <div>
              <MapPin />
              <span>
                <small>{language === "mr" ? "अधिकार क्षेत्र" : "Jurisdiction"}</small>
                <b>Maharashtra · All Districts</b>
              </span>
            </div>
          </div>

          <section className="content-panel">
            <h2>{language === "mr" ? "महत्त्वाची माहिती व मार्गदर्शक सूचना" : "Statutory Service Rules"}</h2>
            <p>
              {language === "mr"
                ? `महाराष्ट्र लोकसेवा हमी कायद्यानुसार (RTS) ही सेवा विहित वेळेत (${service.processing_days || 15} दिवस) मिळण्याची नागरिकांना हमी आहे. अधिकृत अर्जासाठी आपले सरकार पोर्टलवर लॉग इन करून विहित नमुन्यात कागदपत्रांसह अर्ज करावा.`
                : `Under the Maharashtra Right to Public Services Act (RTS), citizens are legally guaranteed delivery of this service within ${service.processing_days || 15} working days. Applications must be submitted through the official portal with digitally verified documents.`}
            </p>
            <div style={{ marginTop: "1rem" }}>
              <a
                href={portalUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="button button-outline"
                style={{ display: "inline-flex", alignItems: "center", gap: "0.5rem" }}
              >
                <span>{language === "mr" ? "आपले सरकार पोर्टलवर अर्ज करा" : "Apply on Aaple Sarkar"}</span>
                <ExternalLink size={16} />
              </a>
            </div>
          </section>

          <SourceList sources={service.sources} />
        </div>

        <aside className="journey-panel">
          <h3>{language === "mr" ? "पुढील पायऱ्या" : "Continue your journey"}</h3>

          <Link href={`/services/${slug}/documents`}>
            <span className="action-icon">
              <FileText />
            </span>
            <span>
              <b>{language === "mr" ? "कागदपत्र यादी (Checklist)" : "Document checklist"}</b>
              <small>{language === "mr" ? "लागणारी सर्व कागदपत्रे तपासा" : "Prepare verified documents"}</small>
            </span>
            <ArrowRight />
          </Link>

          <Link href={`/services/${slug}/guide`}>
            <span className="action-icon">
              <ListOrdered />
            </span>
            <span>
              <b>{language === "mr" ? "अर्ज प्रक्रिया (Guide)" : "Application guide"}</b>
              <small>{language === "mr" ? "पायरी-पायरीने अर्ज समजून घ्या" : "Step-by-step instructions"}</small>
            </span>
            <ArrowRight />
          </Link>

          <Link href={`/services/${slug}/eligibility`}>
            <span className="action-icon">
              <ClipboardCheck />
            </span>
            <span>
              <b>{language === "mr" ? "पात्रता पडताळणी" : "Check eligibility"}</b>
              <small>{language === "mr" ? "तुम्ही पात्र आहात का ते पहा" : "Review preliminary guidance"}</small>
            </span>
            <ArrowRight />
          </Link>

          <Link href="/assistant">
            <span className="action-icon">
              <MessageCircle />
            </span>
            <span>
              <b>{language === "mr" ? "सारथीला विचारा" : "Ask SAARTHI Voice AI"}</b>
              <small>{language === "mr" ? "थेट बोलून प्रश्न विचारा" : "Ask by typing or speaking"}</small>
            </span>
            <ArrowRight />
          </Link>
        </aside>
      </div>

      <Disclaimer />
    </div>
  );
}
