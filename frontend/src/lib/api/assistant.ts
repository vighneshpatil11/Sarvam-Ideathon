import { apiRequest } from "./client";
import { endpoints } from "./endpoints";
import type { AssistantResponse, Language } from "@/types";

export type ChatRole = "user" | "assistant";
export interface ChatHistoryMessage {
  role: ChatRole;
  content: string;
}

export const sendAssistantMessage = (
  message: string,
  language: Language,
  sessionId?: string | null,
  serviceSlug?: string,
  history?: ChatHistoryMessage[]
) =>
  apiRequest<AssistantResponse>(endpoints.assistant, {
    method: "POST",
    body: JSON.stringify({
      message,
      session_id: sessionId ?? null,
      language,
      context: serviceSlug ? { service_slug: serviceSlug } : {},
      history: history ?? [],
    }),
  });
