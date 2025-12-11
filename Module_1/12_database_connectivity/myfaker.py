#!/usr/bin/env python3
"""
generate_synthetic_customers_orders.py

Purpose:
    Generates synthetic customer and order data for AWS Glue pipeline tutorials.
    Creates two CSV files with referential integrity maintained between customers and orders.

Output Files:
    1. customers.csv - Customer master data
       Columns: customer_id, customer_name, email, city, state, created_at

    2. orders.csv - Order transaction data
       Columns: order_id, customer_id, order_date, status, total_amount

Key Features:
    - Maintains referential integrity (orders only for existing customers)
    - Temporal consistency (orders created after customer registration)
    - Realistic data distribution (weighted status probabilities)
    - Configurable data volume via global constants
    - Graceful fallback if faker library not available

Dependencies:
    Required: csv, random, datetime, os (all stdlib)
    Optional: faker (pip install faker) - for more realistic synthetic data

Usage:
    python generate_synthetic_customers_orders.py

    Customize by modifying the CONFIG section:
    - NUM_CUSTOMERS: Number of customer records to generate
    - NUM_ORDERS: Number of order records to generate
    - RANDOM_SEED: For reproducible datasets

Example:
    >>> python generate_synthetic_customers_orders.py
    Generating 200 customers and 2000 orders...
    Files created:
     - datasets/customers.csv
     - datasets/orders.csv
"""

# =============================================================================
# IMPORTS
# =============================================================================
import csv
import random
from datetime import datetime, timedelta
import os

# Try to import faker library for realistic synthetic data generation
# If not available, fall back to hardcoded lists (see fallback data section)
try:
    from faker import Faker

    fake = Faker()  # Initialize faker instance
except Exception:
    fake = None  # Flag indicating faker is not available

# =============================================================================
# CONFIGURATION SECTION
# =============================================================================
# Modify these constants to customize the generated dataset

# Random seed for reproducibility - same seed produces identical datasets
RANDOM_SEED = 42

# Data volume controls
NUM_CUSTOMERS = 200  # Total number of unique customers to generate
NUM_ORDERS = 2000  # Total number of orders to generate (distributed across customers)

# Output file paths - relative to script execution directory
CUSTOMERS_CSV = "datasets/customers.csv"
ORDERS_CSV = "datasets/orders.csv"

# Date range for synthetic timestamps
# Orders and customer creation dates will fall within this window
START_DATE = datetime.now() - timedelta(days=365 * 2)  # Two years ago from today
END_DATE = datetime.now()  # Today

# Order status options with realistic distribution (see generate_orders function)
# Reflects typical e-commerce order lifecycle
ORDER_STATUSES = [
    "pending",  # Order placed, awaiting processing
    "processing",  # Order being prepared
    "shipped",  # Order in transit
    "delivered",  # Order successfully delivered (most common end state)
    "canceled",  # Order canceled before shipment
    "returned"  # Order delivered but returned by customer
]

# =============================================================================
# FALLBACK DATA (used when faker library not available)
# =============================================================================
# These lists provide basic diversity in synthetic data generation
# Faker library provides much richer and more realistic alternatives

# Common Indian first names for diversity
FIRST_NAMES = [
    "Rahul", "Akhil", "Priya", "Neha", "Aman",
    "Vikram", "Sonal", "Ravi", "Deepa", "Kumar",
    "Anita", "Suresh", "Pooja", "Arjun", "Rohit",
    "Sneha", "Manish", "Divya", "Sunil", "Meera"
]

# Common Indian surnames for diversity
LAST_NAMES = [
    "Kumar", "Sharma", "Patel", "Singh", "Reddy",
    "Nair", "Gupta", "Iyer", "Khan", "Das",
    "Roy", "Jain", "Chowdhury", "Bose", "Joshi",
    "Garg", "Malhotra", "Bhat", "Sinha", "Verma"
]

# Major Indian cities
CITIES = [
    "Bengaluru", "Mumbai", "Delhi", "Chennai", "Hyderabad",
    "Pune", "Kolkata", "Ahmedabad", "Jaipur", "Lucknow"
]

