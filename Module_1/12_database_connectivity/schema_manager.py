# schema_manager.py
from psycopg2 import sql
from connector import PostgresConnector

class SchemaManager:
    def __init__(self, connector: PostgresConnector):
        self.connector = connector

    def create_schema_if_not_exists(self, schema_name: str):
        with self.connector.connect() as (conn, cur):
            cur.execute(sql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(sql.Identifier(schema_name)))
            conn.commit()

    def drop_schema(self, schema_name: str, cascade: bool = False):
        with self.connector.connect() as (conn, cur):
            cur.execute(
                sql.SQL("DROP SCHEMA IF EXISTS {} {}").format(
                    sql.Identifier(schema_name),
                    sql.SQL("CASCADE") if cascade else sql.SQL("RESTRICT")
                )
            )
            conn.commit()

    def create_customers_orders_tables(self, schema: str = "public"):
        """
        Create customers and orders tables. Keep columns generic to accommodate datasets.
        """
        create_customers = sql.SQL("""
            CREATE TABLE IF NOT EXISTS {}.customers (
                customer_id   TEXT PRIMARY KEY,
                customer_name TEXT,
                email         TEXT,
                city          TEXT,
                state         TEXT,
                created_at    TIMESTAMP
            );
        """).format(sql.Identifier(schema))

        create_orders = sql.SQL("""
            CREATE TABLE IF NOT EXISTS {}.orders (
                order_id     TEXT PRIMARY KEY,
                customer_id  TEXT REFERENCES {}.customers(customer_id),
                order_date   TIMESTAMP,
                status       TEXT,
                total_amount NUMERIC
            );
        """).format(sql.Identifier(schema), sql.Identifier(schema))

        with self.connector.connect() as (conn, cur):
            cur.execute(create_customers)
            cur.execute(create_orders)
            conn.commit()

    def drop_tables(self, schema: str = "public"):
        with self.connector.connect() as (conn, cur):
            cur.execute(sql.SQL("DROP TABLE IF EXISTS {}.orders CASCADE").format(sql.Identifier(schema)))
            cur.execute(sql.SQL("DROP TABLE IF EXISTS {}.customers CASCADE").format(sql.Identifier(schema)))
            conn.commit()

    def list_tables(self, schema: str = "public"):
        with self.connector.connect() as (conn, cur):
            cur.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = %s
                  AND table_type = 'BASE TABLE'
                ORDER BY table_name;
            """, (schema,))
            return cur.fetchall()

    def table_columns(self, schema: str, table: str):
        with self.connector.connect() as (conn, cur):
            cur.execute("""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_schema = %s AND table_name = %s
                ORDER BY ordinal_position;
            """, (schema, table))
            return cur.fetchall()