"""
===============================================================
PYTHON CONDITIONS — IF, ELIF, ELSE, MATCH-CASE, CONDITIONAL EXPRESSION
===============================================================

Conditions allow your program to make decisions.

Basic structure:
----------------

if condition:
    block of code
elif another_condition:
    block of code
else:
    block of code

Python checks conditions top to bottom.
"""

# 10 > 20
# 10 < 20
# 10 == 10
# 10 != 5
# 10 >= 5
# 10 <= 10


print("\nPYTHON CONDITIONALS\n")

# -------------------------------------------------------------
# BASIC IF EXAMPLE
# -------------------------------------------------------------
# If the condition (temperature > 30) is True, the code inside the block runs.
# Otherwise nothing happens because this example has no 'else' block.
temperature = 35

if temperature > 30:
    print("It's a hot day!")
print("-" * 70)


# -------------------------------------------------------------
# IF-ELSE
# -------------------------------------------------------------
# Classic two-way decision.
# If condition is True → run the IF block
# Otherwise → run the ELSE block.
age = 16

if age >= 18:
    print("You are eligible to vote.")
else:
    print("You are NOT eligible to vote.")
print("-" * 70)


# -------------------------------------------------------------
# IF-ELIF-ELSE
# -------------------------------------------------------------
# 'elif' allows checking multiple conditions in sequence.
# Python checks conditions from top to bottom.
# The FIRST True condition executes, others are ignored.
score = 82

if score >= 90:
    print("Grade: A")
elif score >= 80:
    print("Grade: B")
elif score >= 70:
    print("Grade: C")
else:
    print("Grade: D")
print("-" * 70)


# -------------------------------------------------------------
# Real-world example: ATM withdrawal
# -------------------------------------------------------------
# This example checks for:
# 1) Invalid withdrawal amount
# 2) Insufficient balance
# 3) Valid withdrawal
balance = 5000
withdraw_amount = 1500

if withdraw_amount <= 0:
    print("Invalid amount.")
elif withdraw_amount > balance:
    print("Insufficient balance!")
else:
    # Only executed if previous conditions are False
    balance -= withdraw_amount
    print(f"Withdrawal successful! Remaining balance: {balance}")
print("-" * 70)


# -------------------------------------------------------------
# NESTED CONDITIONS
# -------------------------------------------------------------
# IF inside another IF.
# Useful when one condition depends on a previous condition.
user = "admin"
password = "1234"

if user == "admin":
    # Only checked if user matches
    if password == "1234":
        print("Login successful!")
    else:
        print("Incorrect password.")
else:
    print("User not found.")
print("-" * 70)


# -------------------------------------------------------------
# MATCH-CASE (Python 3.10+)
# -------------------------------------------------------------
# Similar to switch-case in other languages.
# Used for checking specific fixed values.
status = 404

match status:
    case 200:
        print("OK")                 # success response
    case 404:
        print("Page Not Found")     # common error
    case 500:
        print("Server Error")       # internal error
    case _:
        print("Unknown status code")  # default fallback
print("-" * 70)

# -------------------------------------------------------------
# MATCH-CASE EQUIVALENT USING IF-ELIF-ELSE
# -------------------------------------------------------------

if status == 200:
    print("OK")                 # success response
elif status == 404:
    print("Page Not Found")     # common error
elif status == 500:
    print("Server Error")       # internal error
else:
    print("Unknown status code")  # default fallback


# -------------------------------------------------------------
# Real-world example: payment processing
# -------------------------------------------------------------
# match-case is extremely clean when checking fixed options.
payment_method = "upi"

match payment_method:
    case "credit_card":
        print("Processing credit card payment...")
    case "debit_card":
        print("Processing debit card payment...")
    case "upi":
        print("Processing UPI payment...")
    case _:
        print("Invalid payment method.")
print("-" * 70)


# -------------------------------------------------------------
# CONDITIONAL EXPRESSION (one-line if else)
# -------------------------------------------------------------
# Syntax:
#   value_if_true  if condition  else  value_if_false
#
# Useful when you need to choose between two values.
age = 20

message = "Adult" if age >= 18 else "Minor"
print("User is:", message)
print("-" * 70)


# -------------------------------------------------------------
# CONDITIONAL EXPRESSION WITH MULTIPLE CONDITIONS
# -------------------------------------------------------------
# Chaining conditional expressions for multiple categories.
# Evaluated left to right until one condition matches.
age = 45

category = (
    "Child" if age < 13
    else "Teen" if age < 18
    else "Young Adult" if age < 30
    else "Adult" if age < 60
    else "Senior"
)

print("Age category:", category)
print("-" * 70)


# -------------------------------------------------------------
# Real-world conditional expression
# -------------------------------------------------------------
# Discount is 10% if amount > 1000, otherwise 5%.
amount = 1200

discount = 0.10 if amount > 1000 else 0.05
final = amount - (amount * discount)

print("Amount:", amount)
print("Discount applied:", discount * 100, "%")
print("Final Price:", final)
print("-" * 70)


# -------------------------------------------------------------
# COMPLEX CONDITION USING AND / OR
# -------------------------------------------------------------
# The idea:
#
# - Adults (>=18) must have ID → allowed
# - Minors (<18) must BOTH:
#         → come with parent
#         → AND be a club member
#
# Parentheses improve readability and make the logic explicit.
age = 16
has_id = True
is_with_parent = True
is_member = False

if (age >= 18 and has_id) or (age < 18 and is_with_parent and is_member):
    print("Ticket booking allowed.")
else:
    print("Ticket booking denied.")

print("-" * 70)

# -------------------------------------------------------------
# FUNCTION USING IF-ELIF-ELSE
# -------------------------------------------------------------
# Function that compares a number to 20 and returns a message.
def an(a):
    if a > 20:
        return "Greater than 20"
    elif a == 20:
        return "Equal to 20"
    else:
        return "Less than 20"

print(an(19))