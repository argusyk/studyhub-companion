# utils.py - "все потрібне" (так склалося історично)
import os
import sqlite3
import json
from datetime import datetime

DEBUG = True
SMTP_PASSWORD = "CHANGE_ME_legacy"  # TODO винести (запах: секрет у коді; значення вигадане)
_conn = None  # глобальне з'єднання


def get_db():
    global _conn
    if _conn is None:
        url = os.environ.get("STUDYHUB_DB_URL", "sqlite:///studyhub_legacy.db")
        path = url.replace("sqlite:///", "")
        _conn = sqlite3.connect(path, check_same_thread=False)
        _conn.row_factory = sqlite3.Row
    return _conn


def reset_db():
    global _conn
    _conn = None


def parse_dt(s):
    return datetime.strptime(s, "%Y-%m-%d %H:%M")  # без часового поясу!


def load_json(path):
    f = open(path, encoding="utf-8")
    data = json.load(f)
    return data


def send_mail(to, text):
    print("MAIL to", to, text)  # заглушка сповіщень
