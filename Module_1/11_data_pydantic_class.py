from dataclasses import dataclass
from datetime import date

# ==============================================================
# WHAT IS A DATACLASS?
# --------------------------------------------------------------
# A dataclass is a special kind of class designed to hold data.
# Python automatically generates:
#   - __init__
#   - __repr__
#   - __eq__
#   - __hash__ (optional)
#
# HOW IS IT DIFFERENT FROM A NORMAL CLASS?
#   Normal class:
#       - You must write __init__ manually
#       - No auto eq / repr
#
#   Dataclass:
#       - Boilerplate generated automatically
#       - Cleaner and easier for "data holder" objects
#
# IMPORTANT:
#   Dataclasses DO NOT do runtime type validation.
#   If you pass wrong types, Python will still allow it.
# ==============================================================

@dataclass
class Employee:
    name: str
    emp_id: int
    department: str
    joining_date: date
    salary: float = 50000.0   # default value

# Creating objects
e1 = Employee("Rahul", 101, "IT", date(2024, 1, 1))
e2 = Employee("Akhil", 102, "Finance", date(2023, 6, 15), salary=75000)

print(e1)  # Auto-generated __repr__
print(e2)

# Comparing two employees (auto-generated __eq__)
print("Are equal:", e1 == e2)



# ==============================================================
# DATACLASS WITH VALIDATION (__post_init__)
# --------------------------------------------------------------
# Since dataclasses do NOT validate types or values by themselves,
# we must manually validate inside __post_init__().
#
# __post_init__ runs immediately after __init__ finishes.
# ==============================================================

from dataclasses import dataclass

@dataclass
class Product:
    name: str
    price: float
    quantity: int

    def __post_init__(self):
        if self.price < 0:
            raise ValueError("Price cannot be negative")
        if self.quantity < 0:
            raise ValueError("Quantity cannot be negative")

p = Product("Laptop", 55000.0, 10)
print(p)

# ==============================================================
# WHAT IS A PYDANTIC MODEL?
# --------------------------------------------------------------
# Pydantic BaseModel is used for VALIDATED data models.
#
# DIFFERENCES FROM DATACLASS:
#   - Validates data types at runtime ✔
#   - Converts types automatically ✔  ("123" → int 123)
#   - Rejects invalid data with clear errors ✔
#   - Provides JSON support .json(), .dict(), etc.
#
# Dataclass is for internal structured data,
# Pydantic is for INPUT VALIDATION (API, JSON, configs).
# ==============================================================

from pydantic import BaseModel, EmailStr, Field

class User(BaseModel):
    # Field() allows constraints and validation rules
    username: str = Field(min_length=3, max_length=20)
    email: EmailStr  # Validated email
    age: int = Field(ge=18, le=100)

# VALID EXAMPLE
user1 = User(username="prudhvi", email="test@example.com", age=25)
print(user1)

# INVALID EXAMPLE
try:
    User(username="ab", email="invalid_email", age=10)
except Exception as e:
    print("Validation Error:", e)



# ==============================================================
# PYDANTIC AUTO TYPE CONVERSION
# --------------------------------------------------------------
# Pydantic can convert:
#   "123"   → 123
#   "99.9"  → 99.9
#   "true"  → True
# ==============================================================

class Order(BaseModel):
    order_id: int
    price: float
    is_paid: bool

o = Order(order_id="123", price="199.99", is_paid="true")

print(o)
print("Types:", type(o.order_id), type(o.price), type(o.is_paid))



# ==============================================================
# PYDANTIC NESTED MODEL EXAMPLE
# --------------------------------------------------------------
# Pydantic automatically converts list of dicts → list of Item objects.
# Useful for invoices, orders, APIs, nested JSON.
# ==============================================================

from typing import List

class Item(BaseModel):
    name: str
    quantity: int
    price: float

class Invoice(BaseModel):
    invoice_id: str
    items: List[Item]

invoice = Invoice(
    invoice_id="INV123",
    items=[
        {"name": "Laptop", "quantity": 1, "price": 55000},
        {"name": "Mouse",  "quantity": 2, "price": 500}
    ]
)

print(invoice)

# ==============================================================
# DATACLASS VS PYDANTIC: SUMMARY
# --------------------------------------------------------------
# - Dataclass: simple data holder, no validation
# - Pydantic: validated model, auto type conversion
# ==============================================================
# dataclass: developer must validate
from dataclasses import dataclass
@dataclass
class ProductDC:
    name: str
    price: float
    def __post_init__(self):
        if self.price < 0:
            raise ValueError("price < 0")

# pydantic: validates and converts automatically
from pydantic import BaseModel, Field
class ProductPD(BaseModel):
    name: str
    price: float = Field(gt=0)  # pydantic raises error if invalid

# Usage
p_dc = ProductDC("x", 100.0)          # ok
p_pd = ProductPD(name="x", price="100.0")  # price converted to float