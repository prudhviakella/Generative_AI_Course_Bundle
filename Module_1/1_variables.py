"""
===============================================================
PYTHON BASICS: DATA TYPES, FUNCTIONS, MUTABILITY, COMMON OPS
===============================================================

WHAT THIS MODULE COVERS (top-of-module summary):
- Data types: int, float, str, list, tuple, dict, set
- Accessing elements (forward & reverse indexing)
- Mutable vs Immutable (definition + examples)
- What a function is (input -> compute -> return)
- Built-in helpers covered: print(), type(), len(), int(), float(), str()
- Examples showing common errors (immutability, wrong len() usage)

DEFINITIONS:
- IMMUTABLE: An object whose state or contents cannot be changed after it is created.
             Examples: int, float, str, tuple
- MUTABLE:   An object whose contents can be changed after creation.
             Examples: list, dict, set

- FUNCTION (simple definition): A named block of code that optionally takes inputs (arguments),
  performs operations, and optionally returns a value. Example: len("abc") -> returns 3
"""

# -------------------------------------------------------------
# INT (Integer)
# -------------------------------------------------------------
age = 25
print("INT:", age)
print("Type:", type(age))
print("Memory size:", age.__sizeof__(), "bytes")
# len() does NOT work on int -> demonstrates an error
try:
    print("len(age):", len(age))
except TypeError as e:
    print("len() error on int (expected):", e)
print("-" * 70)


# -------------------------------------------------------------
# FLOAT (Decimal Number)
# -------------------------------------------------------------
salary = 45000.75
print("FLOAT:", salary)
print("Type:", type(salary))
print("Memory size:", salary.__sizeof__(), "bytes")
# len() does NOT work on float either
try:
    print("len(salary):", len(salary))
except TypeError as e:
    print("len() error on float (expected):", e)
print("-" * 70)


# -------------------------------------------------------------
# STRING (IMMUTABLE) - len() example included
# -------------------------------------------------------------
message = "Hello Python"
print("STRING:", message)
print("Type:", type(message))
print("Memory size:", message.__sizeof__(), "bytes")

print("Forward index [0]:", message[0])
print("Reverse index [-1]:", message[-1])
print("Length of string (len):", len(message))  # <-- len() example

# Immutable example (will raise error)
try:
    message[0] = "h"
except TypeError as e:
    print("String immutability error (expected):", e)

print("-" * 70)


# -------------------------------------------------------------
# LIST (Mutable) - len() example included
# -------------------------------------------------------------
numbers = [10, 20, 30, 40]
print("LIST:", numbers)
print("Type:", type(numbers))
print("Memory size:", numbers.__sizeof__(), "bytes")

print("Forward index [0]:", numbers[0])
print("Reverse index [-1]:", numbers[-1])
print("Length of list (len):", len(numbers))  # <-- len() example

# list is mutable
numbers[0] = 99
print("Modified list (mutability example):", numbers)

print("-" * 70)


# -------------------------------------------------------------
# TUPLE (Immutable) - len() example included
# -------------------------------------------------------------
point = (5, 10, 15)
print("TUPLE:", point)
print("Type:", type(point))
print("Memory size:", point.__sizeof__(), "bytes")

print("Forward index [0]:", point[0])
print("Reverse index [-1]:", point[-1])
print("Length of tuple (len):", len(point))  # <-- len() example

# Immutable example (will raise error)
try:
    point[0] = 100
except TypeError as e:
    print("Tuple immutability error (expected):", e)

print("-" * 70)


# -------------------------------------------------------------
# DICT (Mutable key-value store) - len() example included
# -------------------------------------------------------------
student = {"name": "Rahul", "age": 21, "courses": ["Python", "ML"]}
print("DICT:", student)
print("Type:", type(student))
print("Memory size:", student.__sizeof__(), "bytes")

# len(dict) returns number of keys
print("Length of dict (number of keys):", len(student))  # <-- len() example
print("Access name:", student["name"])
print("Access age:", student["age"])

# modify dictionary (mutable)
student["age"] = 22
print("Modified dict:", student)

print("-" * 70)


# -------------------------------------------------------------
# SET (Mutable, unordered, unique values) - len() example included
# -------------------------------------------------------------
unique_numbers = {1, 2, 3, 3, 4}
print("SET:", unique_numbers)
print("Type:", type(unique_numbers))
print("Memory size:", unique_numbers.__sizeof__(), "bytes")

print("Length of set (len):", len(unique_numbers))  # <-- len() example
print("Iterating over set:")
for value in unique_numbers:
    print(value)

