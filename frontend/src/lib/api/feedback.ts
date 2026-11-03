import { apiRequest } from "./client"; import { endpoints } from "./endpoints";
export const submitFeedback = (rating: number, comment: string, page: string) => apiRequest<{ received: boolean }>(endpoints.feedback, { method: "POST", body: JSON.stringify({ rating, comment, page }) });
