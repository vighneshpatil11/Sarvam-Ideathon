import { apiRequest } from "./client"; import { endpoints } from "./endpoints"; import type { ServiceDocument } from "@/types";
export const getDocuments = (slug: string) => apiRequest<{ documents: ServiceDocument[] }>(endpoints.documents(slug));
