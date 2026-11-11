# Postgres-MCP для StudyHub (ЛР11)

Використовуємо наявний community-сервер **Postgres MCP Pro** (пакет PyPI `postgres-mcp`,
репозиторій github.com/crystaldba/postgres-mcp, ліцензія MIT). Запуск: `uvx postgres-mcp`
(потрібен `uv`) або Docker-образ `crystaldba/postgres-mcp`. Рядок підключення передається в
змінній оточення `DATABASE_URI`.

Для навчального сервісу вмикайте режим `--access-mode=restricted` (лише читання транзакції
й ліміт часу запиту) І додатково підключайтеся під роллю `studyhub_ro` з правом лише SELECT.
Роль створює `db/init/10-readonly-role.sh` при першому старті `docker compose up db`
(потрібна змінна `STUDYHUB_RO_PASSWORD` у `.env`). Для вже створеного тому виконайте SQL
з цього скрипта вручну або `docker compose down -v` (це видалить дані).

Версію пакета перед використанням закріпіть (`uvx postgres-mcp==<версія>`) і перевірте
актуальність параметрів у README пакета [перевірено: дата]. Дані студентів у реальному
сервісі потрібно знеособити (розд. 17); у навчальному репозиторії дані вигадані.
