# Таксономія StudyHub (еталон ЛР4)

## Глосарій компонентів
| Термін | Де в коді | Значення |
|---|---|---|
| Student | `apps/api/app/models/student.py` | студент; `group_code` – slug групи (`ki-21`) |
| Lab | `apps/api/app/models/lab.py` | лабораторна з дедлайном (UTC) і максимальним балом |
| Submission | `apps/api/app/models/submission.py` | здача: файл, час, статус, підсумковий `score` |
| Grade | `apps/api/app/models/grade.py` (розд. 8) | розрахунок: `raw_score`, `penalty`, `final_score` |
| Router | `apps/api/app/routers/` | HTTP-шар, префікс `/api/v1` задає `main.py` |
| Service | `apps/api/app/services/` | бізнес-логіка (оцінювання, дедлайни, здачі) |
| UtcDateTime | `apps/api/app/db/types.py` | тип колонки «лише aware UTC» |

## Карта потоку «здати лабораторну»
Форма (`apps/web`) -> `lib/api.ts` -> `POST /api/v1/labs/{id}/submissions` ->
`routers/submissions.py` -> `services/submissions.py` -> таблиця `submissions`.

## Правила для агента
- Не вигадувати нові шари (немає `repositories`).
- Час – лише aware UTC; перетворення в пояс кафедри – на межі API.
- Штраф за запізнення – правило R-07 (`docs/business-rules.md`).
