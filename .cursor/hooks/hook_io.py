"""Адаптер протоколу hooks Cursor.

Вхід: один JSON-документ у stdin. Для beforeShellExecution це, зокрема, поля
`command`, `cwd`, `workspace_roots`. Відповідь: JSON у stdout з полем `permission`
(`allow` | `deny` | `ask`) та необов'язковими `user_message` і `agent_message`.
Код завершення 2 також означає «заборонити». Формат може змінюватися між версіями
Cursor: після оновлення звіряйте його з документацією й запускайте
`python -m pytest tools/hooks_testkit`.
"""
import json
import os
import sys
from pathlib import Path


def read_event() -> dict:
    """Читає JSON зі stdin; при порожньому чи зіпсованому вході повертає {}."""
    raw = sys.stdin.buffer.read().decode("utf-8-sig", errors="replace").strip()
    if not raw:
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def workspace_root(event: dict | None = None) -> Path:
    roots = (event or {}).get("workspace_roots") or []
    if roots:
        return Path(roots[0])
    env = os.environ.get("CURSOR_PROJECT_DIR")
    if env:
        return Path(env)
    return Path(__file__).resolve().parents[2]  # .cursor/hooks/hook_io.py -> корінь репозиторію


def _emit(payload: dict, code: int = 0) -> None:
    # ASCII-екранування: безпечно для будь-якої кодової сторінки stdout у Windows
    sys.stdout.write(json.dumps(payload))
    sys.stdout.flush()
    sys.exit(code)


def allow() -> None:
    _emit({"permission": "allow"})


def ask(message: str) -> None:
    _emit({"permission": "ask", "user_message": message, "agent_message": message})


def deny(message: str) -> None:
    _emit({"permission": "deny", "user_message": message, "agent_message": message}, code=2)
