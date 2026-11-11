import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))
from run_cases import CASES, HOOK, event_for, run_hook  # noqa: E402

CASE_LIST = json.loads(CASES.read_text("utf-8"))


@pytest.mark.parametrize("case", CASE_LIST, ids=[c["id"] for c in CASE_LIST])
def test_case(case):
    got, code, _ = run_hook(event_for(case["command"]))
    assert got == case["expect"]
    assert (code == 2) == (got == "deny")


@pytest.mark.parametrize("stdin_text", ["", "not json", "[]", json.dumps({"hook_event_name": "x"}),
                                        json.dumps({"command": ""})])
def test_malformed_input_fails_closed(stdin_text):
    got, code, _ = run_hook(stdin_text)
    assert got == "deny" and code == 2


def test_bom_in_input_is_tolerated():
    got, _, _ = run_hook("\ufeff" + event_for("ls"))
    assert got == "allow"


def test_hook_never_executes_commands():
    source = HOOK.read_text("utf-8")
    for forbidden in ("subprocess", "os.system", "os.popen", "eval(", "exec("):
        assert forbidden not in source
