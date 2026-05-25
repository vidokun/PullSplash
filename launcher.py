import os
import socket
import subprocess
import sys
import tempfile
import threading
import time
import traceback

import requests
import uvicorn
import webview


HOST = "127.0.0.1"
PORT_CANDIDATES = [18432, 19283, 20145, 21789, 22345, 25321, 8000]

# mutable container so the server thread can report its exception
_server_error = [None]


def _run_server(host, port):
    try:
        uvicorn.run("backend.main:app", host=host, port=port, log_level="warning")
    except Exception:
        _server_error[0] = traceback.format_exc()


def show_error(msg: str) -> None:
    sys.stderr.write(f"[ERROR] {msg}\n")
    if sys.platform == "darwin":
        short = msg.split("\n")[0]
        safe = short.replace('"', "'").replace("\\", "/")
        try:
            subprocess.run(
                ["osascript", "-e",
                 f'display dialog "{safe}" with title "PullSplash Error"'
                 f' buttons {{"OK"}} default button "OK" with icon stop'],
                timeout=5,
            )
        except Exception:
            pass
    elif sys.platform == "win32":
        try:
            import ctypes
            ctypes.windll.user32.MessageBoxW(0, msg, "PullSplash Error", 0x10)
        except Exception:
            pass


def find_free_port(candidates=None, fallback=True):
    if candidates:
        for port in candidates:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                if s.connect_ex((HOST, port)) != 0:
                    return port
    if fallback:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, 0))
            return s.getsockname()[1]
    return None


def wait_for_server(url, timeout=10):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            resp = requests.get(url, timeout=1)
            if resp.status_code == 200:
                return True
        except Exception:
            pass
        time.sleep(0.3)
    return False


def preflight_check():
    tests = [
        ("webview", lambda: webview.create_window),
        ("PIL", lambda: __import__("PIL.Image")),
        ("uvicorn", lambda: uvicorn),
        ("backend.main", lambda: __import__("backend.main")),
    ]
    for name, fn in tests:
        try:
            fn()
        except Exception as e:
            show_error(f"Missing dependency: {name}\n{str(e)[:200]}")
            return False
    return True


def main():
    frozen = getattr(sys, "frozen", False)

    if frozen:
        log_path = os.path.join(tempfile.gettempdir(), "pullsplash.log")
        try:
            sys.stdout = open(log_path, "w", buffering=1)
            sys.stderr = sys.stdout
        except Exception:
            pass

    try:
        port = find_free_port(PORT_CANDIDATES)
        if port is None:
            show_error("No available port found.\nPlease close other applications and try again.")
            sys.exit(1)

        url = f"http://{HOST}:{port}"

        if not preflight_check():
            sys.exit(1)

        server_thread = threading.Thread(
            target=_run_server,
            args=(HOST, port),
            daemon=True,
        )
        server_thread.start()

        print(f"Starting PullSplash server at {url} ...")
        if not wait_for_server(f"{url}/api/health"):
            if not server_thread.is_alive():
                detail = _server_error[0] or "Unknown error (no traceback captured)"
                show_error(
                    f"Server crashed during startup.\n\n"
                    f"{detail[-500:]}"
                )
            else:
                show_error(
                    f"Server is running but not responding on port {port}.\n\n"
                    f"A firewall may be blocking the connection."
                )
            sys.exit(1)

        print("Server ready. Opening native window...")
        webview.create_window(
            title="PullSplash",
            url=url,
            width=1200,
            height=800,
            min_size=(800, 600),
        )
        webview.start()

        print("Window closed. Shutting down...")

    except Exception:
        msg = f"PullSplash encountered an error:\n\n{traceback.format_exc()[-800:]}"
        show_error(msg)
        sys.exit(1)


if __name__ == "__main__":
    main()
