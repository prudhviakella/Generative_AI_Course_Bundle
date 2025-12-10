# example_usage.py
from db_config import load_db_config
from connector import PostgresConnector
from schema_manager import SchemaManager
from data_manager import DataManager
from csv_loader import CSVLoader

def main():
    cfg = load_db_config("config.ini")
    connector = PostgresConnector(cfg)
    schema_mgr = SchemaManager(connector)
    data_mgr = DataManager(connector)
    csv_loader = CSVLoader(connector)

    schema = cfg.schema

    # Create schema & tables
    schema_mgr.create_schema_if_not_exists(schema)
    schema_mgr.create_customers_orders_tables(schema)

    # Show tables & columns
    print("Tables:", schema_mgr.list_tables(schema))
    print("Customer columns:", schema_mgr.table_columns(schema, "customers"))
    print("Order columns:", schema_mgr.table_columns(schema, "orders"))

    # Insert sample customer and order
    cust = {
        "customer_id": "C001",
        "customer_name": "Rahul",
        "email": "rahul@example.com",
        "city": "Bengaluru",
        "state": "KA",
        "created_at": "2024-01-01 10:00:00"
    }
    data_mgr.insert_customer(schema, cust)

    order = {
        "order_id": "O001",
        "customer_id": "C001",
        "order_date": "2024-11-01 12:30:00",
        "status": "delivered",
        "total_amount": 1200.0
    }
    data_mgr.insert_order(schema, order)

    # Select data
    print("Customers:", data_mgr.select_all(schema, "customers"))
    print("Orders:", data_mgr.select_all(schema, "orders"))

    # Update email
    data_mgr.update_customer_email(schema, "C001", "rahul.new@example.com")
    print("After update:", data_mgr.select_where(schema, "customers", "customer_id = %s", ("C001",)))

    # Delete order
    data_mgr.delete_order(schema, "O001")
    print("Orders after delete:", data_mgr.select_all(schema, "orders"))

    # Example CSV load (uncomment and set actual file paths)
    csv_loader.load_csv_copy("datasets/customers.csv", schema, "customers",
                            columns=["customer_id", "customer_name", "email", "city", "state", "created_at"])
    csv_loader.load_csv_copy("datasets/orders.csv", schema, "orders",
                             columns=["order_id", "customer_id", "order_date", "status", "total_amount"])

if __name__ == "__main__":
    main()