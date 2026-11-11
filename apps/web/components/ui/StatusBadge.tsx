import type { DashboardCell } from "@studyhub/shared";

export function badgeFor(cell: DashboardCell): { text: string; bg: string; fg: string } | null {
  if (cell.status === "missing") return { text: "Не здано", bg: "var(--sh-neutral-bg)", fg: "var(--sh-muted)" };
  if (cell.status === "returned") return { text: "Повернено", bg: "var(--sh-danger-bg)", fg: "var(--sh-danger)" };
  if (cell.isLate) return { text: `Запізно: ${cell.score ?? "–"}`, bg: "var(--sh-warning-bg)", fg: "var(--sh-warning)" };
  return null;
}

export function StatusBadge({ cell }: { cell: DashboardCell }) {
  const badge = badgeFor(cell);
  if (!badge) return <>{cell.score}</>;
  return (
    <span style={{ background: badge.bg, color: badge.fg, borderRadius: 12,
                   padding: "2px var(--sh-space-1)", fontSize: 12 }}>
      {badge.text}
    </span>
  );
}
