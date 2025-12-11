#!/usr/bin/env python3
"""
generate_synthetic_customers_orders.py

Generates two CSVs:
 - customers.csv
 - orders.csv

Columns (matches the DB schema used previously):

customers.csv:
    customer_id,customer_name,email,city,state,created_at

orders.csv:
    order_id,customer_id,order_date,status,total_amount

Configurable: number of customers and orders.
If `faker` is installed it will be used for more realistic names/cities.
"""

import csv
import random
from datetime import datetime, timedelta
import os

# Try to use faker if available for better names/cities; otherwise fall back to lists
try:
    from faker import Faker
    fake = Faker()
except Exception:
    fake = None

# -------------------------
# CONFIG
# -------------------------
RANDOM_SEED = 42
NUM_CUSTOMERS = 200      # change as needed
NUM_ORDERS = 2000        # change as needed
CUSTOMERS_CSV = "datasets/customers.csv"
ORDERS_CSV = "datasets/orders.csv"
#
START_DATE = datetime.now() - timedelta(days=365 * 2)  # two years ago
END_DATE = datetime.now()

ORDER_STATUSES = ["pending", "processing", "shipped", "delivered", "canceled", "returned"]

# A small fallback list of first/last names & cities/states if faker not installed
FIRST_NAMES = ["Rahul", "Akhil", "Priya", "Neha", "Aman", "Vikram", "Sonal", "Ravi", "Deepa", "Kumar",
               "Anita", "Suresh", "Pooja", "Arjun", "Rohit", "Sneha", "Manish", "Divya", "Sunil", "Meera"]
LAST_NAMES = ["Kumar", "Sharma", "Patel", "Singh", "Reddy", "Nair", "Gupta", "Iyer", "Khan", "Das",
              "Roy", "Jain", "Chowdhury", "Bose", "Joshi", "Garg", "Malhotra", "Bhat", "Sinha", "Verma"]
CITIES = ["Bengaluru", "Mumbai", "Delhi", "Chennai", "Hyderabad", "Pune", "Kolkata", "Ahmedabad", "Jaipur", "Lucknow"]
STATES = ["KA", "MH", "DL", "TN", "TG", "PN", "WB", "GJ", "RJ", "UP"]

# -------------------------
# Utilities
# -------------------------
random.seed(RANDOM_SEED)
if fake:
    fake.seed_instance(RANDOM_SEED)

def gen_customer_name():
    if fake:
        return fake.name()
    else:
        return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"

def gen_email(name, idx):
    # simple deterministic email from name and index
    #Example = Prudhvi Akella -> prudhvi.akella.1@mail.com
    namepart = "".join(ch for ch in name.lower() if ch.isalnum() or ch == " ").replace(" ", ".")
    domain = random.choice(["example.com", "mail.com", "email.com", "test.com"])
    return f"{namepart}.{idx}@{domain}"

def gen_city_state():
    if fake:
        # faker provides city + state
        city = fake.city()
        # state code fallback: try to take state_abbr if available
        try:
            state = fake.state_abbr()
        except Exception:
            state = random.choice(STATES)
        return city, state
    else:
        return random.choice(CITIES), random.choice(STATES)

def random_datetime_between(start: datetime, end: datetime) -> datetime:
    """Return a random datetime between start and end."""
    delta = end - start
    sec = random.randrange(int(delta.total_seconds()))
    return start + timedelta(seconds=sec)

def fmt_dt(dt: datetime) -> str:
    """Format datetime as 'YYYY-MM-DD HH:MM:SS' (Postgres-friendly)."""
    return dt.strftime("%Y-%m-%d %H:%M:%S")

# -------------------------
# Generate customers
# -------------------------
def generate_customers(num_customers: int):
    customers = []
    for i in range(1, num_customers + 1):
        customer_id = f"CUST{i:06d}"
        name = gen_customer_name()
        email = gen_email(name, i)
        city, state = gen_city_state()
        # created_at between START_DATE and END_DATE
        created_at = random_datetime_between(START_DATE, END_DATE - timedelta(days=1))
        customers.append({
            "customer_id": customer_id,
            "customer_name": name,
            "email": email,
            "city": city,
            "state": state,
            "created_at": fmt_dt(created_at)
        })
    return customers

# -------------------------
# Generate orders (referential integrity)
# -------------------------
def generate_orders(customers, num_orders: int):
    orders = []
    num_customers = len(customers)
    # Build mapping from index to created_at for ensuring order_date >= created_at (mostly)
    cust_created_map = {c["customer_id"]: datetime.strptime(c["created_at"], "%Y-%m-%d %H:%M:%S") for c in customers}
    for i in range(1, num_orders + 1):
        order_id = f"ORD{i:07d}"
        # choose a random customer uniformly
        cust = random.choice(customers)
        cust_id = cust["customer_id"]
        cust_created_at = cust_created_map[cust_id]
        # order_date is after customer created_at (or same day) and before END_DATE
        order_start = cust_created_at
        # if start is too close to END_DATE, allow slight jitter
        if order_start >= END_DATE:
            order_start = END_DATE - timedelta(days=1)

        order_date = random_datetime_between(order_start, END_DATE)
        status = random.choices(
            ORDER_STATUSES,
            weights=[5, 10, 40, 30, 10, 5],  # weighted so most become delivered/shipped
            k=1
        )[0]
        # total amount: random between 50 and 5000, with 2 decimals
        total_amount = round(random.uniform(50.0, 5000.0), 2)

        orders.append({
            "order_id": order_id,
            "customer_id": cust_id,
            "order_date": fmt_dt(order_date),
            "status": status,
            "total_amount": total_amount
        })
    return orders

# -------------------------
# Write CSV helpers
# -------------------------
def write_csv_customers(path: str, customers):
    fieldnames = ["customer_id", "customer_name", "email", "city", "state", "created_at"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for c in customers:
            writer.writerow(c)

def write_csv_orders(path: str, orders):
    fieldnames = ["order_id", "customer_id", "order_date", "status", "total_amount"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for o in orders:
            writer.writerow(o)

# -------------------------
# Main
# -------------------------
def main():
    print(f"Generating {NUM_CUSTOMERS} customers and {NUM_ORDERS} orders...")
    customers = generate_customers(NUM_CUSTOMERS)
    orders = generate_orders(customers, NUM_ORDERS)

    # Ensure output folder exists (current)
    out_dir = os.getcwd()
    # file_path_splits = __file__.split("/")
    # file_path_splits = file_path_splits[:-1]
    # print("/".join(file_path_splits))
    cust_path = os.path.join(out_dir, CUSTOMERS_CSV)
    orders_path = os.path.join(out_dir, ORDERS_CSV)

    write_csv_customers(cust_path, customers)
    write_csv_orders(orders_path, orders)

    print("Files created:")
    print(" -", cust_path)
    print(" -", orders_path)
    print("Sample rows (first customer and first order):")
    print(customers[0])
    print(orders[0])

if __name__ == "__main__":
    main()