from psycopg2.extras import RealDictCursor
from config.db import get_connection


class PostgresMemory:
    def __init__(self):
        self.conn = get_connection()
        self.conn.autocommit = True

    def add_turn(self, session_id, role, content):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO chat_memory (session_id, role, content)
                VALUES (%s, %s, %s)
                """,
                (session_id, role, content)
            )

    def get_history(self, session_id, limit=10):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT role, content FROM (
                    SELECT role, content, created_at
                    FROM chat_memory
                    WHERE session_id = %s
                    ORDER BY created_at DESC
                    LIMIT %s
                ) sub
                ORDER BY created_at ASC
                """,
                (session_id, limit)
            )

            return cur.fetchall()

    def clear(self, session_id):
        with self.conn.cursor() as cur:
            cur.execute(
                "DELETE FROM chat_memory WHERE session_id = %s",
                (session_id,)
            )