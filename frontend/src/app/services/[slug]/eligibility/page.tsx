"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { ArrowLeft, ArrowRight, CircleHelp, CheckCircle2, AlertTriangle } from "lucide-react";
import { PageIntro, Disclaimer, ErrorState, EmptyState, SourceList } from "@/components/UI";
import { DEMO_MODE } from "@/lib/config";
import { demoQuestions } from "@/data/demo/service-details";
import { getEligibilityQuestions, evaluateEligibility } from "@/lib/api/eligibility";
import { useApp } from "@/context/AppContext";
import type { EligibilityResult, Question } from "@/types";

const labelsEn: Record<EligibilityResult["status"], string> = {
  potentially_eligible: "You may be eligible",
  potentially_not_eligible: "You may not meet the listed conditions",
  more_information_required: "More information is needed",
  unable_to_determine: "We could not determine this",
};

const labelsMr: Record<EligibilityResult["status"], string> = {
  potentially_eligible: "तुम्ही प्राथमिकदृष्ट्या पात्र आहात",
  potentially_not_eligible: "काही आवश्यक अटी अपूर्ण असू शकतात",
  more_information_required: "अधिक माहिती आवश्यक आहे",
  unable_to_determine: "पात्रता ठरवता आली नाही",
};

export default function EligibilityPage() {
  const { slug } = useParams<{ slug: string }>();
  const { language, t } = useApp();
  const [questions, setQuestions] = useState<Question[]>(DEMO_MODE ? demoQuestions : []);
  const [answers, setAnswers] = useState<Record<string, string | number | boolean>>({});
  const [result, setResult] = useState<EligibilityResult | null>(null);
  const [loading, setLoading] = useState(!DEMO_MODE);
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (!DEMO_MODE) {
      setLoading(true);
      setError("");
      getEligibilityQuestions(slug, language)
        .then((r) => setQuestions(r.questions || []))
        .catch((e) => setError(e.message))
        .finally(() => setLoading(false));
    }
  }, [slug, language]);

  function update(id: string, value: string | number | boolean) {
    setAnswers((a) => ({ ...a, [id]: value }));
  }

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (questions.some((q) => q.required && answers[q.id] === undefined)) {
      setError(
        language === "mr"
          ? "कृपया सर्व अनिवार्य प्रश्नांची उत्तरे द्या."
          : "Please answer all required questions."
      );
      return;
    }
    setError("");
    if (DEMO_MODE) {
      setResult({
        status: "unable_to_determine",
        summary: "Demo mode does not evaluate eligibility.",
        explanation:
          "This sample form demonstrates the interaction only. Connect the backend to receive verified statutory evaluation.",
      });
      return;
    }

    setSubmitting(true);
    try {
      const res = await evaluateEligibility(slug, answers, language);
      setResult(res);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Unable to evaluate answers.");
    } finally {
      setSubmitting(false);
    }
  }

  const serviceTitle = slug.replaceAll("-", " ");
  const statusLabels = language === "mr" ? labelsMr : labelsEn;

  return (
    <div className="container page-container">
      <div className="breadcrumbs">
        <Link href={`/services/${slug}`}>{serviceTitle}</Link>
        <span>/</span>
        <span>{language === "mr" ? "पात्रता पडताळणी" : "Eligibility"}</span>
      </div>

      <PageIntro
        eyebrow={language === "mr" ? "प्राथमिक मार्गदर्शन" : "PRELIMINARY GUIDANCE"}
        title={language === "mr" ? "पात्रता पडताळणी" : "Explore eligibility"}
        description={
          language === "mr"
            ? "काही सोप्या प्रश्नांची उत्तरे देऊन तुम्ही या सेवेसाठी पात्र आहात का ते त्वरित तपासा."
            : "Answer the preliminary questions to verify your eligibility under Maharashtra Government rules."
        }
      />

      {loading ? (
        <div className="skeleton-card wide" />
      ) : error && !questions.length ? (
        <ErrorState message={error} />
      ) : questions.length ? (
        <div className="form-panel">
          <div className="form-panel-heading">
            <CircleHelp />
            <div>
              <h2>{language === "mr" ? "काही मूलभूत प्रश्न" : "Preliminary questions"}</h2>
              <p>
                {language === "mr"
                  ? "तारांकित (*) केलेले सर्व प्रश्न सोडवणे अनिवार्य आहे."
                  : "Fields marked required (*) must be completed."}
              </p>
            </div>
          </div>

          <form onSubmit={submit} className="eligibility-form">
            {questions.map((q) => (
              <div className="question-block" key={q.id}>
                <label className="question-label" htmlFor={q.id}>
                  {q.label}
                  {q.required && <span> *</span>}
                </label>
                {q.description && <p className="question-hint">{q.description}</p>}
                {q.type === "boolean" ? (
                  <select
                    id={q.id}
                    value={answers[q.id] === undefined ? "" : String(answers[q.id])}
                    onChange={(e) => update(q.id, e.target.value === "true")}
                  >
                    <option value="">{language === "mr" ? "पर्याय निवडा" : "Select an answer"}</option>
                    <option value="true">{language === "mr" ? "होय (Yes)" : "Yes"}</option>
                    <option value="false">{language === "mr" ? "नाही (No)" : "No"}</option>
                  </select>
                ) : q.type === "single_choice" ? (
                  <select
                    id={q.id}
                    value={String(answers[q.id] ?? "")}
                    onChange={(e) => update(q.id, e.target.value)}
                  >
                    <option value="">{language === "mr" ? "पर्याय निवडा" : "Select an option"}</option>
                    {q.options?.map((o) => (
                      <option value={o.value} key={o.value}>
                        {o.label}
                      </option>
                    ))}
                  </select>
                ) : (
                  <input
                    id={q.id}
                    type={q.type === "number" ? "number" : "text"}
                    value={String(answers[q.id] ?? "")}
                    onChange={(e) =>
                      update(q.id, q.type === "number" ? Number(e.target.value) : e.target.value)
                    }
                  />
                )}
              </div>
            ))}

            {error && (
              <p className="inline-error" role="alert">
                {error}
              </p>
            )}

            <button className="button button-primary" disabled={submitting}>
              {submitting
                ? language === "mr"
                  ? "पडताळणी करत आहे…"
                  : "Checking…"
                : language === "mr"
                ? "पात्रता तपासा"
                : "Check Eligibility"}
              <ArrowRight size={17} />
            </button>
          </form>
        </div>
      ) : (
        <EmptyState
          title={language === "mr" ? "पात्रतेचे प्रश्न उपलब्ध नाहीत" : "Eligibility questions are not available"}
          message={
            language === "mr"
              ? "या सेवेसाठी प्रश्न लोड केले जात आहेत."
              : "The connected backend has not supplied questions for this service yet."
          }
        />
      )}

      {result && (
        <section className="result-panel">
          <div className="result-kicker">
            {language === "mr" ? "प्राथमिक निकाल" : "PRELIMINARY RESULT"}
          </div>
          <h2>{statusLabels[result.status]}</h2>
          <p>{result.summary || result.explanation}</p>
          {result.explanation && result.summary && <p>{result.explanation}</p>}
          {result.missing_information?.length ? (
            <div>
              <b>{language === "mr" ? "आवश्यक पूरक माहिती" : "Additional information needed"}</b>
              <ul>
                {result.missing_information.map((x, i) => (
                  <li key={i}>{x}</li>
                ))}
              </ul>
            </div>
          ) : null}
          <Disclaimer>{t("preliminary")}</Disclaimer>
          <SourceList sources={result.sources} />
        </section>
      )}

      <Disclaimer>{t("preliminary")}</Disclaimer>
      <Link href={`/services/${slug}`} className="back-link">
        <ArrowLeft size={16} /> {language === "mr" ? "सेवेकडे परत जा" : "Back to service"}
      </Link>
    </div>
  );
}
