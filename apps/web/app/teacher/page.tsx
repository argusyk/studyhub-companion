import { dashboardExample } from "@studyhub/shared";
import { GradesTable } from "../../components/GradesTable";
import { StatCard } from "../../components/ui/StatCard";

export default function TeacherDashboard() {
  const data = dashboardExample;
  return (
    <main>
      <h1>Дашборд викладача · група {data.group.toUpperCase()}</h1>
      <div style={{ display: "grid", gap: "var(--sh-space-2)", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))" }}>
        <StatCard label="Середній бал групи" value={data.stats.average.toString().replace(".", ",")} />
        <StatCard label="Здано робіт" value={`${data.stats.submitted} / ${data.stats.total}`} tone="success" />
        <StatCard label="Із запізненням" value={data.stats.late} tone="warning" />
      </div>
      <div style={{ background: "var(--sh-surface)", border: "1px solid var(--sh-border)",
                    borderRadius: "var(--sh-radius)", padding: "var(--sh-space-2)", marginTop: "var(--sh-space-3)" }}>
        <GradesTable data={data} />
      </div>
    </main>
  );
}
