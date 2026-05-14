#!/usr/bin/env python3

import argparse
import json
import os
import re
import sqlite3
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone


DB_PATH = os.path.expanduser("~/.local/share/opencode/opencode.db")

LESSON_RULES = [
    {
        "id": "verify_paths_before_editing",
        "source": "tool_error",
        "pattern": re.compile(r"File not found|ENOENT", re.IGNORECASE),
        "title": "Verify paths before editing",
        "guardrail": "Before any read or edit, verify the exact path exists and prefer glob/search over guessing file paths.",
    },
    {
        "id": "reread_before_patching",
        "source": "tool_error",
        "pattern": re.compile(r"oldString not found", re.IGNORECASE),
        "title": "Reread the live file before patching",
        "guardrail": "Before patching, reread the current file and anchor edits on live surrounding context instead of assuming earlier text still matches.",
    },
    {
        "id": "avoid_noop_edits",
        "source": "tool_error",
        "pattern": re.compile(r"oldString and newString must be different", re.IGNORECASE),
        "title": "Skip no-op edits",
        "guardrail": "Do not issue no-op edits. Compare the intended replacement first and only patch when the new content is actually different.",
    },
    {
        "id": "recover_from_tool_abort",
        "source": "tool_error",
        "pattern": re.compile(r"Tool execution aborted|aborted", re.IGNORECASE),
        "title": "Shrink the step after tool aborts",
        "guardrail": "If a tool aborts, inspect the exact failure, reduce the step size, and choose a deterministic fallback instead of retrying blindly.",
    },
    {
        "id": "respect_analysis_mode",
        "source": "user_text",
        "pattern": re.compile(r"我只是問|只是確認|幫我分析|先分析|先討論|先不要做|不要動手", re.IGNORECASE),
        "title": "Stay in analysis mode when asked",
        "guardrail": "When the user is asking for explanation, analysis, or review, stay in analysis mode and do not edit unless they explicitly ask for changes.",
    },
    {
        "id": "respect_no_change_constraints",
        "source": "user_text",
        "pattern": re.compile(r"先不要改|先不要做|不要改|不用改|不要參考", re.IGNORECASE),
        "title": "Treat no-change instructions as hard constraints",
        "guardrail": "Treat 'do not change' and 'ignore this source' instructions as hard constraints and repeat them back before acting if there is any ambiguity.",
    },
]


