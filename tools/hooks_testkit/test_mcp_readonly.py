import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))
from run_cases import ROOT, run_hook  # noqa: E402

HOOK = ROOT / ".cursor" / "hooks" / "mcp_readonly.py"


def ev(tool, **inp):
    return json.dumps({"hook_event_name": "beforeMCPExecution", "tool_name": tool, "tool_input": inp})


@pytest.mark.parametrize("tool,inp,expect", [
    ("get_schedule", {"group": "ПІ-22а", "week": 7}, "allow"),
    ("find_free_slot", {"teacher": "Коваленко О. М."}, "allow"),
    ("execute_sql", {"sql": "SELECT count(*) FROM submissions"}, "allow"),
    ("execute_sql", {"sql": "DROP TABLE submissions"}, "deny"),
    ("execute_sql", {"sql": "SELECT 1; DELETE FROM grades"}, "deny"),
    ("execute_sql", {"sql": "WITH x AS (DELETE FROM grades RETURNING *) SELECT * FROM x"}, "deny"),
    ("book_room", {"room": "3.214"}, "deny"),
    ("", {}, "deny"),
])
def test_mcp_policy(tool, inp, expect):
    got, code, _ = run_hook(ev(tool, **inp), hook=HOOK)
    assert got == expect and (code == 2) == (got == "deny")
