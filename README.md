# Task API



A small CRUD API for managing a to-do list, built with FastAPI. Built as part of [Backend AI Engineering/https://internship.flyrank] — this is a learning project with in-memory storage only, no [...]



## How to run it



1. Clone this repo and enter the folder:

  git clone https://github.com/favour79/todo-api.git

  cd todo-api



2. Create and activate a virtual environment:

  python -m venv venv

  venv\Scripts\activate      (Windows)

  source venv/bin/activate   (Mac/Linux)



3. Install dependencies:

  pip install fastapi uvicorn



4. Run the server:

  uvicorn main:app --reload



5. Open http://localhost:8000/docs to see and test the API in Swagger UI.



## Endpoints



| Method | Path              | Description                          |

|--------|-------------------|---------------------------------------|

| GET    | /                 | API info                              |

| GET    | /health           | Health check                          |

| GET    | /tasks            | List all tasks                        |

| GET    | /tasks/{task_id}  | Get one task by id                    |

| POST   | /tasks            | Create a new task                     |

| PUT    | /tasks/{task_id}  | Update a task's title and/or done     |

| DELETE | /tasks/{task_id}  | Delete a task                         |


## Database

This project now uses SQLite instead of an in-memory list. SQLite was chosen because it needs no separate server or installation — it's a single file, which is ideal for a learning project at this stage and mirrors how many production systems start before scaling to PostgreSQL or MySQL.

The database file is created automatically the first time the app runs, at:
todo-api/tasks.db

The `tasks` table and 3 example rows are also created automatically on first run. Restarting the server no longer resets your data — this is the core change from Assignment 1.

### Example SQL query

Run directly in DB Browser for SQLite:

SELECT * FROM tasks;

Result:

| id | title                          | done |
|----|--------------------------------|------|
| 5  | Buy milk                       | 0    |
| 6  | Review loan file for Obligor A | 0    |
| 7  | Submit weekly PAR report       | 1    |

### DB Browser screenshot

![DB Browser screenshot](db-browser-screenshot.png)

Note: no extra installation is needed for the database — Python's built-in sqlite3 module handles it.

## Running with Docker Compose

The whole stack (app + Postgres) starts with one command:

docker compose up

This builds the app image, starts Postgres with a persistent volume, and runs the API on http://localhost:8000. Connection details are read from `.env` (see `.env.example` for the required variables — copy it to `.env` and fill in your own values before running).

### Architecture note

The API and routes are unchanged from Assignment 2. Only the storage layer changed: a new `repository.py` file now talks to Postgres instead of SQLite, and `main.py` calls those repository functions without knowing what database sits underneath. This is the same architecture principle proven again, one layer down.

### Persistence proof

To confirm data survives a full restart of the stack:

1. Created a task via POST /tasks
2. Confirmed it with GET /tasks
3. Stopped the entire stack (Ctrl+C on `docker compose up`, confirming both containers report "Stopped")
4. Started the stack again with `docker compose up`
5. Ran GET /tasks again — the task was still present, and Postgres logged "Database directory appears to contain a database; Skipping initialization," confirming the volume preserved the data rather than starting fresh

## Index performance: EXPLAIN ANALYZE

To explore query performance, the `tasks` table was seeded with 5,000 additional rows and a new `assigned_to` column, then queried by that column before and after adding an index.

### Before index (sequential scan)

Seq Scan on tasks (cost=0.00..99.51 rows=1040 width=25) (actual time=0.011..0.518 rows=1040 loops=1)
  Filter: (assigned_to = 'Ngozi'::text)
  Rows Removed by Filter: 3961
Execution Time: 0.556 ms

Postgres checked all 5,001 rows one by one, discarding 3,961 that didn't match.

### After index

CREATE INDEX idx_tasks_assigned_to ON tasks (assigned_to);

Bitmap Heap Scan on tasks (cost=16.34..66.34 rows=1040 width=25) (actual time=0.110..0.344 rows=1040 loops=1)
  Recheck Cond: (assigned_to = 'Ngozi'::text)
  ->  Bitmap Index Scan on idx_tasks_assigned_to (cost=0.00..16.08 rows=1040 width=0) (actual time=0.098..0.099 rows=1040 loops=1)
Execution Time: 0.401 ms

### Observation

The query plan changed from a full sequential scan to an index-assisted bitmap scan, and execution time dropped from 0.556ms to 0.401ms (about 28% faster). The improvement is modest at this table size (5,000 rows) — Postgres's planner correctly judges that a sequential scan is already cheap enough here that index overhead barely matters. Indexes pay off more clearly at much larger row counts, where scanning every row becomes genuinely expensive; this is a useful reminder that adding an index is a deliberate trade-off (faster reads, slightly slower writes, extra storage), not something to add reflexively to every column.

## Example request


curl -i -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d "{\"title\":\"Buy milk\"}"


Response:

HTTP/1.1 201 Created

{"id":4,"title":"Buy milk","done":false}



## Swagger UI



Screenshot below shows a successful POST /tasks call tested directly in Swagger UI:



![Swagger screenshot](swagger-screenshot.png)



## Notes



Data is stored in memory only — restarting the server resets the task list back to the 3 example tasks. This is intentional for this stage of the project; persistent storage comes later.
