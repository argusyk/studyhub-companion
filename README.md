# StudyHub – навчальний репозиторій до посібника

Супровідний репозиторій до навчального посібника «Розробка програмного забезпечення з Cursor».
Репозиторій: https://github.com/argusyk/studyhub-companion. Усі дані вигадані; реальних студентів і секретів тут немає.

StudyHub – сервіс обліку лабораторних робіт кафедри: студент здає роботу, викладач
перевіряє й ставить бал, бачить статистику групи. Репозиторій побудований так, щоб кожна з
12 лабораторних робіт Додатка Г мала **стартову точку** (git-тег `lab-N-start`).
Еталонні розв'язання зберігаються в окремому приватному репозиторії для викладачів (https://github.com/argusyk/studyhub-solutions).
Кожен `lab-N-start` містить стан, досягнутий наприкінці ЛР N−1.

## Структура

```text
apps/api/            FastAPI (Python 3.12+), SQLAlchemy 2, Alembic, pytest
apps/web/            Next.js 15 + TypeScript, Vitest
packages/shared/     спільні TypeScript-типи й чисті функції
legacy/              старий Flask-прототип «зі смородом» (ЛР10)
tools/schedule_mcp/  власний MCP-сервер «розклад кафедри» (ЛР11)
tools/hooks_testkit/ тест-набір для hooks без виконання небезпечних команд (вправа 17.6, ЛР11)
agents/checker/      каркас агента перевірки звітів + eval-набір (ЛР12)
.cursor/             rules/*.mdc, skills, agents, hooks, mcp.json, BUGBOT.md, worktrees.json
data/seed/           seed-дані (студенти, лабораторні); data/schedule.json – розклад
docs/                taxonomy, business-rules, specs, templates, design (макет), threat-model, tasks
db/init/             ініціалізація PostgreSQL (роль studyhub_ro лише для читання)
```

## Швидкий старт

Потрібні: Git, Python 3.12+, Node.js 22+, Docker (для PostgreSQL; для тестів не потрібен).

```bash
cp .env.example .env                       # Windows PowerShell: Copy-Item .env.example .env
cd apps/api
python -m venv .venv                       # активуйте: .venv/bin/activate або .venv\Scripts\Activate.ps1
pip install -e ".[dev]"
python -X utf8 -m pytest                   # тести (SQLite in-memory, PostgreSQL не потрібен)
python -m app.seed                         # seed у локальний SQLite (або у БД з DATABASE_URL)
uvicorn app.main:app --reload              # http://localhost:8000/docs
```

