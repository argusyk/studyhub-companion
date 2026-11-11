"""Подає JSON-події в hook через stdin. Команди з cases.json НЕ виконуються."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HOOK = ROOT / ".cursor" / "hooks" / "guard_shell.py"
CASES = Path(__file__).with_name("cases.json")


def run_hook(stdin_text: str, hook: Path = HOOK) -> tuple[str, int, str]:
    proc = subprocess.run([sys.executable, str(hook)], input=stdin_text, capture_output=True,
                          text=True, encoding="utf-8", timeout=20, cwd=ROOT)
    try:
        permission = json.loads(proc.stdout)["permission"]
    except (json.JSONDecodeError, KeyError):
        permission = "no-answer"
    return permission, proc.returncode, proc.stderr


def event_for(command: str) -> str:
    return json.dumps({"hook_event_name": "beforeShellExecution", "command": command,
                       "cwd": str(ROOT), "workspace_roots": [str(ROOT)]}, ensure_ascii=False)


def main() -> int:
    cases = json.loads(CASES.read_text("utf-8"))
    failed = 0
    for case in cases:
        got, code, _ = run_hook(event_for(case["command"]))
        ok = got == case["expect"] and (code == 2) == (got == "deny")
        failed += not ok
        if not ok:
            print(f"FAIL {case['id']}: очікувалось {case['expect']}, отримано {got} (код {code})")
    print(f"{len(cases) - failed}/{len(cases)} випадків пройдено")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
