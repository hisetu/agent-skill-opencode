#!/usr/bin/env python3
import argparse
import json
import os
import sqlite3
import sys


DB_PATH = os.path.expanduser("~/.local/share/opencode/opencode.db")


def connect(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def print_rows(rows):
    for row in rows:
        print(json.dumps(dict(row), ensure_ascii=False))


def sessions_cmd(conn: sqlite3.Connection, date: str | None, limit: int, query: str | None):
    where = []
    params = []
    if date:
        where.append("(datetime(time_created/1000,'unixepoch','localtime') LIKE ? OR datetime(time_updated/1000,'unixepoch','localtime') LIKE ?)")
        params.extend([f"{date}%", f"{date}%"])
    if query:
        where.append("(id LIKE ? OR title LIKE ? OR directory LIKE ?)")
        like = f"%{query}%"
        params.extend([like, like, like])

    sql = """
    SELECT
      id,
      title,
      directory,
      datetime(time_created/1000,'unixepoch','localtime') AS created_at,
      datetime(time_updated/1000,'unixepoch','localtime') AS updated_at
    FROM session
    """
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY time_updated DESC LIMIT ?"
    params.append(limit)
    rows = conn.execute(sql, params).fetchall()
    print_rows(rows)


def session_cmd(conn: sqlite3.Connection, session_id: str):
    rows = conn.execute(
        """
        SELECT
          id,
          title,
          directory,
          version,
          datetime(time_created/1000,'unixepoch','localtime') AS created_at,
          datetime(time_updated/1000,'unixepoch','localtime') AS updated_at
        FROM session
        WHERE id = ?
        """,
        (session_id,),
    ).fetchall()
    print_rows(rows)


def messages_cmd(conn: sqlite3.Connection, session_id: str, limit: int):
    rows = conn.execute(
        """
        SELECT
          id,
          datetime(time_created/1000,'unixepoch','localtime') AS created_at,
          json_extract(data,'$.role') AS role,
          json_extract(data,'$.model') AS model,
          json_extract(data,'$.providerID') AS provider,
          substr(COALESCE(json_extract(data,'$.content'), json_extract(data,'$.summary'), ''), 1, 300) AS preview
        FROM message
        WHERE session_id = ?
        ORDER BY time_created
        LIMIT ?
        """,
        (session_id, limit),
    ).fetchall()
    print_rows(rows)


def parts_cmd(conn: sqlite3.Connection, session_id: str, limit: int, types: list[str] | None):
    sql = """
    SELECT
      message_id,
      datetime(time_created/1000,'unixepoch','localtime') AS created_at,
      json_extract(data,'$.type') AS type,
      json_extract(data,'$.tool') AS tool,
      substr(COALESCE(json_extract(data,'$.text'), json_extract(data,'$.tool'), json_extract(data,'$.state.status'), ''), 1, 500) AS preview
    FROM part
    WHERE session_id = ?
    """
    params: list[object] = [session_id]
    if types:
        sql += " AND json_extract(data,'$.type') IN ({})".format(
            ",".join("?" for _ in types)
        )
        params.extend(types)
    sql += " ORDER BY time_created LIMIT ?"
    params.append(limit)
    rows = conn.execute(sql, params).fetchall()
    print_rows(rows)


def main():
    parser = argparse.ArgumentParser(description="Inspect OpenCode sessions via SQLite")
    parser.add_argument("--db", default=DB_PATH, help="Path to opencode.db")
    sub = parser.add_subparsers(dest="command", required=True)

    p_sessions = sub.add_parser("sessions", help="List candidate sessions")
    p_sessions.add_argument("--date", help="Local date filter, e.g. 2026-03-16")
    p_sessions.add_argument("--query", help="Filter by id/title/directory substring")
    p_sessions.add_argument("--limit", type=int, default=20)

    p_session = sub.add_parser("session", help="Show one session metadata")
    p_session.add_argument("session_id")

    p_messages = sub.add_parser("messages", help="List message summaries")
    p_messages.add_argument("session_id")
    p_messages.add_argument("--limit", type=int, default=200)

    p_parts = sub.add_parser("parts", help="List transcript/tool parts")
    p_parts.add_argument("session_id")
    p_parts.add_argument("--limit", type=int, default=400)
    p_parts.add_argument("--types", nargs="*", help="Filter part types, e.g. text tool")

    args = parser.parse_args()
    if not os.path.exists(args.db):
        print(f"Database not found: {args.db}", file=sys.stderr)
        raise SystemExit(1)

    conn = connect(args.db)
    try:
        if args.command == "sessions":
            sessions_cmd(conn, args.date, args.limit, args.query)
        elif args.command == "session":
            session_cmd(conn, args.session_id)
        elif args.command == "messages":
            messages_cmd(conn, args.session_id, args.limit)
        elif args.command == "parts":
            parts_cmd(conn, args.session_id, args.limit, args.types)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
