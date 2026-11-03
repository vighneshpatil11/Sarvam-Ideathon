import { apiRequest } from "./client";
import { endpoints } from "./endpoints";
import type { EligibilityResult, Language, Question } from "@/types";

export const getEligibilityQuestions = (slug: string, language?: Language) =>
  apiRequest<{ questions: Question[] }>(
    `${endpoints.questions(slug)}${language ? `?language=${language}` : ""}`
  );

export const evaluateEligibility = (
  slug: string,
  answers: Record<string, string | number | boolean>,
  language: Language
) =>
  apiRequest<EligibilityResult>(endpoints.evaluate(slug), {
    method: "POST",
    body: JSON.stringify({ answers, language }),
  });
