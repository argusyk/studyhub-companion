"""beforeMCPExecution: дозволяє лише інструменти читання (allowlist); решту відхиляє.

Поля події (`tool_name`, `tool_input`) звіряйте з документацією hooks вашої версії Cursor.
Для execute_sql додатково перевіряється, що це один оператор читання. Це допоміжний шар:
основа захисту – роль studyhub_ro і режим --access-mode=restricted.
"""
import re

from hook_io import allow, deny, read_event

ALLOWED_TOOLS = {"get_schedule", "find_free_slot",  # studyhub-schedule
                 "list_schemas", "list_objects", "get_object_details",  # postgres-mcp, читання
                 "execute_sql", "explain_query"}
READ_SQL = re.compile(r"^\s*(select|with|explain|show)\b", re.IGNORECASE)
WRITE_WORDS = re.compile(r"\b(insert|update|delete|drop|alter|create|truncate|grant|revoke|copy)\b",
                         re.IGNORECASE)


def main() -> None:
    event = read_event()
    tool = event.get("tool_name") or event.get("toolName") or ""
    if tool not in ALLOWED_TOOLS:
        deny(f"MCP-інструмент {tool!r} не входить до allowlist (лише читання).")
    if tool == "execute_sql":
        raw = event.get("tool_input") or {}
        if isinstance(raw, str):
            raw = {"sql": raw}
        sql = str(raw.get("sql", "")).strip().rstrip(";")
        if ";" in sql or not READ_SQL.match(sql) or WRITE_WORDS.search(sql):
            deny("execute_sql: дозволений лише один оператор читання (SELECT/WITH/EXPLAIN/SHOW).")
    allow()


if __name__ == "__main__":
    main()
