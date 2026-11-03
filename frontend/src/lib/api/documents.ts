import { apiRequest } from "./client";
import { endpoints } from "./endpoints";
import type { ServiceDocument, Language } from "@/types";

export const getDocuments = (slug: string, language?: Language) =>
  apiRequest<{ documents: ServiceDocument[] }>(
    `${endpoints.documents(slug)}${language ? `?language=${language}` : ""}`
  );
