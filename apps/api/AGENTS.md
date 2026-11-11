# apps/api

- Новий ендпоінт додається разом зі схемою, сервісом і тестом.
- Помилки віддаються як HTTPException із зрозумілим повідомленням українською.
- Часові пояси: усе в БД у UTC (UtcDateTime), див. docs/business-rules.md, розділ «Дедлайни».
- Тести: `python -m pytest` (SQLite in-memory, без PostgreSQL).
- Файли міграцій: короткі імена `000N_xxx.py` (обмеження довжини шляху в Windows).
