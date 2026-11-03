import { API_BASE_URL } from "@/lib/config";
export class ApiError extends Error {
  status: number; code?: string; details?: unknown;
  constructor(message: string, status: number, code?: string, details?: unknown) { super(message); this.name = "ApiError"; this.status = status; this.code = code; this.details = details; }
}
export async function apiRequest<T>(path: string, options: RequestInit = {}): Promise<T> {
  const url = `${API_BASE_URL}${path.startsWith("/") ? path : `/${path}`}`;
  let response: Response;
  try {
    response = await fetch(url, { ...options, headers: { ...(options.body ? { "Content-Type": "application/json" } : {}), ...options.headers } });
  } catch {
    throw new ApiError("Cannot connect to SAARTHI services. Check that the backend is running.", 0, "NETWORK_ERROR");
  }
  let payload: unknown;
  try { payload = await response.json(); } catch { throw new ApiError("The server returned an unreadable response.", response.status, "INVALID_RESPONSE"); }
  const body = payload as { success?: boolean; data?: T; error?: { message?: string; code?: string; details?: unknown } };
  if (!response.ok || body?.success === false) throw new ApiError(body?.error?.message || "The request could not be completed.", response.status, body?.error?.code, body?.error?.details);
  if (body && body.success === true && "data" in body) return body.data as T;
  return payload as T;
}
