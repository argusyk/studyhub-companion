"""Відтворення бага дедлайну (ЛР9): `python scripts/repro_deadline_bug.py`.

Показує, як змінюється is_late для здач о 20:00–21:30 UTC (23:00–00:30 за Києвом
у літній час) залежно від часового поясу сервера. Нічого не пише в БД.
"""
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "apps" / "api"))

from app.services.submissions import mark_submission  # noqa: E402

LAB = SimpleNamespace(deadline=datetime(2026, 4, 6, 20, 59, tzinfo=timezone.utc))  # 23:59 Київ


def run(server_tz: str | None) -> None:
    if server_tz:
        os.environ["SERVER_TZ"] = server_tz
    else:
        os.environ.pop("SERVER_TZ", None)
    print(f"\nСервер: {server_tz or 'UTC (CI)'}")
    print("здача (UTC)  здача (Київ)  is_late  очікується")
    t = datetime(2026, 4, 6, 20, 0, tzinfo=timezone.utc)
    while t <= datetime(2026, 4, 6, 21, 30, tzinfo=timezone.utc):
        sub = SimpleNamespace(is_late=None)
        mark_submission(sub, LAB, t)
        expected = t > LAB.deadline
        flag = "" if sub.is_late == expected else "  <-- ПОМИЛКА"
        kyiv = (t + timedelta(hours=3)).strftime("%H:%M")
        print(f"  {t:%H:%M}        {kyiv}        {str(sub.is_late):5}    {str(expected):5}{flag}")
        t += timedelta(minutes=30)


if __name__ == "__main__":
    run(None)
    run("Europe/Kyiv")
