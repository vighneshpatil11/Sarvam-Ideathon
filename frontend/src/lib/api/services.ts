import { apiRequest } from "./client"; import { endpoints } from "./endpoints"; import type { Service, ServiceList, Language } from "@/types";
export const listServices = (language?: Language) => apiRequest<ServiceList>(`${endpoints.services}${language ? `?language=${language}` : ""}`);
export const getService = (slug: string, language?: Language) => apiRequest<Service>(`${endpoints.service(slug)}${language ? `?language=${language}` : ""}`);
