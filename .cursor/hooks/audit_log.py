"""afterShellExecution: дописує виконану команду в .cursor/hooks/audit.log (без виводу команди)."""
import json
import sys
from datetime import datetime, timezone

from hook_io import read_event, workspace_root


def main() -> None:
    event = read_event()
    record = {"ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
              "command": str(event.get("command", ""))[:500], "cwd": event.get("cwd")}
    log = workspace_root(event) / ".cursor" / "hooks" / "audit.log"
    with open(log, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    sys.exit(0)


if __name__ == "__main__":
    main()
