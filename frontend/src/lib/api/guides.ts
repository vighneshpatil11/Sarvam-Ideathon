import { apiRequest } from "./client";
import { endpoints } from "./endpoints";
import type { ApplicationStep, Source, Language } from "@/types";

export const getGuide = (slug: string, language?: Language) =>
  apiRequest<{ steps: ApplicationStep[]; fees?: unknown[]; processing_time?: string | null; sources?: Source[] }>(
    `${endpoints.steps(slug)}${language ? `?language=${language}` : ""}`
  );
