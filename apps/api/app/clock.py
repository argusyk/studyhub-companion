"""Годинник сервера. УВАГА: навчальний код з навмисним дефектом для ЛР9.

`server_now_naive` імітує `datetime.now()` на сервері, де задано змінну оточення TZ:
повертає «наївний» (без tzinfo) місцевий час. На CI SERVER_TZ не задано – це UTC.
(На Windows `time.tzset` немає, тому TZ сервера імітується змінною SERVER_TZ.)
"""
import os
from datetime import datetime, timezone
from zoneinfo import ZoneInfo


def server_now_naive(at_utc: datetime | None = None) -> datetime:
    moment = at_utc or datetime.now(timezone.utc)
    tz_name = os.environ.get("SERVER_TZ")
    local = moment.astimezone(ZoneInfo(tz_name)) if tz_name else moment.astimezone(timezone.utc)
    return local.replace(tzinfo=None)
