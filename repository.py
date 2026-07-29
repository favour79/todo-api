import os
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    return psycopg2.connect(DATABASE_URL)


def get_all_tasks():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT * FROM tasks ORDER BY id")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_task_by_id(task_id):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def create_task(title):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute(
        "INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING *",
        (title, False)
    )
    new_task = cursor.fetchone()
    conn.commit()
    conn.close()
    return dict(new_task)


def update_task(task_id, title=None, done=None):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    existing = cursor.fetchone()

    if existing is None:
        conn.close()
        return None

    new_title = title if title is not None else existing["title"]
    new_done = done if done is not None else existing["done"]

    cursor.execute(
        "UPDATE tasks SET title = %s, done = %s WHERE id = %s RETURNING *",
        (new_title, new_done, task_id)
    )
    updated = cursor.fetchone()
    conn.commit()
    conn.close()
    return dict(updated)


def delete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM tasks WHERE id = %s", (task_id,))
    existing = cursor.fetchone()

    if existing is None:
        conn.close()
        return False

    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()
    conn.close()
    return True