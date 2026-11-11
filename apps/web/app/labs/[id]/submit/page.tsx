"use client";
import { useParams } from "next/navigation";
import { useState } from "react";
import { useSubmitLab } from "../../../../lib/hooks/useSubmitLab";

export default function SubmitPage() {
  const params = useParams<{ id: string }>();
  const labId = Number(params.id);
  const { submit, result, error, pending } = useSubmitLab(labId);
  const [studentId, setStudentId] = useState("1");
  const [file, setFile] = useState<File | null>(null);

  return (
    <main>
      <h1>Здати лабораторну №{labId}</h1>
      <form
        onSubmit={(e) => {
          e.preventDefault();
          void submit(Number(studentId), file);
        }}
      >
        <p>
          <label htmlFor="student">Ідентифікатор студента (навчальне спрощення)</label>
          <br />
          <input id="student" type="number" min={1} value={studentId}
                 onChange={(e) => setStudentId(e.target.value)} required />
        </p>
        <p>
          <label htmlFor="file">Файл звіту (до 10 МБ)</label>
          <br />
          <input id="file" type="file" onChange={(e) => setFile(e.target.files?.[0] ?? null)} />
        </p>
        <button type="submit" disabled={pending}>
          {pending ? "Надсилання…" : "Здати"}
        </button>
      </form>
      {error && <p role="alert">{error}</p>}
      {result && <p role="status">Прийнято: {result.filename} (№{result.id})</p>}
    </main>
  );
}
