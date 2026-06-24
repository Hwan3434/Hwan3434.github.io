#!/usr/bin/env python3
import datetime as dt
import fcntl
import os
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path("/Users/jeonghwan/develop/Hwan3434.github.io")
CODEX_BIN = Path("/opt/homebrew/bin/codex")
PROMPT_FILE = REPO_ROOT / "tools" / "codex_news_digest_prompt.md"
LOG_DIR = REPO_ROOT / ".codex-news-logs"
LOCK_FILE = LOG_DIR / "daily-news.lock"


def main() -> int:
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    if not CODEX_BIN.exists():
        print(f"codex not found: {CODEX_BIN}", file=sys.stderr)
        return 1
    if not PROMPT_FILE.exists():
        print(f"prompt file not found: {PROMPT_FILE}", file=sys.stderr)
        return 1

    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    log_file = LOG_DIR / f"news-{stamp}.log"

    with LOCK_FILE.open("w") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            print("daily news Codex job is already running")
            return 0

        prompt = PROMPT_FILE.read_text(encoding="utf-8")
        cmd = [
            str(CODEX_BIN),
            "exec",
            "--cd",
            str(REPO_ROOT),
            "--sandbox",
            "danger-full-access",
            "-c",
            'approval_policy="never"',
            "-",
        ]

        if os.environ.get("DRY_RUN") == "1":
            print(" ".join(cmd))
            print(f"log: {log_file}")
            return 0

        with log_file.open("w", encoding="utf-8") as log:
            log.write(f"started: {dt.datetime.now().isoformat()}\n")
            log.write(f"command: {' '.join(cmd)}\n\n")
            log.flush()

            result = subprocess.run(
                cmd,
                cwd=REPO_ROOT,
                input=prompt,
                text=True,
                stdout=log,
                stderr=subprocess.STDOUT,
                check=False,
            )

            log.write(f"\nfinished: {dt.datetime.now().isoformat()}\n")
            log.write(f"exit_code: {result.returncode}\n")

        print(f"log: {log_file}")
        return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
