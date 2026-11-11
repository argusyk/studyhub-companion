import { fetchLabs } from "../lib/api";

export const dynamic = "force-dynamic";

export default async function Home() {
  let labs: Awaited<ReturnType<typeof fetchLabs>> = [];
  let error: string | null = null;
  try {
    labs = await fetchLabs();
  } catch (e) {
    error = e instanceof Error ? e.message : "Помилка";
  }
  return (
    <main>
      <h1>StudyHub</h1>
      {error && <p role="alert">API недоступне: {error}</p>}
      <ul>
        {labs.map((lab) => (
          <li key={lab.id}>
            ЛР{lab.number}. {lab.title}
          </li>
        ))}
      </ul>
    </main>
  );
}
