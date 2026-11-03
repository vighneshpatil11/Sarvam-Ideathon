import { apiRequest } from "./client"; import { endpoints } from "./endpoints"; import type { ApplicationStep, Source } from "@/types";
export const getGuide = (slug: string) => apiRequest<{ steps: ApplicationStep[]; fees?: unknown[]; processing_time?: string | null; sources?: Source[] }>(endpoints.steps(slug));