def connect(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def recent_sessions(conn: sqlite3.Connection, days: int, limit: int):
    cutoff = int((datetime.now(timezone.utc) - timedelta(days=days)).timestamp() * 1000)
    return conn.execute(
        """
        SELECT
          id,
          title,
          directory,
          time_updated,
          datetime(time_updated/1000, 'unixepoch', 'localtime') AS updated_at
        FROM session
        WHERE time_updated >= ?
        ORDER BY time_updated DESC
        LIMIT ?
        """,
        (cutoff, limit),
    ).fetchall()


def load_parts(conn: sqlite3.Connection, session_id: str):
    return conn.execute(
        """
        SELECT
          p.data AS part_data,
          json_extract(m.data, '$.role') AS role,
          datetime(p.time_created/1000, 'unixepoch', 'localtime') AS created_at
        FROM part p
        LEFT JOIN message m ON m.id = p.message_id
        WHERE p.session_id = ?
        ORDER BY p.time_created
        """,
        (session_id,),
    ).fetchall()


def match_rules(source: str, text: str):
    matches = []
    for rule in LESSON_RULES:
        if rule["source"] != source:
            continue
        if rule["pattern"].search(text):
            matches.append(rule)
    return matches


def should_ignore_user_text(text: str) -> bool:
    collapsed = " ".join(text.split())
    ignored_patterns = [
        r"^▣ DCP",
        r"tokens removed",
        r"^lucas@.*%",
        r"^https?://",
    ]
    return any(re.search(pattern, collapsed, re.IGNORECASE) for pattern in ignored_patterns)


def trim(text: str, length: int = 180) -> str:
    collapsed = " ".join(text.split())
    if len(collapsed) <= length:
        return collapsed
    return collapsed[: length - 3] + "..."


def analyze_session(conn: sqlite3.Connection, session_row: sqlite3.Row):
    result = {
        "id": session_row["id"],
        "title": session_row["title"] or "",
        "directory": session_row["directory"] or "",
        "updated_at": session_row["updated_at"],
        "tool_errors": 0,
        "user_corrections": 0,
        "score": 0,
        "examples": [],
        "rule_hits": defaultdict(list),
    }

    for row in load_parts(conn, session_row["id"]):
        try:
            payload = json.loads(row["part_data"])
        except json.JSONDecodeError:
            continue

        part_type = payload.get("type")
        role = row["role"] or ""

        if part_type == "tool":
            status = ((payload.get("state") or {}).get("status")) or ""
            if status != "error":
                continue
            error_text = ((payload.get("state") or {}).get("error")) or ""
            if not error_text:
                continue

            result["tool_errors"] += 1
            result["score"] += 2
            snippet = trim(error_text)
            result["examples"].append(f"tool error: {snippet}")
            for rule in match_rules("tool_error", error_text):
                result["rule_hits"][rule["id"]].append(
                    {
                        "session_id": result["id"],
                        "title": result["title"],
                        "snippet": snippet,
                    }
                )

        if part_type == "text" and role == "user":
            text = payload.get("text") or ""
            if not text:
                continue
            if should_ignore_user_text(text):
                continue
            matched = match_rules("user_text", text)
            if not matched:
                continue

            result["user_corrections"] += 1
            result["score"] += 3
            snippet = trim(text)
            result["examples"].append(f"user correction: {snippet}")
            for rule in matched:
                result["rule_hits"][rule["id"]].append(
                    {
                        "session_id": result["id"],
                        "title": result["title"],
                        "snippet": snippet,
                    }
                )

    return result


def collect_analysis(conn: sqlite3.Connection, days: int, limit: int):
    sessions = [analyze_session(conn, row) for row in recent_sessions(conn, days, limit)]
    sessions = [session for session in sessions if session["score"] > 0]
    sessions.sort(key=lambda item: (item["score"], item["tool_errors"], item["user_corrections"], item["updated_at"]), reverse=True)

    rule_summary = {}
    for rule in LESSON_RULES:
        examples = []
        seen = set()
        for session in sessions:
            for example in session["rule_hits"].get(rule["id"], []):
                key = (example["session_id"], example["snippet"])
                if key in seen:
                    continue
                seen.add(key)
                examples.append(example)
        if examples:
            rule_summary[rule["id"]] = {"rule": rule, "examples": examples}

    return sessions, rule_summary


def render_sessions(sessions, max_examples: int):
    lines = []
    for session in sessions:
        lines.append(
            f"{session['id']} | score={session['score']} | tool_errors={session['tool_errors']} | user_corrections={session['user_corrections']} | {session['title']}"
        )
        for example in session["examples"][:max_examples]:
            lines.append(f"  - {example}")
    return "\n".join(lines) if lines else "No high-signal failure sessions found."


def render_prompt(days: int, sessions, rule_summary, top_rules: int, max_examples: int):
    if not sessions:
        return "No stable failure patterns found in the selected window."

    ranked = sorted(
        rule_summary.values(),
        key=lambda item: len(item["examples"]),
        reverse=True,
    )[:top_rules]

    lines = []
    lines.append("# Failure-Informed Prompt Guardrails")
    lines.append("")
    lines.append(f"Window: last {days} days")
    lines.append(f"Sessions with signal: {len(sessions)}")
    lines.append("")
    lines.append("## Observed Patterns")
    lines.append("")

    guardrails = []
    for index, item in enumerate(ranked, start=1):
        rule = item["rule"]
        guardrails.append(rule["guardrail"])
        lines.append(f"{index}. {rule['title']} ({len(item['examples'])} hits)")
        for example in item["examples"][:max_examples]:
            lines.append(f"- {example['session_id']}: {example['snippet']}")
        lines.append(f"- Guardrail: {rule['guardrail']}")
        lines.append("")

    lines.append("## Reusable Prompt Block")
    lines.append("")
    lines.append("```text")
    lines.append("<failure_guardrails>")
    for guardrail in guardrails:
        lines.append(f"- {guardrail}")
    lines.append("</failure_guardrails>")
    lines.append("```")

    return "\n".join(lines)


def write_output(text: str, output_path: str | None):
    if output_path:
        with open(output_path, "w", encoding="utf-8") as handle:
            handle.write(text)
            handle.write("\n")
    else:
        print(text)


def main():
    parser = argparse.ArgumentParser(description="Mine OpenCode failure patterns into reusable prompt guardrails")
    parser.add_argument("--db", default=DB_PATH, help="Path to opencode.db")
    subparsers = parser.add_subparsers(dest="command", required=True)

    sessions_parser = subparsers.add_parser("sessions", help="List recent sessions with failure signals")
    sessions_parser.add_argument("--days", type=int, default=30)
    sessions_parser.add_argument("--limit", type=int, default=30)
    sessions_parser.add_argument("--max-examples", type=int, default=3)
    sessions_parser.add_argument("--output")

    prompt_parser = subparsers.add_parser("prompt", help="Generate reusable prompt guardrails")
    prompt_parser.add_argument("--days", type=int, default=30)
    prompt_parser.add_argument("--limit", type=int, default=40)
    prompt_parser.add_argument("--top-rules", type=int, default=5)
    prompt_parser.add_argument("--max-examples", type=int, default=3)
    prompt_parser.add_argument("--output")

    args = parser.parse_args()
    if not os.path.exists(args.db):
        print(f"Database not found: {args.db}", file=sys.stderr)
        raise SystemExit(1)

    conn = connect(args.db)
    try:
        if args.command == "sessions":
            sessions, _ = collect_analysis(conn, args.days, args.limit)
            output = render_sessions(sessions, args.max_examples)
            write_output(output, args.output)
        elif args.command == "prompt":
            sessions, rule_summary = collect_analysis(conn, args.days, args.limit)
            output = render_prompt(args.days, sessions, rule_summary, args.top_rules, args.max_examples)
            write_output(output, args.output)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
