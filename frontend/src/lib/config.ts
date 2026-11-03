export const API_BASE_URL = (
  process.env.BACKEND_SERVICE_URL
    ? `${process.env.BACKEND_SERVICE_URL.replace(/\/$/, "")}/api/v1`
    : (process.env.NEXT_PUBLIC_API_BASE_URL || "/api/v1")
).replace(/\/$/, "");

export const DEMO_MODE = process.env.NEXT_PUBLIC_DEMO_MODE === "true";
