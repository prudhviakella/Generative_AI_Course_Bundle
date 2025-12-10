# data_manager.py
from psycopg2 import sql
from connector import PostgresConnector
from typing import Dict, Any, Tuple, List

class DataManager:
    def __init__(self, connector: PostgresConnector):
        self.connector = connector

    # Generic SELECT ALL
    def select_all(self, schema: str, table: str, limit: int = 100) -> List[Tuple[Any]]:
        with self.connector.connect() as (conn, cur):
            q = sql.SQL("SELECT * FROM {}.{} LIMIT %s").format(sql.Identifier(schema), sql.Identifier(table))
            cur.execute(q, (limit,))
            return cur.fetchall()

    def select_where(self, schema: str, table: str, where_clause: str, params: Tuple = (), limit: int = 100):
        with self.connector.connect() as (conn, cur):
            q = sql.SQL("SELECT * FROM {}.{} WHERE " + where_clause + " LIMIT %s").format(sql.Identifier(schema), sql.Identifier(table))
            cur.execute(q, params + (limit,))
            return cur.fetchall()

    def insert_customer(self, schema: str, customer: Dict[str, Any]):
        with self.connector.connect() as (conn, cur):
            q = sql.SQL("""
                INSERT INTO {}.customers (customer_id, customer_name, email, city, state, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (customer_id) DO UPDATE SET
                  customer_name = EXCLUDED.customer_name,
                  email = EXCLUDED.email,
                  city = EXCLUDED.city,
                  state = EXCLUDED.state,
                  created_at = EXCLUDED.created_at;
            """).format(sql.Identifier(schema))
            cur.execute(q, (
                customer.get("customer_id"),
                customer.get("customer_name"),
                customer.get("email"),
                customer.get("city"),
                customer.get("state"),
                customer.get("created_at")
            ))
            conn.commit()

    def insert_order(self, schema: str, order: Dict[str, Any]):
        with self.connector.connect() as (conn, cur):
            q = sql.SQL("""
                INSERT INTO {}.orders (order_id, customer_id, order_date, status, total_amount)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (order_id) DO UPDATE SET
                  customer_id = EXCLUDED.customer_id,
                  order_date = EXCLUDED.order_date,
                  status = EXCLUDED.status,
                  total_amount = EXCLUDED.total_amount;
            """).format(sql.Identifier(schema))
            cur.execute(q, (
                order.get("order_id"),
                order.get("customer_id"),
                order.get("order_date"),
                order.get("status"),
                order.get("total_amount")
            ))
            conn.commit()

    def update_customer_email(self, schema: str, customer_id: str, new_email: str):
        with self.connector.connect() as (conn, cur):
            q = sql.SQL("UPDATE {}.customers SET email = %s WHERE customer_id = %s").format(sql.Identifier(schema))
            cur.execute(q, (new_email, customer_id))
            conn.commit()

    def delete_order(self, schema: str, order_id: str):
        with self.connector.connect() as (conn, cur):
            q = sql.SQL("DELETE FROM {}.orders WHERE order_id = %s").format(sql.Identifier(schema))
            cur.execute(q, (order_id,))
            conn.commit()

    # Run arbitrary query (returns fetchall or None)
    def run_query(self, query: str, params: Tuple = ()):
        with self.connector.connect() as (conn, cur):
            cur.execute(query, params)
            try:
                return cur.fetchall()
            except Exception:
                return None