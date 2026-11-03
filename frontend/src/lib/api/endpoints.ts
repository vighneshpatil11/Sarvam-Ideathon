export const endpoints = {
  health: "/health", services: "/services", service: (slug: string) => `/services/${encodeURIComponent(slug)}`,
  search: "/search", documents: (slug: string) => `/services/${encodeURIComponent(slug)}/documents`,
  questions: (slug: string) => `/services/${encodeURIComponent(slug)}/eligibility/questions`,
  evaluate: (slug: string) => `/services/${encodeURIComponent(slug)}/eligibility/evaluate`,
  steps: (slug: string) => `/services/${encodeURIComponent(slug)}/steps`, assistant: "/assistant/chat", feedback: "/feedback"
};
