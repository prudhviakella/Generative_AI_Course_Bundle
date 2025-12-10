# csv_loader.py (replace the load_csv_copy method with this)
import os
from psycopg2 import sql
from connector import PostgresConnector
from typing import List, Optional

class CSVLoader:
    def __init__(self, connector: PostgresConnector):
        self.connector = connector

    def load_csv_copy(self, csv_path: str, schema: str, table: str,
                      columns: Optional[List[str]] = None,
                      delimiter: str = ",", null_str: str = ""):
        """
        Use COPY FROM STDIN via psycopg2.copy_expert to bulk load CSV file.

        NOTE: copy_expert requires a complete SQL string (no parameter placeholders).
        We build the SQL using psycopg2.sql to safely format identifiers and literals.
        """
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"{csv_path} not found")

        # Prepare column list if provided
        if columns:
            cols_sql = sql.SQL(", ").join(sql.Identifier(c) for c in columns)
            cols_fragment = sql.SQL("({})").format(cols_sql)
        else:
            cols_fragment = sql.SQL("")

        # Use sql.Literal for delimiter and null representation to ensure proper quoting
        copy_sql = sql.SQL(
            "COPY {}.{} {} FROM STDIN WITH CSV HEADER DELIMITER {} NULL {}"
        ).format(
            sql.Identifier(schema),
            sql.Identifier(table),
            cols_fragment,
            sql.Literal(delimiter),
            sql.Literal(null_str)
        )

        # Make sure connection is open (we need the raw connection object for copy_expert)
        self.connector.open()
        try:
            with open(csv_path, "r", encoding="utf-8") as f:
                # copy_expert expects a SQL string, so we pass the fully formatted SQL
                self.connector.cur.copy_expert(copy_sql.as_string(self.connector.conn), f, size=8192)
            self.connector.commit()
        finally:
            self.connector.close()