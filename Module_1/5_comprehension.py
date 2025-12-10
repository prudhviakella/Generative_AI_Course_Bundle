"""
===============================================================
PYTHON COMPREHENSIONS — LIST & DICTIONARY
===============================================================

Comprehensions allow you to build new lists, sets, or dictionaries
in a clean, short, and powerful way.

They are faster, more readable, and more "Pythonic" than traditional loops.

Basic List Comprehension:
-------------------------
new_list = [expression for item in iterable]

Basic Dict Comprehension:
-------------------------
new_dict = {key_expression: value_expression for item in iterable}

How comprehension loops work internally:
----------------------------------------
List comprehension is simply a for loop written in one line.

Traditional loop:
-----------------
for x in [1,2,3]:
    do something with x

Equivalent comprehension:
-------------------------
[ do something with x  for x in [1,2,3] ]
"""

print("\nLIST & DICT COMPREHENSION\n")


# =============================================================
# 1. BASIC LIST COMPREHENSION
# =============================================================
numbers = [1, 2, 3, 4, 5]

# Traditional loop:
# Iteration 1 → n=1 → append 1*1 = 1
# Iteration 2 → n=2 → append 4
# Iteration 3 → n=3 → append 9
# Iteration 4 → n=4 → append 16
# Iteration 5 → n=5 → append 25
squares_loop = []
for n in numbers:
    squares_loop.append(n * n)

# List comprehension does the same in ONE line:
# squares_comp = [1,4,9,16,25]
squares_comp = [n * n for n in numbers]

print("Squares using loop:", squares_loop)
print("Squares using comprehension:", squares_comp)
print("-" * 70)


# =============================================================
# 2. LIST COMPREHENSION WITH FILTER CONDITION
# =============================================================
# Extract even numbers only
#
# Iteration:
# n=1 → skip
# n=2 → add
# n=3 → skip
# n=4 → add
# n=5 → skip
numbers = [1, 2, 3, 4, 5]

"""
iteration1:
        n = 1
        1 % 2 == 0 → False → skip
iteration2:
        n = 2
        2 % 2 == 0 → True → add 2 to list
iteration3:
        n = 3
        3 % 2 == 0 → False → skip
iteration4:
        n = 4
        4 % 2 == 0 → True → add 4 to list
iteration5:
        n = 5
        5 % 2 == 0 → False → skip
Final evens = [2,4]
"""
evens = [n for n in numbers if n % 2 == 0]
print(evens)


# =============================================================
# 3. LIST COMPREHENSION WITH IF-ELSE EXPRESSION
# =============================================================
# Classify numbers into "Even" or "Odd"
#
# n=1 → "Odd"
# n=2 → "Even"
# n=3 → "Odd"
# etc.
labels = ["Even" if n % 2 == 0 else "Odd" for n in numbers]

print("Labels (even/odd):", labels)
print("-" * 70)


# =============================================================
# 4. LIST COMPREHENSION WITH NESTED LOOPS
# =============================================================
# Creates all combinations (x,y)
#
# x=1 → y=1,(1,1) y=2,(1,2) y=3,(1,3)
# x=2 → y=1,(2,1) y=2,(2,2) y=3,(2,3)
pairs = [(x, y) for x in range(1, 3) for y in range(1, 4)]

print("Generated pairs:", pairs)
print("-" * 70)


# =============================================================
# 5. BASIC DICTIONARY COMPREHENSION
# =============================================================
numbers = [1, 2, 3, 4]

# Create dict of number:square
#
# Iteration:
# 1 → 1:1
# 2 → 2:4
# 3 → 3:9
# 4 → 4:16
squares_dict = {n: n*n for n in numbers}

print("Square dictionary:", squares_dict)
print("-" * 70)


# =============================================================
# 6. DICT COMPREHENSION WITH FILTER
# =============================================================
# Only include even numbers
#
# 1 → skip
# 2 → include
# 3 → skip
# 4 → include
even_square_dict = {n: n*n for n in numbers if n % 2 == 0}

print("Even squares dict:", even_square_dict)
print("-" * 70)


# =============================================================
# 7. REAL-WORLD EXAMPLE — LIST OF TUPLES → DICT
# =============================================================
students = [("Rahul", 85), ("Akhil", 92), ("John", 78)]

# Converts:
# ("Rahul",85) → Rahul:85
# ("Akhil",92) → Akhil:92
# ("John",78)  → John:78
student_dict = {name: score for (name, score) in students}

print("Student dictionary:", student_dict)
print("-" * 70)

# Alternative using dict() constructor
student_dict = dict(student_dict)


# =============================================================
# 8. REAL-WORLD EXAMPLE — CLEANING DICTIONARY DATA
# =============================================================
raw_data = {
    "Rahul": "85",
    "Akhil": "invalid",
    "John": "92",
    "Asha": "N/A"
}

# Only keep valid numeric values
#
# Iteration:
# ("Rahul", "85") → valid → include
# ("Akhil","invalid") → invalid → skip
# ("John", "92") → valid → include
# ("Asha", "N/A") → invalid → skip
clean_data = {
    name: int(score)
    for name, score in raw_data.items()
    if score.isdigit()
}

print("Cleaned score dictionary:", clean_data)
print("-" * 70)