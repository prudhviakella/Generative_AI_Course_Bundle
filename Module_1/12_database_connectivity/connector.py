# connector.py
import psycopg2
from typing import Optional
from contextlib import contextmanager
from db_config import DBConfig

class PostgresConnector:
    """
    Thin wrapper over psycopg2 connection.
    Supports use as context manager via .connect() method or manual open/close.
    """

    def __init__(self, cfg: DBConfig):
        self.cfg = cfg
        self.conn: Optional[psycopg2.extensions.connection] = None
        self.cur: Optional[psycopg2.extensions.cursor] = None

    def open(self):
        """Open connection and a cursor (if not already open)."""
        if self.conn is None:
            self.conn = psycopg2.connect(
                host=self.cfg.host,
                port=self.cfg.port,
                dbname=self.cfg.dbname,
                user=self.cfg.user,
                password=self.cfg.password,
            )
            self.cur = self.conn.cursor()

    def close(self):
        """Close cursor and connection safely."""
        try:
            if self.cur:
                self.cur.close()
        except Exception:
            pass
        try:
            if self.conn:
                self.conn.close()
        except Exception:
            pass
        self.cur = None
        self.conn = None

    @contextmanager
    def connect(self):
        """
        Context manager that opens connection, yields (conn, cur) and ensures close.
        Usage:
            with pg.connect() as (conn, cur):
                cur.execute(...)
        """
        try:
            self.open()
            yield (self.conn, self.cur)
        finally:
            self.close()

    def commit(self):
        if self.conn:
            self.conn.commit()