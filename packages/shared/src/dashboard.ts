import example from "./dashboard.example.json";

export type CellStatus = "submitted" | "reviewed" | "returned" | "missing";

export interface DashboardCell {
  labNumber: number;
  score: number | null;
  status: CellStatus;
  isLate: boolean;
}

export interface DashboardData {
  group: string;
  labs: { number: number; title: string }[];
  rows: { student: string; cells: DashboardCell[] }[];
  stats: { average: number; submitted: number; total: number; late: number };
}

// Навчальні дані для ЛР8 (поки немає ендпоінта статистики групи).
export const dashboardExample = example as DashboardData;
