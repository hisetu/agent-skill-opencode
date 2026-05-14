# SQLite Query Recipes for OpenCode Session Forensics

## Open the database

```bash
sqlite3 "$HOME/.local/share/opencode/opencode.db"
```

## Reusable TEMP VIEW setup

```sql
CREATE TEMP VIEW temp_repo_sessions AS
SELECT
  s.id AS session_id,
  s.title AS session_title,
  s.directory,
  datetime(s.time_created / 1000, 'unixepoch', 'localtime') AS created_at,
  datetime(s.time_updated / 1000, 'unixepoch', 'localtime') AS updated_at
FROM session s;

CREATE TEMP VIEW temp_session_parts AS
SELECT
  p.session_id,
  s.title AS session_title,
  s.directory,
  p.message_id,
  p.time_created AS part_created_ms,
  datetime(p.time_created / 1000, 'unixepoch', 'localtime') AS part_created_at,
  json_extract(p.data, '$.type') AS part_type,
  json_extract(p.data, '$.tool') AS tool,
  json_extract(p.data, '$.text') AS part_text,
  json_extract(p.data, '$.path') AS part_path,
  json_extract(p.data, '$.filePath') AS part_file_path,
  json_extract(p.data, '$.command') AS part_command,
  CAST(p.data AS TEXT) AS raw_part_json
FROM part p
JOIN session s ON s.id = p.session_id;
```

## Find recent sessions for one repo

```sql
SELECT session_id, session_title, created_at, updated_at
FROM temp_repo_sessions
WHERE directory LIKE '%/PRO-SPACE-BACKEND%'
ORDER BY updated_at DESC
LIMIT 50;
```

## Find sessions by keyword

```sql
SELECT DISTINCT
  session_id,
  session_title,
  updated_at
FROM temp_repo_sessions
JOIN temp_session_parts USING (session_id, session_title, directory)
WHERE directory LIKE '%/PRO-SPACE-BACKEND%'
  AND (
    part_text LIKE '%CoachBodyRecordRoutes%'
    OR part_path LIKE '%CoachBodyRecordRoutes.kt%'
    OR part_file_path LIKE '%CoachBodyRecordRoutes.kt%'
    OR raw_part_json LIKE '%CoachBodyRecordRoutes%'
  )
ORDER BY updated_at DESC;
```

## Find sessions by multiple clues

```sql
SELECT DISTINCT
  session_id,
  session_title,
  updated_at
FROM temp_repo_sessions
JOIN temp_session_parts USING (session_id, session_title, directory)
WHERE directory LIKE '%/PRO-SPACE-BACKEND%'
  AND (
    part_text LIKE '%CoachBodyRecordRoutes%'
    OR part_path LIKE '%CoachBodyRecordRoutes.kt%'
    OR part_file_path LIKE '%CoachBodyRecordRoutes.kt%'
    OR part_text LIKE '%body-records/download%'
    OR part_command LIKE '%body-records/download%'
    OR part_text LIKE '%GetCoachBodyRecordPhotoDownloadUseCase%'
    OR part_text LIKE '%BatchDownloadCoachBodyRecordPhotosUseCase%'
    OR raw_part_json LIKE '%CoachBodyRecordRoutes%'
    OR raw_part_json LIKE '%body-records/download%'
    OR raw_part_json LIKE '%GetCoachBodyRecordPhotoDownloadUseCase%'
    OR raw_part_json LIKE '%BatchDownloadCoachBodyRecordPhotosUseCase%'
  )
ORDER BY updated_at DESC;
```

## Inspect the evidence for one session

```sql
SELECT
  part_created_at,
  part_created_ms,
  part_type,
  tool,
  substr(COALESCE(part_text, raw_part_json), 1, 500) AS snippet
FROM temp_session_parts
WHERE session_id = 'ses_xxx'
  AND (
    part_text LIKE '%CoachBodyRecordRoutes%'
    OR part_path LIKE '%CoachBodyRecordRoutes.kt%'
    OR part_file_path LIKE '%CoachBodyRecordRoutes.kt%'
    OR part_text LIKE '%body-records/download%'
    OR part_command LIKE '%body-records/download%'
    OR raw_part_json LIKE '%CoachBodyRecordRoutes%'
    OR raw_part_json LIKE '%body-records/download%'
  )
ORDER BY part_created_ms, message_id;
```

## Show full timeline for one session

```sql
SELECT
  part_created_at,
  part_created_ms,
  part_type,
  tool,
  substr(COALESCE(part_text, raw_part_json), 1, 300) AS snippet
FROM temp_session_parts
WHERE session_id = 'ses_xxx'
ORDER BY part_created_ms, message_id;
```

## Materialize temporary cache for repeated searches

```sql
CREATE TEMP TABLE temp_session_parts_cache AS
SELECT
  p.session_id,
  s.title AS session_title,
  s.directory,
  p.message_id,
  p.time_created AS part_created_ms,
  datetime(p.time_created / 1000, 'unixepoch', 'localtime') AS part_created_at,
  json_extract(p.data, '$.type') AS part_type,
  json_extract(p.data, '$.tool') AS tool,
  json_extract(p.data, '$.text') AS part_text,
  json_extract(p.data, '$.path') AS part_path,
  json_extract(p.data, '$.filePath') AS part_file_path,
  json_extract(p.data, '$.command') AS part_command,
  CAST(p.data AS TEXT) AS raw_part_json
FROM part p
JOIN session s ON s.id = p.session_id;

CREATE INDEX temp.idx_parts_session ON temp_session_parts_cache(session_id);
CREATE INDEX temp.idx_parts_directory ON temp_session_parts_cache(directory);
CREATE INDEX temp.idx_parts_type ON temp_session_parts_cache(part_type);
```

## Use the cached table

```sql
SELECT DISTINCT
  session_id,
  session_title
FROM temp_session_parts_cache
WHERE directory LIKE '%/PRO-SPACE-BACKEND%'
  AND (
    part_text LIKE '%git stash%'
    OR part_command LIKE '%git stash%'
    OR raw_part_json LIKE '%git stash%'
  )
ORDER BY session_id;
```

## Heuristic reminder

- `TEMP VIEW` improves authoring speed
- `TEMP TABLE` helps repeated filtering and temp indexing
- `%keyword%` scans are still expensive
- search `raw_part_json` when `$.text` misses evidence
- keep raw millisecond timestamps for accurate timeline ordering
- use repo + date + title narrowing before broad text search
