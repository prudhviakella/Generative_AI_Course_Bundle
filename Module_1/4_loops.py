"""
===============================================================
PYTHON FOR LOOP — INTRODUCTION FOR BEGINNERS
===============================================================

A 'for loop' is used to repeat a block of code for each item in a sequence.

You can loop over:
- lists
- strings
- tuples
- sets
- dictionaries
- ranges (numbers)

What happens in a for-loop?
---------------------------
The loop picks ONE item at a time from the sequence.

Iteration 1 → takes the 1st value
Iteration 2 → takes the 2nd value
Iteration 3 → takes the 3rd value
... until sequence ends
"""

print("\nFOR LOOP BASICS\n")

# -------------------------------------------------------------
# LOOPING OVER A LIST
# -------------------------------------------------------------
fruits = ["apple", "banana", "mango"]

# Iteration explanation:
# Iteration 1 → fruit = "apple"
# Iteration 2 → fruit = "banana"
# Iteration 3 → fruit = "mango"
for fruit in fruits:
    print("Fruit:", fruit)

print("-" * 70)


# -------------------------------------------------------------
# LOOPING OVER A STRING (char-by-char)
# -------------------------------------------------------------
text = "Python"

# Iteration explanation:
# Iteration 1 → char = 'P'
# Iteration 2 → char = 'y'
# Iteration 3 → char = 't'
# Iteration 4 → char = 'h'
# Iteration 5 → char = 'o'
# Iteration 6 → char = 'n'
for char in text:
    print("Character:", char)

print("-" * 70)


# -------------------------------------------------------------
# RANGE LOOP
# -------------------------------------------------------------
# range(1, 6) generates: 1, 2, 3, 4, 5
# Iteration 1 → i = 1
# Iteration 2 → i = 2
# Iteration 3 → i = 3
# Iteration 4 → i = 4
# Iteration 5 → i = 5
for i in range(1, 6):
    print("Number:", i)

print("-" * 70)


# -------------------------------------------------------------
# RANGE WITH STEP
# -------------------------------------------------------------
# range(0, 20, 5) generates: 0, 5, 10, 15
# Iteration 1 → i = 0
# Iteration 2 → i = 5
# Iteration 3 → i = 10
# Iteration 4 → i = 15
for i in range(0, 20, 5):
    print("Step value:", i)

print("-" * 70)


# -------------------------------------------------------------
# LOOP USING ENUMERATE (index + value)
# -------------------------------------------------------------
cities = ["Delhi", "Mumbai", "Chennai"]

# enumerate gives:
# Iteration 1 → index=0, city="Delhi"
# Iteration 2 → index=1, city="Mumbai"
# Iteration 3 → index=2, city="Chennai"
for index, city in enumerate(cities):
    print(f"{index}: {city}")

print("-" * 70)


# -------------------------------------------------------------
# LOOPING OVER A DICTIONARY
# -------------------------------------------------------------
student = {"name": "Rahul", "age": 22, "course": "Python"}

# student.items():
# Iteration 1 → key="name",  value="Rahul"
# Iteration 2 → key="age",   value=22
# Iteration 3 → key="course",value="Python"
for key, value in student.items():
    print(key, "=>", value)

print("-" * 70)


# -------------------------------------------------------------
# LOOP WITH CONDITIONS
# -------------------------------------------------------------
numbers = [5, 12, 7, 20, 3, 18]

# For each number:
# If number > 10, print message
for n in numbers:
    # Iteration happens like:
    # Iter 1 → n=5   (5 > 10? No)
    # Iter 2 → n=12  (12 > 10? Yes → print)
    # Iter 3 → n=7   (No)
    # Iter 4 → n=20  (Yes)
    # Iter 5 → n=3   (No)
    # Iter 6 → n=18  (Yes)
    if n > 10:
        print(n, "is greater than 10")

print("-" * 70)


# -------------------------------------------------------------
# NESTED LOOP EXAMPLE
# -------------------------------------------------------------
# Outer loop → rows (1 to 3)
# Inner loop → columns (1 to 3)
#
# Iteration breakdown:
# Outer Iter 1 → row = 1
#       Inner Iter → col = 1 → (1, 1)
#       Inner Iter → col = 2 → (1, 2)
#       Inner Iter → col = 3 → (1, 3)
#
# Outer Iter 2 → row = 2
#       Inner loop prints (2,1), (2,2), (2,3)
#
# Outer Iter 3 → row = 3
#       Inner loop prints (3,1), (3,2), (3,3)
for row in range(1, 4):
    for col in range(1, 4):
        print(f"({row}, {col})")

print("-" * 70)


# -------------------------------------------------------------
# MULTIPLICATION TABLE
# -------------------------------------------------------------
num = 5

# Iteration:
# i = 1 → 5 x 1 = 5
# i = 2 → 5 x 2 = 10
# ...
# i = 10 → 5 x 10 = 50
for i in range(1, 11):
    print(f"{num} x {i} = {num * i}")

print("-" * 70)


# -------------------------------------------------------------
# BREAK AND CONTINUE
# -------------------------------------------------------------
numbers = [1, 2, 3, 4, 5, 6]

print("Using continue (skip even numbers):")
# Iteration:
# n=1 → odd → print
# n=2 → even → continue → skip printing
# n=3 → odd → print
# n=4 → even → skip
# ...
for n in numbers:
    if n % 2 == 0:
        continue
    print(n)

print("\nUsing break (stop at 4):")
# Iteration:
# n=1 → print
# n=2 → print
# n=3 → print
# n=4 → break → loop stops immediately
for n in numbers:
    if n == 4:
        break
    print(n)

print("-" * 70)


# -------------------------------------------------------------
# SEARCHING FOR AN ITEM IN A LIST
# -------------------------------------------------------------
products = ["laptop", "mouse", "keyboard", "charger"]
target = "keyboard"

found = False

# Iteration:
# p="laptop"  → not match
# p="mouse"   → not match
# p="keyboard"→ match → break
for p in products:
    if p == target:
        print("Product found:", p)
        found = True
        break

if not found:
    print("Product not found")

print("-" * 70)