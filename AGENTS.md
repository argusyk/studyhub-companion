# StudyHub

Сервіс обліку лабораторних робіт кафедри: студенти здають роботи, викладач
перевіряє й виставляє бали, бачить статистику групи.

## Стек
- apps/web – Next.js 15, TypeScript, Vitest, Playwright
- apps/api – FastAPI, Python 3.12, SQLAlchemy, Alembic, pytest
- БД – PostgreSQL (docker compose up db); CI – GitHub Actions

## Команди
- Встановлення API: `cd apps/api && python -m venv .venv && pip install -e ".[dev]"`
- API: `cd apps/api && uvicorn app.main:app --reload`
- Тести API: `cd apps/api && python -m pytest`
- Веб: `npm install` у корені, далі `npm run dev`; тести: `npm run test`
- Міграції: `cd apps/api && alembic revision --autogenerate -m "<опис>"`, `alembic upgrade head`

## Конвенції
- Змін без тестів не приймаємо; один коміт – одна змістова зміна.
- Гілки: feature/<коротко>; PR описує, що змінено і як перевірено.
- Типи обов'язкові: mypy для Python, strict для TypeScript.
- API: префікс `/api/v1`, одна сутність Submission (docs/taxonomy.md).

## Заборони
- Не читати й не змінювати .env та файли секретів.
- Не виконувати міграції на спільній БД; лише на локальній.
- Не змінювати вже злиті міграції.

## Де шукати
- Архітектура: docs/architecture.md, терміни: docs/taxonomy.md
- Бізнес-правила: docs/business-rules.md
- Модельна політика: docs/model-policy.md