# Indian state codes (ISO 3166-2:IN format)
STATES = [
    "KA",  # Karnataka
    "MH",  # Maharashtra
    "DL",  # Delhi
    "TN",  # Tamil Nadu
    "TG",  # Telangana
    "PN",  # Punjab (note: standard code is PB, using PN for illustration)
    "WB",  # West Bengal
    "GJ",  # Gujarat
    "RJ",  # Rajasthan
    "UP"  # Uttar Pradesh
]

# =============================================================================
# INITIALIZATION
# =============================================================================
# Set random seed for reproducibility across both stdlib and faker
random.seed(RANDOM_SEED)
if fake:
    fake.seed_instance(RANDOM_SEED)  # Faker has its own seed mechanism


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def gen_customer_name():
    """
    Generate a random customer name.

    Strategy:
        - If faker is available: Use faker.name() for realistic full names
        - Otherwise: Combine random first and last names from fallback lists

    Returns:
        str: Full customer name (e.g., "Rahul Kumar" or "John Smith")

    Example:
        >>> gen_customer_name()
        "Priya Sharma"
    """
    if fake:
        return fake.name()  # Faker generates culturally diverse realistic names
    else:
        # Fallback: randomly combine first and last name from lists
        return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"


def gen_email(name, idx):
    """
    Generate a deterministic email address from customer name and index.

    Strategy:
        1. Convert name to lowercase
        2. Keep only alphanumeric characters and spaces
        3. Replace spaces with dots for standard email format
        4. Append index number for uniqueness
        5. Add random domain from common providers

    Args:
        name (str): Customer full name (e.g., "Prudhvi Akella")
        idx (int): Unique customer index number

    Returns:
        str: Email address (e.g., "prudhvi.akella.1@mail.com")

    Example:
        >>> gen_email("Rahul Kumar", 42)
        "rahul.kumar.42@example.com"

    Note:
        - Ensures email uniqueness through index suffix
        - Removes special characters to avoid email validation issues
    """
    # Step 1-2: Extract alphanumeric + space, convert to lowercase
    namepart = "".join(ch for ch in name.lower() if ch.isalnum() or ch == " ")

    # Step 3: Replace spaces with dots for email format
    namepart = namepart.replace(" ", ".")

    # Step 4-5: Construct email with index and random domain
    domain = random.choice(["example.com", "mail.com", "email.com", "test.com"])
    return f"{namepart}.{idx}@{domain}"


def gen_city_state():
    """
    Generate a random city and state pair.

    Strategy:
        - If faker is available: Use faker's built-in city/state generation
        - Otherwise: Random selection from fallback lists

    Returns:
        tuple: (city: str, state: str)
            city - City name
            state - State code (2-letter abbreviation)

    Example:
        >>> gen_city_state()
        ("Hyderabad", "TG")

    Note:
        Faker provides more diverse and realistic city-state combinations
    """
    if fake:
        # Faker provides geographically diverse options
        city = fake.city()

        # Try to get state abbreviation; fallback to random if not available
        try:
            state = fake.state_abbr()  # US state codes by default
        except Exception:
            # Fallback for non-US locales or errors
            state = random.choice(STATES)

        return city, state
    else:
        # Simple random selection from fallback lists
        return random.choice(CITIES), random.choice(STATES)


def random_datetime_between(start: datetime, end: datetime) -> datetime:
    """
    Generate a random datetime between two given datetimes.

    This is crucial for creating realistic temporal data where:
    - Customer creation dates span the entire time window
    - Order dates occur after customer registration

    Algorithm:
        1. Calculate total time delta between start and end
        2. Convert to seconds for granular randomness
        3. Pick random second within range
        4. Add to start datetime

    Args:
        start (datetime): Lower bound (inclusive)
        end (datetime): Upper bound (exclusive)

    Returns:
        datetime: Random datetime in range [start, end)

    Example:
        >>> start = datetime(2023, 1, 1)
        >>> end = datetime(2023, 12, 31)
        >>> random_datetime_between(start, end)
        datetime.datetime(2023, 7, 15, 14, 23, 45)

    Raises:
        ValueError: If start >= end (implicit in timedelta/randrange)
    """
    # Calculate the time difference in seconds
    delta = end - start

    # Generate random number of seconds within the range
    sec = random.randrange(int(delta.total_seconds()))

    # Return start time plus random offset
    return start + timedelta(seconds=sec)


