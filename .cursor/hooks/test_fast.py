"""stop: запускає швидкі тести; при падінні повертає агентові followup_message (не exit code).

Cursor передає агентові зворотний зв'язок із hook лише через JSON `followup_message`;
`loop_limit` у hooks.json і `loop_count` у вході обмежують кількість повторів.
"""
import json
import subprocess
import sys

from hook_io import read_event, workspace_root

MAX_LOOPS = 3


def main() -> None:
    event = read_event()
    if event.get("status", "completed") != "completed" or event.get("loop_count", 0) >= MAX_LOOPS:
        sys.exit(0)
    api = workspace_root(event) / "apps" / "api"
    try:
        proc = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider"],
                              cwd=api, capture_output=True, encoding="utf-8", errors="replace", timeout=100)
    except subprocess.TimeoutExpired:
        print(json.dumps({"followup_message": "Швидкі тести не вклалися в 100 с: скоротіть набір."},
                         ))
        sys.exit(0)
    if proc.returncode not in (0, 5):  # 5 – тестів не знайдено
        tail = "\n".join((proc.stdout + proc.stderr).strip().splitlines()[-15:])
        print(json.dumps({"followup_message":
                          f"python -m pytest впав. Виправ причину, не послаблюючи тести:\n{tail}"},
                         ))
    sys.exit(0)


if __name__ == "__main__":
    main()
