#!/usr/bin/env python3
"""
OpenCode Session Compaction Cleaner

Remove compaction messages from an OpenCode session to restore full conversation history.
Compaction causes AI agents to "forget" earlier context by replacing it with summaries.

Usage:
  python3 clean_compaction.py <session_id> [--dry-run] [--backup]

Examples:
  # Preview what would be deleted (safe)
  python3 clean_compaction.py ses_abc123 --dry-run

  # Backup DB then clean
  python3 clean_compaction.py ses_abc123 --backup

  # Clean directly (DB backup recommended)
  python3 clean_compaction.py ses_abc123
"""

import argparse
import json
import os
import shutil
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

DB_PATH = Path.home() / ".local" / "share" / "opencode" / "opencode.db"


def get_db_path():
    if not DB_PATH.exists():
        print(f"Error: OpenCode database not found at {DB_PATH}")
        sys.exit(1)
    return str(DB_PATH)


def backup_db():
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = f"{DB_PATH}.bak-{timestamp}"
    shutil.copy2(str(DB_PATH), backup_path)
    size_mb = os.path.getsize(backup_path) / (1024 * 1024)
    print(f"Backup created: {backup_path} ({size_mb:.1f} MB)")
    return backup_path


def find_session(conn, session_id):
    """Find session by ID (exact or partial match)."""
    cur = conn.execute(
        "SELECT id, title, slug FROM session WHERE id = ?", (session_id,)
    )
    row = cur.fetchone()
    if row:
        return row

    # Try partial match
    cur = conn.execute(
        "SELECT id, title, slug FROM session WHERE id LIKE ?",
        (f"%{session_id}%",),
    )
    rows = cur.fetchall()
    if len(rows) == 1:
        return rows[0]
    elif len(rows) > 1:
        print(f"Error: Multiple sessions match '{session_id}':")
        for r in rows:
            print(f"  - {r[0]}: {r[1]} ({r[2]})")
        sys.exit(1)
    else:
        print(f"Error: No session found matching '{session_id}'")
        sys.exit(1)


def find_compaction_messages(conn, session_id):
    """Find all compaction-related messages in a session."""
    # 1. Messages with mode = 'compaction'
    cur = conn.execute(
        """
        SELECT m.id, m.time_created,
               json_extract(m.data, '$.role') as role,
               json_extract(m.data, '$.mode') as mode
        FROM message m
        WHERE m.session_id = ?
          AND json_extract(m.data, '$.mode') = 'compaction'
        ORDER BY m.time_created
        """,
        (session_id,),
    )
    compaction_msgs = cur.fetchall()

    # 2. Messages with parts of type 'compaction'
    cur = conn.execute(
        """
        SELECT DISTINCT m.id, m.time_created,
               json_extract(m.data, '$.role') as role,
               json_extract(m.data, '$.mode') as mode
        FROM message m
        JOIN part p ON p.message_id = m.id
        WHERE m.session_id = ?
          AND json_extract(p.data, '$.type') = 'compaction'
        ORDER BY m.time_created
        """,
        (session_id,),
    )
    compaction_part_msgs = cur.fetchall()

    # Merge and deduplicate
    seen = set()
    result = []
    for msg in compaction_msgs + compaction_part_msgs:
        if msg[0] not in seen:
            seen.add(msg[0])
            result.append(msg)

    result.sort(key=lambda x: x[1])
    return result


def find_messages_after_compaction(conn, session_id, first_compaction_time):
    """Find all messages from the first compaction onwards."""
    cur = conn.execute(
        """
        SELECT m.id, m.time_created,
               json_extract(m.data, '$.role') as role,
               json_extract(m.data, '$.mode') as mode,
               substr(json_extract(m.data, '$.text'), 1, 80) as text_preview
        FROM message m
        WHERE m.session_id = ?
          AND m.time_created >= ?
        ORDER BY m.time_created
        """,
        (session_id, first_compaction_time),
    )
    return cur.fetchall()


def count_parts(conn, message_ids):
    """Count parts belonging to given messages."""
    if not message_ids:
        return 0
    placeholders = ",".join("?" * len(message_ids))
    cur = conn.execute(
        f"SELECT COUNT(*) FROM part WHERE message_id IN ({placeholders})",
        message_ids,
    )
    return cur.fetchone()[0]


def get_session_stats(conn, session_id):
    """Get total message and part counts for a session."""
    cur = conn.execute(
        "SELECT COUNT(*) FROM message WHERE session_id = ?", (session_id,)
    )
    msg_count = cur.fetchone()[0]
    cur = conn.execute(
        "SELECT COUNT(*) FROM part WHERE session_id = ?", (session_id,)
    )
    part_count = cur.fetchone()[0]
    return msg_count, part_count