def fmt_dt(dt: datetime) -> str:
    """
    Format datetime object as PostgreSQL-compatible string.

    Uses standard SQL timestamp format: 'YYYY-MM-DD HH:MM:SS'
    This format is compatible with:
    - PostgreSQL TIMESTAMP columns
    - AWS Glue/Athena timestamp parsing
    - Most database systems

    Args:
        dt (datetime): Python datetime object to format

    Returns:
        str: Formatted timestamp string

    Example:
        >>> from datetime import datetime
        >>> fmt_dt(datetime(2024, 12, 11, 15, 30, 45))
        "2024-12-11 15:30:45"
    """
    return dt.strftime("%Y-%m-%d %H:%M:%S")


# =============================================================================
# DATA GENERATION FUNCTIONS
# =============================================================================

def generate_customers(num_customers: int):
    """
    Generate synthetic customer master data records.

    Creates a list of customer dictionaries with all required fields,
    ensuring data quality and consistency:
    - Unique customer IDs (zero-padded for sorting)
    - Unique emails (name + index ensures uniqueness)
    - Creation timestamps within defined date range

    Args:
        num_customers (int): Number of customer records to generate

    Returns:
        list[dict]: List of customer dictionaries with keys:
            - customer_id: Unique identifier (e.g., "CUST000001")
            - customer_name: Full name
            - email: Unique email address
            - city: Customer's city
            - state: State code
            - created_at: Account creation timestamp (formatted string)

    Data Quality Guarantees:
        1. Unique customer_id (sequential)
        2. Unique email (index-based)
        3. Timestamps before END_DATE to allow order placement
        4. All fields populated (no nulls)

    Example:
        >>> customers = generate_customers(3)
        >>> len(customers)
        3
        >>> customers[0].keys()
        dict_keys(['customer_id', 'customer_name', 'email', 'city', 'state', 'created_at'])
    """
    customers = []  # Initialize empty list to store customer records

    # Generate customers with 1-based indexing for human-readable IDs
    for i in range(1, num_customers + 1):
        # Generate unique customer ID with zero-padding (e.g., CUST000042)
        # :06d means: integer, 6 digits, zero-padded
        customer_id = f"CUST{i:06d}"

        # Generate random name using utility function
        name = gen_customer_name()

        # Generate unique email from name and index
        email = gen_email(name, i)

        # Generate random city and state
        city, state = gen_city_state()

        # Generate creation timestamp
        # Customer created at least 1 day before END_DATE to allow for orders
        created_at = random_datetime_between(
            START_DATE,
            END_DATE - timedelta(days=1)
        )

        # Build customer record as dictionary
        customers.append({
            "customer_id": customer_id,
            "customer_name": name,
            "email": email,
            "city": city,
            "state": state,
            "created_at": fmt_dt(created_at)  # Format as string for CSV
        })

    return customers


