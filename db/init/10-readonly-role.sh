#!/bin/sh
# Виконується ОДИН раз при створенні тому PostgreSQL (docker-entrypoint-initdb.d).
# Створює користувача studyhub_ro лише для читання (для Postgres-MCP, ЛР11).
set -e
if [ -z "$STUDYHUB_RO_PASSWORD" ]; then
  echo "STUDYHUB_RO_PASSWORD не задано: роль studyhub_ro не створюється"
  exit 0
fi
psql -v ON_ERROR_STOP=1 -v ropass="$STUDYHUB_RO_PASSWORD" -v dbname="$POSTGRES_DB" \
     --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<'SQL'
CREATE ROLE studyhub_ro LOGIN PASSWORD :'ropass';
GRANT CONNECT ON DATABASE :"dbname" TO studyhub_ro;
GRANT USAGE ON SCHEMA public TO studyhub_ro;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO studyhub_ro;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO studyhub_ro;
ALTER ROLE studyhub_ro SET default_transaction_read_only = on;
SQL