print("-" * 70)

# -------------------------------------------------------------
# WHY PYTHON IS A DYNAMIC PROGRAMMING LANGUAGE
# -------------------------------------------------------------
"""
Python is called a *dynamic programming language* because:

1. You do NOT need to declare data types.
   The interpreter automatically understands the data type
   based on the value assigned.

2. A variable can change its type at runtime.
   The type of a variable is determined during execution,
   not before running the program.

3. You can assign different types of values to the same variable
   without any error.
"""

print("\nWHY PYTHON IS A DYNAMIC LANGUAGE\n")

# Example 1: Python infers type automatically
x = "Hello"
print("x =", x, "| type:", type(x))

# Now x becomes an integer
x = 10
print("x =", x, "| type now:", type(x))

# Then x becomes a float
x = 3.14
print("x =", x, "| type now:", type(x))

# And x can again become a string
x = "Python is dynamic"
print("x =", x, "| type now:", type(x))


# Example 2: Starting with a string but reassigning to other types
data = "123"
print("\ndata =", data, "| type:", type(data))

data = int(data)  # converting to int
print("After converting to int:", data, "| type:", type(data))

data = str(data)  # converting back to string
print("After converting back to string:", data, "| type:", type(data))

data = [1, 2, 3]  # now assigning a list
print("After assigning list:", data, "| type:", type(data))

data = {"name": "Rahul"}  # now assigning dict
print("After assigning dict:", data, "| type:", type(data))

print("""
Conclusion:
- Python lets variables hold ANY type of data.
- The type can change at any moment.
- You never declare types like in Java or C++.
This flexibility is why Python is called a dynamic, strongly-typed language.
""")

# -------------------------------------------------------------
# DEFINING DATA TYPES AT THE TIME OF VARIABLE DEFINITION
# (Using Type Hints / Type Annotations)
# -------------------------------------------------------------
"""
Python allows you to *suggest* the type of a variable using type hints.

IMPORTANT:
- These are just SUGGESTIONS.
- Python does NOT enforce them.
- They help with readability and tools like IDEs, linters, mypy, etc.

Example:
    x: int = 10
    name: str = "Rahul"
    price: float = 99.99
"""

print("\nDEFINING DATA TYPES USING TYPE HINTS\n")

# examples explaining type hint syntax
age: int = 25
name: str = "Rahul"
height: float = 5.8
scores: list = [90, 85, 88]
coordinates: tuple = (10, 20)
student_info: dict = {"name": "Rahul", "age": 21}
unique_ids: set = {101, 102, 103}

print("age:", age, "| annotated type: int")
print("name:", name, "| annotated type: str")
print("height:", height, "| annotated type: float")
print("scores:", scores, "| annotated type: list")
print("coordinates:", coordinates, "| annotated type: tuple")
print("student_info:", student_info, "| annotated type: dict")
print("unique_ids:", unique_ids, "| annotated type: set")

# Show that Python still allows type change (dynamic behavior)
print("\nEven after annotation, Python still allows type changes (dynamic typing):")
age = "Now age is a string!"
print("age changed:", age, "| type now:", type(age))

print("""
Conclusion:
- Type hints improve clarity and help tools catch mistakes early.
- Python does NOT enforce the types — variables can still change type.
- This is part of why Python is a dynamic programming language.
""")

# -------------------------------------------------------------
# TYPE CONVERSION EXAMPLES (conversion functions)
# -------------------------------------------------------------
num_str = "123"
num_int = int(num_str)    # converts "123" -> 123
num_float = float(num_str)  # converts "123" -> 123.0
back_to_str = str(num_int)  # converts 123 -> "123"

print("Original string:", num_str)
print("Converted to int:", num_int, type(num_int))
print("Converted to float:", num_float, type(num_float))
print("Converted back to string:", back_to_str, type(back_to_str))

# len() on converted values
print("len(num_str):", len(num_str))       # string length
print("len(back_to_str):", len(back_to_str))  # also string length
# len() on num_int would error (we demonstrated earlier)

print("-" * 70)

# # -------------------------------------------------------------
# String Interpolation Example
# # -------------------------------------------------------------
user_balance = 1000.25
withdrawal_amount = 250
aBool = True

# Using f-string for interpolation
# Withdrawing 250 from your balance of 10000

output = "Withdrawing " + str(withdrawal_amount) + " from your balance of " + str(user_balance)
print(output)

output = f"Withdrawing {withdrawal_amount} from your balance of {user_balance} its an boolean value {aBool}"
print(output)