База PostgreSQL: `docker compose up db` (змініть `POSTGRES_PASSWORD` у `.env`), далі
`DATABASE_URL=postgresql+psycopg://...` і `alembic upgrade head` у `apps/api`.
Веб: у корені `npm install`, потім `npm run dev` (http://localhost:3000), `npm run test`, `npm run typecheck`.

Інші перевірки (з кореня репозиторію): `python -m pytest legacy/tests tools agents`
(потрібні `pip install flask "mcp[cli]"`).

## Як перемикатися між етапами лабораторних

```bash
git tag                                     # усі етапи
git switch -c my-lab-3 lab-3-start          # власна гілка від стартової точки ЛР3
```

| ЛР | Тег старту | Що є на старті | Що здається |
|---|---|---|---|
| 1 | `lab-1-start` | порожнє монорепо, `.gitignore`, `.env.example`, `docker-compose.yml` | структура, `.cursorignore`, звіт |
| 2 | `lab-2-start` | FastAPI-каркас: `/api/v1/health`, `/api/v1/labs`, моделі Student/Lab, seed, тести | фільтри списку лабораторних, `docs/model-policy.md` |
| 3 | `lab-3-start` | + фільтри `labs` | модель `Submission`, схеми Pydantic, тест валідації |
| 4 | `lab-4-start` | + `Submission`, `docs/architecture.md` | `docs/taxonomy.md`, звіт про контекст |
| 5 | `lab-5-start` | + Alembic 0001, скелет Next.js, `packages/shared` | `POST /api/v1/labs/{id}/submissions`, міграція 0002, сторінка здачі |
| 6 | `lab-6-start` | робочий потік здачі | `.cursor/rules`, `AGENTS.md`, skill «нова міграція» |
| 7 | `lab-7-start` | + шаблони PRD/spec/plan/todo | модуль оцінювання за специфікацією, правило R-07 |
| 8 | `lab-8-start` | + макет `docs/design/dashboard-mockup.svg`, приклад даних | дашборд викладача, `design-system.mdc` |
| 9 | `lab-9-start` | **навмисний баг** `is_late` (naive datetime, пояс Києва), xfail-тест, `scripts/repro_deadline_bug.py` | виправлення кореневої причини, регресійний тест, hooks |
| 10 | `lab-10-start` | `legacy/` (Flask), фікстури й знімок `ki21_golden.json` | характеризаційні тести, перенесені ендпоінти, `docs/business-rules.md`, TS-модуль |
| 11 | `lab-11-start` | `guard_shell.py`, `tools/hooks_testkit`, `data/schedule.json`, роль `studyhub_ro` | MCP-сервер розкладу, `mcp.json`, threat model, протокол ін'єкції |
| 12 | `lab-12-start` | задачі A/B/C для worktrees, eval-випадки, `tools/test_gitignore.py` | три фічі, CI/Bugbot, агент з eval, протокол експерименту |

Гілка `main` = `lab-12-start` + цей README. Теги `lab-N-start` – «що видає викладач».

## Канонічні рішення

- Одна сутність **Submission**: `id, student_id, lab_id, submitted_at (UTC), file_url, filename,
  size_bytes, status (submitted|reviewed|returned), score (0..100|null), is_late`. Розрахунок оцінки – у `Grade`.
- Усі шляхи API мають префікс **`/api/v1`**, його задає `app/main.py`.
- Правило штрафу за запізнення має єдиний ідентифікатор **R-07** (`docs/business-rules.md`):
  10 % від бала за календарну добу (за Києвом), не більше 30 %.
- Шари бекенду: `routers -> services -> Session` (без `repositories`).
- Час: у БД лише aware UTC (`UtcDateTime`); перетворення в `Europe/Kyiv` на межі API.
- Постачальник Postgres-MCP: PyPI-пакет `postgres-mcp` (crystaldba, MIT), див. `docs/postgres-mcp.md`.

## Hooks і безпека

`.cursor/hooks/guard_shell.py` читає JSON зі stdin (поле `command`), відповідає
`{"permission": "allow|deny|ask"}` і кодом 2 при забороні; залежить лише від `hook_io.py`.
Блокує `rm --recursive`, `rm -fr`, `Remove-Item -Recurse`, `rd /s`, `find -delete`, `rmtree`,
`git push --force`, `curl | sh`, читання `.env` тощо; рекурсивне видалення дозволене лише для кешів
(`node_modules`, `.next`, `dist`, …). Перевірка без виконання команд:
`python -m pytest tools/hooks_testkit`. Це допоміжний шар, а не межа безпеки (розд. 17).

## MCP-сервер розкладу

`pip install "mcp[cli]"`, потім `python tools/schedule_mcp/server.py` (stdio) або через `.cursor/mcp.json`.
Cursor має запускати `python` із venv, де встановлено `mcp` (або вкажіть абсолютний шлях у `command`).
Сервер сумісний з `mcp` 1.x (`FastMCP`) і 2.x (`MCPServer`). Користувача БД для `postgres-mcp`
створює `db/init/10-readonly-role.sh` (змінна `STUDYHUB_RO_PASSWORD`).

## Відомі обмеження

- Файли міграцій мають короткі імена (`0002_subm.py`, `0003_grade.py`, `0004_late.py`), а деякі
  каталоги тестів скорочені (`tests/moodle`, `tests/notif`) – щоб не перевищити ліміт довжини шляху Windows.
- Vitest-тести й `npm run typecheck` перевірені на Node 24; Playwright-сценарії не додано.
- Формати `permissions.json` та `hooks.json` звірте з документацією вашої версії Cursor.
- Ціни, токени й дати у `docs/model-policy.md` та протоколах – заповнювані [плейсхолдери].
