import { demoServices } from "./services";
import type { Question, ServiceDocument, ApplicationStep } from "@/types";
export const getDemoService = (slug: string) => demoServices.find((item) => item.slug === slug);
export const demoQuestions: Question[] = [
  { id: "need_context", label: "What would you like help understanding?", description: "This sample question demonstrates the form only; it does not determine eligibility.", type: "single_choice", required: true, options: [{ value: "requirements", label: "Requirements" }, { value: "process", label: "Application process" }, { value: "sources", label: "Official sources" }] }
];
export const demoDocuments: ServiceDocument[] = [];
export const demoSteps: ApplicationStep[] = [];
