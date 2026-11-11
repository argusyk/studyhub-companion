"""beforeShellExecution: охоронець shell-команд.

Читає JSON зі stdin (поле `command`), відповідає JSON у stdout (`permission`) і кодом 2 при
забороні. Залежить лише від hook_io.py поруч (інших модулів немає). Команди НІКОЛИ не виконує.

Політика: рекурсивне видалення дозволене лише для явного списку каталогів-кешів усередині
проєкту (SAFE_DIRS). Усе, що схоже на рекурсивне видалення, але не відповідає списку, блокується.

Чесне обмеження: denylist не є межею безпеки. Агент може записати команду у файл і
запустити його, обфускувати рядок тощо. Цей хук ловить типові помилки (історія з 300 ГБ),
а від свідомого обходу захищають пісочниця ОС і контейнер (розд. 17).
"""
import re
from pathlib import Path

from hook_io import allow, ask, deny, read_event, workspace_root

SAFE_DIRS = {".next", "node_modules", ".pytest_cache", "__pycache__", "build", "dist",
             ".turbo", ".mypy_cache", ".ruff_cache"}
DELETE_CMDS = {"rm", "rmdir", "rd", "del", "erase", "remove-item", "ri"}
INTERPRETERS = {"bash", "sh", "zsh", "dash", "pwsh", "powershell", "cmd", "python", "python3",
                "py", "node", "eval", "xargs", "sudo", "env", "time", "nohup", "exec", "start"}
SEGMENT_SPLIT = re.compile(r"&&|\|\||[;|\n&]")
TOKEN = re.compile(r"\"[^\"]*\"?|'[^']*'?|\S+")
PS_RECURSE = re.compile(r"^-r(e(c(u(r(s(e)?)?)?)?)?)?(:.*)?$", re.IGNORECASE)
WIN_FLAGS = re.compile(r"^(/[a-zA-Z])+$")
BAD_PATH_CHARS = set("$`~%*?{}()<>|")

DENY_PATTERNS = [
    (r"\bfind\b[^|;&\n]*\s-delete\b", "find -delete заборонено"),
    (r"\b(shutil\.)?rmtree\b|\bos\.removedirs\b", "програмне рекурсивне видалення (rmtree) заборонено"),
    (r"\bgit\s+push\b[^|;&\n]*(--force\b|--force-with-lease|\s-f\b|\s\+\S)", "force-push заборонено"),
    (r"\bgit\s+clean\b[^|;&\n]*\s-[a-zA-Z]*f", "git clean -f видаляє файли без відновлення"),
    (r"\bchmod\b[^|;&\n]*(-R|--recursive)[^|;&\n]*\b777\b", "chmod -R 777 заборонено"),
    (r"\bmkfs(\.\w+)?\b|\bdd\b[^|;&\n]*\bof=/dev/|:\(\)\s*\{|\bformat\s+[a-z]:", "форматування диска заборонено"),
    (r"\b(curl|wget|iwr|invoke-webrequest)\b[^\n]*\|\s*(sudo\s+)?(ba|z|da)?sh\b", "виконання завантаженого скрипта (curl | sh) заборонено"),
    (r"\b(curl|wget|iwr|invoke-webrequest)\b[^\n]*\|\s*(iex|invoke-expression|pwsh|powershell)\b", "виконання завантаженого скрипта заборонено"),
    (r"\b(cat|type|get-content|gc|less|more|head|tail|bat)\b[^|;&\n]*\.env(?!\.example)\b", "читання .env (секрети) заборонено"),
]
ASK_PATTERNS = [
    (r"\bgit\s+reset\s+[^|;&\n]*--hard\b", "git reset --hard знищує незакомічені зміни"),
    (r"\b(drop\s+(table|database|schema)|truncate\s+table)\b", "SQL, що знищує дані"),
]


def cmd_name(token: str) -> str:
    base = token.replace("\\", "/").rsplit("/", 1)[-1].lower()
    for ext in (".exe", ".cmd", ".bat", ".ps1"):
        if base.endswith(ext):
            base = base[: -len(ext)]
    return base


def unquote(token: str) -> str:
    if token[:1] in "\"'":
        token = token[1:]
        if token[-1:] in "\"'":
            token = token[:-1]
    return token


def is_recursive(name: str, args: list[str]) -> bool:
    for a in args:
        if name == "rm":
            if a.startswith("--") and len(a) > 2 and "recursive".startswith(a[2:].split("=")[0]):
                return True
            if re.fullmatch(r"-[A-Za-z]*[rR][A-Za-z]*", a):
                return True
        elif name in {"remove-item", "ri"}:
            if PS_RECURSE.match(a):
                return True
        else:  # rmdir, rd, del, erase (cmd.exe): /s
            if re.search(r"(?i)(^|/)s(?![a-z])", a) and a.startswith("/"):
                return True
    return False


def target_args(name: str, args: list[str]) -> list[str]:
    out, seen_dd = [], False
    for a in args:
        if a == "--" and not seen_dd:
            seen_dd = True
        elif not seen_dd and a.startswith("-") and a != "-":
            continue
        elif name in {"rmdir", "rd", "del", "erase"} and WIN_FLAGS.match(a):
            continue
        else:
            out.append(a)
    return out


def targets_are_safe(targets: list[str], root: Path, cwd: Path) -> bool:
    if not targets:
        return False
    for raw in targets:
        t = unquote(raw).replace("\\", "/")
        if not t or any(c in BAD_PATH_CHARS for c in t):
            return False
        p = Path(t)
        resolved = (p if p.is_absolute() else cwd / p).resolve()
        if resolved == root or root not in resolved.parents or resolved.name not in SAFE_DIRS:
            return False
    return True


def analyze(command: str, root: Path, cwd: Path, depth: int = 0) -> list[tuple[str, str]]:
    findings: list[tuple[str, str]] = []
    if depth > 3:
        return [("deny", "надто глибоке вкладення команд")]
    for segment in SEGMENT_SPLIT.split(command):
        tokens = [unquote(t) for t in TOKEN.findall(segment)]
        seen_interpreter = False
        for i, tok in enumerate(tokens):
            name = cmd_name(tok)
            if name in INTERPRETERS:
                seen_interpreter = True
            elif seen_interpreter and re.search(r"\s", tok):
                findings += analyze(tok, root, cwd, depth + 1)
            if name in DELETE_CMDS:
                args = tokens[i + 1:]
                if is_recursive(name, args) and not targets_are_safe(target_args(name, args), root, cwd):
                    findings.append(("deny", "Рекурсивне видалення дозволене лише для: "
                                     + ", ".join(sorted(SAFE_DIRS)) + " усередині проєкту."))
    return findings


def evaluate(command: str, root: Path, cwd: Path) -> tuple[str, str]:
    findings = analyze(command, root, cwd)
    for pattern, message in DENY_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            findings.append(("deny", message))
    for pattern, message in ASK_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            findings.append(("ask", message))
    for level in ("deny", "ask"):
        for lvl, msg in findings:
            if lvl == level:
                return level, msg
    return "allow", ""


def main() -> None:
    event = read_event()
    command = event.get("command")
    if not isinstance(command, str) or not command.strip():
        deny("Хук не зміг прочитати command (fail closed).")
    root = workspace_root(event).resolve()
    cwd = Path(event.get("cwd") or root)
    level, message = evaluate(command, root, cwd.resolve() if cwd.exists() else root)
    if level == "deny":
        deny(message)
    elif level == "ask":
        ask(message)
    else:
        allow()


if __name__ == "__main__":
    main()
