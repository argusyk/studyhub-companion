"""Генерує data/schedule.json (вигадані дані): python tools/schedule_mcp/make_schedule.py"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[2] / "data" / "schedule.json"
GROUPS = ["ПІ-22а", "ПІ-22б", "КІ-21"]
TEACHERS = ["Коваленко О. М.", "Петренко І. В.", "Мельничук С. А."]
SUBJECTS = ["Бази даних", "Програмування", "Тестування ПЗ", "Комп'ютерні мережі"]
ROOMS = ["3.214", "3.216", "2.101", "4.005"]


def build() -> dict:
    slots = []
    for week in range(1, 19):
        for day in range(1, 6):
            for pair in range(1, 5):
                gi = (week + day + pair) % len(GROUPS)
                ti = (day + pair) % len(TEACHERS)
                # деякі пари вільні: викладач не зайнятий
                if (week * 7 + day * 3 + pair) % 4 == 0:
                    continue
                slots.append({"week": week, "day": day, "pair": pair, "group": GROUPS[gi],
                              "teacher": TEACHERS[ti], "subject": SUBJECTS[(gi + ti) % len(SUBJECTS)],
                              "room": ROOMS[(gi + pair) % len(ROOMS)]})
    # приклад із розд. 12: четвер, пари 2-3 на 7 тижні в Коваленко О. М.
    slots = [s for s in slots if not (s["week"] == 7 and s["day"] == 4 and s["pair"] in (2, 3))]
    slots += [
        {"week": 7, "day": 4, "pair": 2, "group": "ПІ-22а", "teacher": "Коваленко О. М.",
         "subject": "Бази даних", "room": "3.214"},
        {"week": 7, "day": 4, "pair": 3, "group": "ПІ-22б", "teacher": "Коваленко О. М.",
         "subject": "Бази даних", "room": "3.214"},
    ]
    slots.sort(key=lambda s: (s["week"], s["day"], s["pair"], s["group"]))
    return {"pairs_per_day": 6, "slots": slots}


if __name__ == "__main__":
    data = build()
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(data, ensure_ascii=False, indent=0) + "\n")
    print("schedule: slots =", len(data["slots"]))
