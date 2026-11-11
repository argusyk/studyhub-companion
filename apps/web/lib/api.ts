import type { Lab } from "@studyhub/shared";

// Єдина точка доступу до API: компоненти -> hooks -> lib/api.ts -> типи з packages/shared.
export const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

export async function apiGet<T>(path: string): Promise<T> {
  const resp = await fetch(`${API_URL}${path}`, { cache: "no-store" });
  if (!resp.ok) throw new Error(`GET ${path}: ${resp.status}`);
  return (await resp.json()) as T;
}

export const fetchLabs = () => apiGet<Lab[]>("/labs");
