# Тест-набір для hooks (вправа 17.6, ЛР11)

Набір подає JSON-події в hook через stdin і перевіряє відповідь. **Жодна команда з
`cases.json` не виконується**: це лише рядки в полі `command`. Запуск з кореня репозиторію:

    python tools/hooks_testkit/run_cases.py          # таблиця результатів
    python -m pytest tools/hooks_testkit             # те саме як тести

Додайте власні випадки в `cases.json` (поля `id`, `command`, `expect`: allow | deny | ask).
Якщо ви знайшли обхід, спершу додайте випадок (тест падає), потім виправляйте hook.
Чесно: denylist-хук не є межею безпеки, див. docstring у `.cursor/hooks/guard_shell.py`.
