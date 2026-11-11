# Задача B: експорт оцінок групи в CSV (worktree 2)

`GET /api/v1/groups/{group}/grades.csv` повертає `text/csv; charset=utf-8` з BOM (Excel),
роздільник `;`, колонки: студент, лабораторна, бал, штраф %, запізнення (діб).
**Зона файлів:** `apps/api/app/exports/**`, `apps/api/app/routers/exports.py`,
`apps/api/tests/exports/**`; єдина зміна поза зоною – рядок `include_router` у `main.py`.
УВАГА: каталог `apps/api/app/exports/` має потрапляти в git (перевірте `.gitignore`).
Захист від CSV-ін'єкцій: значення, що починаються з `=`, `+`, `-`, `@`, екрануються.
