#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "demo_tasks.json"


def run(argv: list[str]) -> int:
    import subprocess

    def cli(*args: str) -> int:
        cmd = [sys.executable, str(ROOT / "main.py"), "--storage", "json", "--json-path", str(JSON_PATH), *args]
        return subprocess.call(cmd)

    HELP = (
        "Commands:\n"
        "  1) add <title> [--priority low|normal|high|urgent] [--due YYYY-MM-DD] [--tag TAG ...] [--note NOTE]\n"
        "  2) list [--all]\n"
        "  3) done <id>\n"
        "  4) delete <id>\n"
        "  5) search <keyword>\n"
        "  6) prioritize\n"
        "  7) suggest\n"
        "  8) weekly-summary\n"
        "  ?) help\n"
        "  q) quit\n"
    )

    print("PKMS interactive menu (json store)")
    print(f"Data file: {JSON_PATH}")
    print(HELP)
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if not raw:
            continue
        if raw in {"q", "quit", "exit"}:
            return 0
        if raw in {"?", "help", "h"}:
            print(HELP)
            continue

        parts = raw.split()
        cmd, rest = parts[0], parts[1:]
        if cmd == "add":
            if not rest:
                print("usage: add <title> [--priority ...] [--due ...] [--tag ...] [--note ...]")
                continue
            cli("add", *rest)
        elif cmd == "list":
            cli("list", *rest)
        elif cmd == "done":
            cli("done", *rest)
        elif cmd == "delete":
            cli("delete", *rest)
        elif cmd == "search":
            cli("search", *rest)
        elif cmd == "prioritize":
            cli("prioritize")
        elif cmd == "suggest":
            cli("suggest")
        elif cmd == "weekly-summary":
            cli("weekly-summary")
        else:
            print("Unknown command. Type ? for help.")

    return 0


if __name__ == "__main__":
    raise SystemExit(run(sys.argv[1:]))
