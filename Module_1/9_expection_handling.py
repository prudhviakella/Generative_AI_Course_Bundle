"""
===============================================================
PYTHON EXCEPTION HANDLING — COMPLETE BEGINNER MODULE
===============================================================

Exception handling is used to deal with RUNTIME ERRORS gracefully.

Basic Structure:
----------------
try:
    # code that might cause an error
except SomeError:
    # what to do if error happens
else:
    # runs only if NO error
finally:
    # runs ALWAYS (cleanup)

Exceptions prevent the program from crashing.
===============================================================
"""
import traceback

print("\nEXCEPTION HANDLING BASICS\n")

# -------------------------------------------------------------
# 1. BASIC try-except
# -------------------------------------------------------------
try:
    x = 10 / 0    # This line will cause ZeroDivisionError
except ZeroDivisionError:
    print("Error: Cannot divide by zero!")
print("-" * 70)


# -------------------------------------------------------------
# 2. MULTIPLE EXCEPT BLOCKS
# -------------------------------------------------------------
try:
    value = int("abc")  # ValueError
except ValueError:
    print("Error: Conversion to integer failed!")
    exc_str = traceback.format_exc()
    print(exc_str)
except TypeError:
    print("Error: Wrong type used!")
print("-" * 70)


# -------------------------------------------------------------
# 3. EXCEPT CATCHING MULTIPLE ERRORS TOGETHER
# -------------------------------------------------------------
try:
    result = 10 / int("0")  # ZeroDivisionError + ValueError possibility
except (ZeroDivisionError, ValueError) as e:
    print("Caught error:", e)
print("-" * 70)


# -------------------------------------------------------------
# 4. ELSE BLOCK — runs only when NO EXCEPTION occurs
# -------------------------------------------------------------
try:
    n = int("25")  # Valid → no error
except ValueError:
    print("Invalid number")
else:
    print("Successfully converted:", n)
print("-" * 70)


# -------------------------------------------------------------
# 5. FINALLY BLOCK — runs ALWAYS
# -------------------------------------------------------------
try:
    file = open("temp.txt", "w")
    file.write("Hello!")
except Exception as e:
    print("Error writing file:", e)
finally:
    file.close()
    print("File closed successfully (finally block executed)")
print("-" * 70)


# -------------------------------------------------------------
# 6. RAISING EXCEPTIONS MANUALLY
# -------------------------------------------------------------
def withdraw(balance, amount):
    if amount > balance:
        raise ValueError("Insufficient balance!")
    return balance - amount

try:
    print(withdraw(1000, 2000))
except ValueError as e:
    print("Bank Error:", e)
print("-" * 70)


# -------------------------------------------------------------
# 7. REAL-WORLD EXAMPLE — LOGIN SYSTEM
# -------------------------------------------------------------
def login(username, password):
    if username != "admin":
        raise ValueError("Invalid username")
    if password != "1234":
        raise ValueError("Incorrect password")
    return "Login successful!"

try:
    print(login("admin", "0000"))
except ValueError as e:
    print("Login failed:", e)
print("-" * 70)


# -------------------------------------------------------------
# 8. REAL-WORLD EXAMPLE — FILE READING
# -------------------------------------------------------------
try:
    with open("data.txt", "r") as f:
        content = f.read()
        print(content)
except FileNotFoundError:
    print("Error: File not found.")
print("-" * 70)


# -------------------------------------------------------------
# 9. CREATING A CUSTOM EXCEPTION CLASS
# -------------------------------------------------------------
class AgeError(Exception):
    """Custom exception used when age is invalid."""
    pass

def register_user(name, age):
    if age < 18:
        raise AgeError("User must be 18 or older")
    print(f"User '{name}' registered successfully!")

try:
    register_user("Rahul", 16)
except AgeError as e:
    print("Custom Exception:", e)
print("-" * 70)


# -------------------------------------------------------------
# 10. COMBINED EXAMPLE — ATM SYSTEM
# -------------------------------------------------------------
def atm_withdraw(balance, amount):
    try:
        if amount <= 0:
            raise ValueError("Amount must be positive")

        if amount > balance:
            raise ValueError("Insufficient funds")

        new_balance = balance - amount
        return new_balance

    except ValueError as e:
        print("ATM Error:", e)
        return balance   # return balance unchanged

    finally:
        print("Transaction completed (success or fail)")

current_balance = 5000
print("Before:", current_balance)
current_balance = atm_withdraw(current_balance, 7000)
print("After:", current_balance)
print("-" * 70)

"""
===============================================================
CUSTOM EXCEPTIONS IN PYTHON
===============================================================
Why create custom exceptions?

When the built-in exceptions (ValueError, TypeError, etc.)
are not specific enough for your application, you define
your own exception classes.

A custom exception:
    ✔ makes error messages clearer
    ✔ represents domain-specific problems
    ✔ improves debugging
    ✔ follows real-world logic

Example use cases:
    - InvalidAgeError
    - InsufficientFundsError
    - LoginFailedError
    - InvalidProductError
===============================================================
"""

print("\nCUSTOM EXCEPTION HANDLING\n")


# -------------------------------------------------------------
# 1. DEFINING A CUSTOM EXCEPTION
# -------------------------------------------------------------
class InvalidAgeError(Exception):
    """
    Custom exception raised when the user's age is invalid.

    We extend the base `Exception` class.
    This keeps all standard exception features.
    """
    pass


def register_user(name, age):
    """
    Function that validates user age.
    If age is below 18 → raise custom exception.
    """
    if age < 18:
        raise InvalidAgeError(f"User '{name}' must be at least 18 years old.")
    print(f"User '{name}' registered successfully!")


# Testing the custom exception
try:
    register_user("Rahul", 16)
except InvalidAgeError as e:
    print("Registration Error:", e)

print("-" * 70)


# -------------------------------------------------------------
# 2. BANKING EXAMPLE — MULTIPLE CUSTOM EXCEPTIONS
# -------------------------------------------------------------
class InsufficientFundsError(Exception):
    """Raised when withdraw amount exceeds available balance."""
    pass


class NegativeAmountError(Exception):
    """Raised when withdraw or deposit amount is invalid."""
    pass


def withdraw(balance, amount):
    """
    Withdraw money from account with validation.
    Raises custom exceptions instead of generic ValueError.
    """
    if amount <= 0:
        raise NegativeAmountError("Amount must be greater than zero.")
    if amount > balance:
        raise InsufficientFundsError("Not enough balance to withdraw.")
    return balance - amount


# Testing multiple custom exceptions
balance = 5000

try:
    balance = withdraw(balance, 6000)
except InsufficientFundsError as e:
    print("Bank Error:", e)
except NegativeAmountError as e:
    print("Amount Error:", e)

print("Remaining Balance:", balance)
print("-" * 70)


# -------------------------------------------------------------
# 3. REAL WORLD: PRODUCT VALIDATION EXAMPLE
# -------------------------------------------------------------
class InvalidProductError(Exception):
    """Raised when product name or price is invalid."""
    pass


def add_product(name, price):
    if not name.strip():
        raise InvalidProductError("Product name cannot be empty.")
    if price <= 0:
        raise InvalidProductError("Product price must be positive.")
    print(f"Product '{name}' added successfully.")


try:
    add_product("Laptop", -50000)
except InvalidProductError as e:
    print("Product Error:", e)

print("-" * 70)