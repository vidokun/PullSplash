import os
import sys
from pathlib import Path


def _get_app_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent.parent


def _get_user_dir() -> Path:
    if getattr(sys, "frozen", False):
        if sys.platform == "darwin":
            return Path.home() / "Library" / "Application Support" / "PullSplash"
        elif sys.platform == "win32":
            return Path(os.getenv("APPDATA", Path.home())) / "PullSplash"
        return Path.home() / ".pullsplash"
    return Path(__file__).resolve().parent.parent


APP_DIR = _get_app_dir()
USER_DIR = _get_user_dir()
BACKEND_DIR = APP_DIR / "backend"
DOWNLOADS_DIR = Path.home() / "Downloads" / "PullSplash"
API_KEY_FILE = USER_DIR / "api_key.txt"

DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)
USER_DIR.mkdir(parents=True, exist_ok=True)

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