def delete_messages_and_parts(conn, session_id, message_ids):
    """Delete parts first (FK), then messages."""
    if not message_ids:
        return 0, 0

    placeholders = ",".join("?" * len(message_ids))

    # Delete parts
    conn.execute(
        f"DELETE FROM part WHERE message_id IN ({placeholders})", message_ids
    )
    parts_deleted = conn.execute("SELECT changes()").fetchone()[0]

    # Also delete parts by session that might be orphaned
    conn.execute(
        f"""DELETE FROM part WHERE session_id = ? 
            AND message_id IN ({placeholders})""",
        [session_id] + list(message_ids),
    )

    # Delete messages
    conn.execute(
        f"DELETE FROM message WHERE id IN ({placeholders})", message_ids
    )
    msgs_deleted = conn.execute("SELECT changes()").fetchone()[0]

    return msgs_deleted, parts_deleted


def main():
    parser = argparse.ArgumentParser(
        description="Remove compaction messages from an OpenCode session"
    )
    parser.add_argument("session_id", help="Session ID (full or partial)")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what would be deleted without making changes",
    )
    parser.add_argument(
        "--backup",
        action="store_true",
        help="Create a database backup before cleaning",
    )
    parser.add_argument(
        "--mode",
        choices=["compaction-only", "compaction-and-after"],
        default="compaction-and-after",
        help="'compaction-only': delete only compaction messages. "
             "'compaction-and-after': delete compaction and all messages after first compaction (default)",
    )
    args = parser.parse_args()

    db_path = get_db_path()

    if args.backup and not args.dry_run:
        backup_db()

    conn = sqlite3.connect(db_path)

    # Find session
    session_id, title, slug = find_session(conn, args.session_id)
    print(f"\nSession: {title} ({slug})")
    print(f"ID: {session_id}")

    # Get current stats
    total_msgs, total_parts = get_session_stats(conn, session_id)
    print(f"Total: {total_msgs} messages, {total_parts} parts")

    # Find compaction messages
    compaction_msgs = find_compaction_messages(conn, session_id)

    if not compaction_msgs:
        print("\nNo compaction messages found. Session is clean!")
        conn.close()
        return

    print(f"\nFound {len(compaction_msgs)} compaction message(s):")
    for msg in compaction_msgs:
        print(f"  - {msg[0]} ({msg[2]}/{msg[3]}) at {msg[1]}")

    first_compaction_time = compaction_msgs[0][1]

    if args.mode == "compaction-and-after":
        # Find all messages from first compaction onwards
        to_delete = find_messages_after_compaction(
            conn, session_id, first_compaction_time
        )
        msg_ids = [m[0] for m in to_delete]
        parts_count = count_parts(conn, msg_ids)

        print(f"\nMessages to delete (from first compaction onwards): {len(to_delete)}")
        print(f"Parts to delete: {parts_count}")
        print(f"Will keep: {total_msgs - len(to_delete)} messages, {total_parts - parts_count} parts")
    else:
        # Only delete compaction messages themselves
        msg_ids = [m[0] for m in compaction_msgs]

        # Also find the auto-generated user messages paired with compaction
        paired_user_msgs = []
        for msg in compaction_msgs:
            if msg[2] == "assistant":  # compaction is assistant message
                cur = conn.execute(
                    """
                    SELECT id FROM message
                    WHERE session_id = ?
                      AND json_extract(data, '$.role') = 'user'
                      AND time_created < ?
                      AND time_created > ? - 100
                    ORDER BY time_created DESC LIMIT 1
                    """,
                    (session_id, msg[1], msg[1]),
                )
                row = cur.fetchone()
                if row:
                    # Check if this user message has no text (auto-generated)
                    cur2 = conn.execute(
                        "SELECT json_extract(data, '$.text') FROM message WHERE id = ?",
                        (row[0],),
                    )
                    text = cur2.fetchone()[0]
                    if not text:
                        paired_user_msgs.append(row[0])

        msg_ids = list(set(msg_ids + paired_user_msgs))
        parts_count = count_parts(conn, msg_ids)

        print(f"\nMessages to delete (compaction only + paired empty user msgs): {len(msg_ids)}")
        print(f"Parts to delete: {parts_count}")

    if args.dry_run:
        print("\n[DRY RUN] No changes made.")
        if args.mode == "compaction-and-after":
            print("\nMessages that would be deleted:")
            for m in to_delete:
                preview = m[4][:60] + "..." if m[4] and len(m[4]) > 60 else (m[4] or "(empty)")
                print(f"  {m[0]} [{m[2]}/{m[3]}] {preview}")
        conn.close()
        return

    # Execute deletion
    msgs_deleted, parts_deleted = delete_messages_and_parts(conn, session_id, msg_ids)
    conn.commit()

    # Verify
    final_msgs, final_parts = get_session_stats(conn, session_id)
    remaining_compactions = len(find_compaction_messages(conn, session_id))

    print(f"\nDone!")
    print(f"  Messages: {total_msgs} -> {final_msgs} (deleted {total_msgs - final_msgs})")
    print(f"  Parts: {total_parts} -> {final_parts} (deleted {total_parts - final_parts})")
    print(f"  Remaining compactions: {remaining_compactions}")

    conn.close()


if __name__ == "__main__":
    main()
