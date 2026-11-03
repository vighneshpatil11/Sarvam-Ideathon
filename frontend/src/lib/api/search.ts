import { apiRequest } from "./client"; import { endpoints } from "./endpoints"; import type { Language, ServiceList } from "@/types";
export const searchServices = (query: string, language: Language) => apiRequest<ServiceList>(endpoints.search, { method: "POST", body: JSON.stringify({ query, language, state: "Maharashtra", district: "Pune" }) });
