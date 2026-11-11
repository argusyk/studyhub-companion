"""afterFileEdit: форматує змінений Python-файл через ruff, якщо він встановлений."""
import shutil
import subprocess
import sys
from pathlib import Path

from hook_io import read_event


def main() -> None:
    path = read_event().get("file_path", "")
    ruff = shutil.which("ruff")
    if ruff and path.endswith(".py") and Path(path).exists():
        subprocess.run([ruff, "format", path], capture_output=True, timeout=15, check=False)
    sys.exit(0)


if __name__ == "__main__":
    main()