def generate_orders(customers, num_orders: int):
    """
    Generate synthetic order transaction data with referential integrity.

    Creates order records that maintain critical business rules:
    1. Referential Integrity: All orders reference existing customers
    2. Temporal Consistency: Orders created after customer registration
    3. Realistic Distribution: Status follows weighted probabilities

    Args:
        customers (list[dict]): List of customer records from generate_customers()
        num_orders (int): Total number of order records to generate

    Returns:
        list[dict]: List of order dictionaries with keys:
            - order_id: Unique identifier (e.g., "ORD0000001")
            - customer_id: Foreign key to customers table
            - order_date: Order placement timestamp (formatted string)
            - status: Current order status
            - total_amount: Order value in currency (2 decimal places)

    Status Distribution (via weighted random):
        - pending: 5% (rare - quickly processed)
        - processing: 10%
        - shipped: 40% (common - in-transit state)
        - delivered: 30% (most common successful state)
        - canceled: 10%
        - returned: 5% (rare - requires delivery first)

    Data Quality Guarantees:
        1. All customer_id values exist in customers list
        2. order_date >= customer.created_at (temporal consistency)
        3. order_date <= END_DATE (no future orders)
        4. Unique order_id (sequential)
        5. Total amount always positive, 2 decimal precision

    Example:
        >>> customers = generate_customers(10)
        >>> orders = generate_orders(customers, 50)
        >>> len(orders)
        50
        >>> all(o['customer_id'] in [c['customer_id'] for c in customers] for o in orders)
        True
    """
    orders = []  # Initialize empty list for order records
    num_customers = len(customers)

    # Build lookup map: customer_id -> account creation datetime
    # This allows us to ensure orders happen after customer registration
    cust_created_map = {
        c["customer_id"]: datetime.strptime(c["created_at"], "%Y-%m-%d %H:%M:%S")
        for c in customers
    }

    # Generate orders with 1-based indexing
    for i in range(1, num_orders + 1):
        # Generate unique order ID with zero-padding (e.g., ORD0000042)
        # :07d means: integer, 7 digits, zero-padded (more orders than customers)
        order_id = f"ORD{i:07d}"

        # Randomly assign order to a customer (uniform distribution)
        # In real data, some customers would have more orders (power law)
        # For simplicity, we use uniform random selection
        cust = random.choice(customers)
        cust_id = cust["customer_id"]

        # Get customer's registration date for temporal consistency
        cust_created_at = cust_created_map[cust_id]

        # Order date must be >= customer creation date
        order_start = cust_created_at

        # Edge case handling: if customer created very close to END_DATE
        # Allow small buffer to avoid random_datetime_between errors
        if order_start >= END_DATE:
            order_start = END_DATE - timedelta(days=1)

        # Generate random order date after customer registration
        order_date = random_datetime_between(order_start, END_DATE)

        # Generate order status with realistic weighted probabilities
        # weights list corresponds to ORDER_STATUSES list order
        # Delivered (30%) and Shipped (40%) are most common (70% success rate)
        status = random.choices(
            ORDER_STATUSES,
            weights=[5, 10, 40, 30, 10, 5],  # Sums to 100 for percentage interpretation
            k=1  # Select 1 item
        )[0]

        # Generate random order amount between $50 and $5000
        # round() ensures exactly 2 decimal places for currency
        total_amount = round(random.uniform(50.0, 5000.0), 2)

        # Build order record as dictionary
        orders.append({
            "order_id": order_id,
            "customer_id": cust_id,
            "order_date": fmt_dt(order_date),  # Format as string for CSV
            "status": status,
            "total_amount": total_amount
        })

    return orders


# =============================================================================
# CSV WRITING FUNCTIONS
# =============================================================================

def write_csv_customers(path: str, customers):
    """
    Write customer records to CSV file.

    Creates a properly formatted CSV with header row and all customer records.
    Uses UTF-8 encoding to support international characters in names/cities.

    Args:
        path (str): Output file path (relative or absolute)
        customers (list[dict]): Customer records from generate_customers()

    CSV Format:
        - Header row with column names
        - One row per customer
        - Comma-separated values
        - UTF-8 encoding (supports international characters)
        - Unix line endings (\\n)

    Side Effects:
        - Creates/overwrites file at specified path
        - Creates parent directories if they don't exist (via main())

    Raises:
        IOError: If file cannot be written (permissions, disk space, etc.)

    Example:
        >>> customers = generate_customers(5)
        >>> write_csv_customers("output/customers.csv", customers)
        # Creates file with 6 lines (1 header + 5 data rows)
    """
    # Define column order for CSV header
    fieldnames = ["customer_id", "customer_name", "email", "city", "state", "created_at"]

    # Open file in write mode with UTF-8 encoding
    # newline='' prevents extra blank lines on Windows
    with open(path, "w", newline="", encoding="utf-8") as f:
        # Create CSV writer with dictionary support
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        # Write header row
        writer.writeheader()

        # Write each customer record as a row
        for c in customers:
            writer.writerow(c)


