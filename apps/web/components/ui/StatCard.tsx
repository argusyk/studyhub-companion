import type { ReactNode } from "react";

interface Props {
  label: string;
  value: ReactNode;
  tone?: "default" | "success" | "warning";
}

const TONES = { default: "var(--sh-text)", success: "var(--sh-success)", warning: "var(--sh-warning)" };

export function StatCard({ label, value, tone = "default" }: Props) {
  return (
    <section
      aria-label={label}
      style={{ background: "var(--sh-surface)", border: "1px solid var(--sh-border)",
               borderRadius: "var(--sh-radius)", padding: "var(--sh-space-2)" }}
    >
      <div style={{ color: "var(--sh-muted)", fontSize: 13 }}>{label}</div>
      <div style={{ color: TONES[tone], fontSize: 34, fontWeight: 700 }}>{value}</div>
    </section>
  );
}
