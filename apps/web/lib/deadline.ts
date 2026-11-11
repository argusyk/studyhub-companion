const TZ = "Europe/Kyiv";

/** "2026-04-19T20:59:00Z" -> "19.04.2026 23:59" за часом кафедри. */
export function formatDeadline(iso: string): string {
  const parts = new Intl.DateTimeFormat("uk-UA", {
    timeZone: TZ, day: "2-digit", month: "2-digit", year: "numeric",
    hour: "2-digit", minute: "2-digit", hourCycle: "h23",
  }).formatToParts(new Date(iso));
  const get = (t: string) => parts.find((p) => p.type === t)?.value ?? "";
  return `${get("day")}.${get("month")}.${get("year")} ${get("hour")}:${get("minute")}`;
}

/** Скільки повних діб лишилось до дедлайну (від'ємне – прострочено). */
export function daysLeft(iso: string, now: Date): number {
  return Math.floor((new Date(iso).getTime() - now.getTime()) / 86_400_000);
}