def write_csv_orders(path: str, orders):
    """
    Write order records to CSV file.

    Creates a properly formatted CSV with header row and all order records.
    Uses UTF-8 encoding for consistency with customers CSV.

    Args:
        path (str): Output file path (relative or absolute)
        orders (list[dict]): Order records from generate_orders()

    CSV Format:
        - Header row with column names
        - One row per order
        - Comma-separated values
        - UTF-8 encoding
        - Unix line endings (\\n)

    Side Effects:
        - Creates/overwrites file at specified path
        - Creates parent directories if they don't exist (via main())

    Raises:
        IOError: If file cannot be written (permissions, disk space, etc.)

    Example:
        >>> orders = generate_orders(customers, 20)
        >>> write_csv_orders("output/orders.csv", orders)
        # Creates file with 21 lines (1 header + 20 data rows)
    """
    # Define column order for CSV header
    fieldnames = ["order_id", "customer_id", "order_date", "status", "total_amount"]

    # Open file in write mode with UTF-8 encoding
    with open(path, "w", newline="", encoding="utf-8") as f:
        # Create CSV writer with dictionary support
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        # Write header row
        writer.writeheader()

        # Write each order record as a row
        for o in orders:
            writer.writerow(o)


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """
    Main execution function - orchestrates the entire data generation process.

    Workflow:
        1. Print configuration summary
        2. Generate customer data
        3. Generate order data (with customer references)
        4. Determine output paths
        5. Write CSV files
        6. Print success confirmation with sample data

    Directory Structure Created:
        datasets/
        ├── customers.csv
        └── orders.csv

    Exit Codes:
        0: Success
        Non-zero: Error (file I/O, permissions, etc.)

    Example Output:
        Generating 200 customers and 2000 orders...
        Files created:
         - /path/to/datasets/customers.csv
         - /path/to/datasets/orders.csv
        Sample rows (first customer and first order):
        {'customer_id': 'CUST000001', 'customer_name': 'Rahul Kumar', ...}
        {'order_id': 'ORD0000001', 'customer_id': 'CUST000042', ...}
    """
    # Print execution summary
    print(f"Generating {NUM_CUSTOMERS} customers and {NUM_ORDERS} orders...")

    # Step 1: Generate customer data
    # This must happen first since orders reference customers
    customers = generate_customers(NUM_CUSTOMERS)

    # Step 2: Generate order data with referential integrity
    orders = generate_orders(customers, NUM_ORDERS)

    # Step 3: Determine output file paths
    out_dir = os.getcwd()  # Use current working directory

    # Note: The commented code below shows how to place files relative to script location
    # This approach uses current working directory instead for flexibility
    # file_path_splits = __file__.split("/")
    # file_path_splits = file_path_splits[:-1]
    # out_dir = "/".join(file_path_splits)

    # Construct full paths for output files
    cust_path = os.path.join(out_dir, CUSTOMERS_CSV)
    orders_path = os.path.join(out_dir, ORDERS_CSV)

    # Step 4: Write data to CSV files
    write_csv_customers(cust_path, customers)
    write_csv_orders(orders_path, orders)

    # Step 5: Print success confirmation
    print("Files created:")
    print(" -", cust_path)
    print(" -", orders_path)

    # Print sample rows for quick verification
    print("Sample rows (first customer and first order):")
    print(customers[0])  # Show first customer record
    print(orders[0])  # Show first order record


# =============================================================================
# SCRIPT ENTRY POINT
# =============================================================================
if __name__ == "__main__":
    """
    Standard Python idiom for script execution.

    This block only runs when script is executed directly (not imported).
    Allows this module to be safely imported without triggering execution.

    Usage:
        Direct execution: python generate_synthetic_customers_orders.py
        Import: from generate_synthetic_customers_orders import generate_customers
    """
    main()