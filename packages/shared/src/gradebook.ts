// Перенесено з legacy/static/js/gradebook.js (ЛР10, крок 4) зі збереженням поведінки.

/** Увага (Сумнівно: так): знаменник включає порожні (null) оцінки, як у legacy. */
export function average(grades: Array<number | null>): number {
  let sum = 0;
  for (const g of grades) {
    if (g !== null) sum += g;
  }
  return grades.length ? Math.round((sum / grades.length) * 10) / 10 : 0;
}

export function lateBadge(days: number): string {
  if (days === 0) return "";
  if (days > 5) return "Не приймається";
  return `Запізно на ${days} д.`;
}

export function formatScore(x: number | null): string {
  return x === null ? "–" : String(x);
}
