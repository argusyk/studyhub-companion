"""tools/schedule_mcp/server.py – MCP-сервер «розклад кафедри» для StudyHub (лише читання).

Запуск (stdio): `python tools/schedule_mcp/server.py` з venv, де встановлено `mcp[cli]`.
Дані: data/schedule.json (генерується tools/schedule_mcp/make_schedule.py, вигадані).
"""
import json
from pathlib import Path

try:  # mcp 1.x
    from mcp.server.fastmcp import FastMCP
except ImportError:  # mcp >= 2: FastMCP перейменовано на MCPServer
    from mcp.server.mcpserver import MCPServer as FastMCP

DATA = Path(__file__).resolve().parents[2] / "data" / "schedule.json"
DAYS = {1: "понеділок", 2: "вівторок", 3: "середа", 4: "четвер", 5: "п'ятниця"}

mcp = FastMCP("studyhub-schedule")


def load() -> dict:
    with DATA.open(encoding="utf-8") as fh:
        return json.load(fh)


def check_week(week: int) -> None:
    if not 1 <= week <= 18:
        raise ValueError(f"Тиждень {week} поза семестром; допустимо від 1 до 18.")


@mcp.tool()
def get_schedule(group: str, week: int) -> list[dict]:
    """Повертає заняття академічної групи на тиждень семестру. Лише читання.

    Викликай, коли треба знати, коли група має пари.
    group: шифр групи як у розкладі кафедри, напр. "ПІ-22а".
    week: номер тижня семестру від 1 до 18.
    Результат: список занять з днем, номером пари, дисципліною, викладачем і аудиторією.
    """
    check_week(week)
    rows = [s for s in load()["slots"] if s["group"] == group and s["week"] == week]
    if not rows:
        raise ValueError(f'Для групи "{group}" на тиждень {week} занять не знайдено. '
                         'Перевірте шифр: він має вигляд "ПІ-22а".')
    return sorted(rows, key=lambda s: (s["day"], s["pair"]))


@mcp.tool()
def find_free_slot(teacher: str, duration: int = 1, week: int = 1) -> list[dict]:
    """Шукає вільні пари викладача на тиждень семестру. Лише читання.

    Викликай для планування консультацій чи перездач.
    teacher: прізвище та ініціали як у розкладі, напр. "Коваленко О. М.".
    duration: скільки пар поспіль потрібно, від 1 до 3.
    week: номер тижня семестру від 1 до 18.
    Результат: до 10 варіантів з днем і номером першої пари.
    """
    check_week(week)
    if not 1 <= duration <= 3:
        raise ValueError("duration має бути від 1 до 3 пар поспіль.")
    data = load()
    known = {s["teacher"] for s in data["slots"]}
    if teacher not in known:
        raise ValueError(f'Викладача "{teacher}" немає в розкладі. '
                         'Формат імені: "Прізвище І. Б.".')
    busy = {(s["day"], s["pair"]) for s in data["slots"]
            if s["teacher"] == teacher and s["week"] == week}
    last = data["pairs_per_day"] - duration + 1
    free = [{"day": DAYS[d], "start_pair": p, "pairs": duration}
            for d in DAYS for p in range(1, last + 1)
            if all((d, p + k) not in busy for k in range(duration))]
    return free[:10]


if __name__ == "__main__":
    mcp.run()  # транспорт stdio
