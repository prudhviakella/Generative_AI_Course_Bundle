"""
======================================================================
PYTHON STRING, LIST & DICTIONARY METHODS — TEACHING MODULE
======================================================================

This file demonstrates commonly used string, list and dictionary
methods with clear, normalized variable names and detailed comments.

Structure:
- STRING METHODS (immutable) : case, find, replace, split/join, checks, length
- LIST METHODS   (mutable)   : add/remove/search/sort/copy/slicing
- DICTIONARY METHODS          : access, update, delete, copy, creation helpers
======================================================================
"""

# ---------------------------
# STRING METHODS (IMMUTABLE)
# ---------------------------
print("\n=== STRING METHODS ===\n")

# Example string for case conversion
name = "prudhvi akella"

# CASE CONVERSION
# ----------------
# .upper()    -> returns a new string with all uppercase characters
# .lower()    -> returns a new string with all lowercase characters
# .title()    -> returns a new string with each word capitalized
# .capitalize() -> capitalizes only the first character of the string
print("Original name:", name)
print("upper():", name.upper())          # 'PRUDHVI AKELLA'
print("lower():", name.lower())          # 'prudhvi akella'
print("title():", name.title())          # 'Prudhvi Akella'
print("capitalize():", name.capitalize())# 'Prudhvi akella'
print("-" * 70)

# FINDING SUBSTRINGS
# -------------------
text = "I love Python programming. Python is powerful."

# .find(sub) -> returns index of first occurrence or -1 if not found
# .rfind(sub)-> returns index of last occurrence or -1
# .count(sub)-> number of non-overlapping occurrences
# .startswith(prefix), .endswith(suffix) -> boolean checks
first_index = text.find("Python")    # first occurrence index
last_index = text.rfind("Python")    # last occurrence index
count_python = text.count("Python")  # how many times 'Python' appears
starts_with_I = text.startswith("I") # True/False
ends_with_powerful = text.endswith("powerful.") # True/False

print("text:", text)
print("find('Python') ->", first_index)
print("rfind('Python') ->", last_index)
print("count('Python') ->", count_python)
print("startswith('I') ->", starts_with_I)
print("endswith('powerful.') ->", ends_with_powerful)
print("-" * 70)

# REPLACE AND STRIP
# ------------------
line = "   hello world   "
# .strip()  -> remove whitespace from both ends
# .lstrip() -> remove whitespace from left
# .rstrip() -> remove whitespace from right
print("Original line (visible spaces):", repr(line))
print("strip() ->", repr(line.strip()))
print("lstrip() ->", repr(line.lstrip()))
print("rstrip() ->", repr(line.rstrip()))

# .replace(old, new) -> returns a new string with replacements
sentence = "I like Java"
print("Before replace:", sentence)
print("After replace:", sentence.replace("Java", "Python"))
print("-" * 70)

# SPLIT AND JOIN
# ---------------
data = "apple,banana,mango"
# .split(sep) -> splits string into a list of substrings (sep removed)
# .join(iterable) -> joins list of strings into a single string with given separator
fruits = data.split(",")  # ['apple', 'banana', 'mango']
print("Split string into list:", fruits)

joined = "-".join(fruits)  # 'apple-banana-mango'
print("Join list into string with '-':", joined)
print("-" * 70)

# CHECK METHODS (character classes)
# ----------------------------------
s1 = "12345"
s2 = "Python3"
s3 = "python"
s4 = "   "

# .isdigit() -> all characters are digits (and at least one character)
# .isalpha() -> all alphabetic letters (no digits/space)
# .isalnum() -> alphanumeric (letters and/or digits)
# .isspace() -> all whitespace characters
print("isdigit('12345') ->", s1.isdigit())
print("isalpha('python') ->", s3.isalpha())
print("isalnum('Python3') ->", s2.isalnum())
print("isspace('   ') ->", s4.isspace())
print("-" * 70)

# LENGTH & MEMBERSHIP
# --------------------
word = "programming"
# len() -> number of characters
# 'sub' in word -> membership test
print("word:", word)
print("len(word) ->", len(word))
print("'pro' in word ->", "pro" in word)
print("-" * 70)


# ---------------------------
# LIST METHODS (MUTABLE)
# ---------------------------
print("\n=== LIST METHODS ===\n")

# ADDING ITEMS
# -------------
numbers = [1, 2, 3]            # initial list

# Add elements towards to the end of the list
# .append(x) -> add single element to end
numbers.append(4)              # [1,2,3,4]
print("After append(4):", numbers)

# Add elements at the head part of the list
numbers = [0] + [1,2,4]
print("After insert(0, 1):", numbers)

# .extend(iterable) -> extend list with elements from iterable
numbers.extend([5, 6, 7])     # [1,2,3,4,5,6,7]
print("After extend([5,6,7]):", numbers)

# .insert(index, x) -> insert element at position index
numbers.insert(0, 0)          # [0,1,2,3,4,5,6,7]
print("After insert(0,0):", numbers)
print("-" * 70)

# REMOVING ITEMS
# ---------------
# .remove(x) -> remove first occurrence of x (raises ValueError if not present)
# .pop() -> remove and return last item; .pop(i) -> remove and return item at index i
numbers.remove(3)             # removes first 3
print("After remove(3):", numbers)

value = numbers.pop()         # removes last element
print("pop() returned:", value)
value0 = numbers.pop(0)       # remove at index 0
print("pop(0) removed first:", value0)
numbers.clear()               # remove all elements -> []
print("After clear():", numbers)
print("-" * 70)

# SEARCHING & COUNTING
# ---------------------
fruits_list = ["apple", "banana", "apple", "mango"]

# .index(x) -> index of first occurrence of x (ValueError if not found)
# .count(x) -> number of occurrences
print("fruits_list:", fruits_list)
print("index('banana') ->", fruits_list.index("banana"))
print("count('apple') ->", fruits_list.count("apple"))
print("-" * 70)

# SORTING & REVERSING
# --------------------
nums = [5, 1, 4, 2, 3]
nums.sort()                    # sorts in place ascending
print("After sort():", nums)
nums.sort(reverse=True)        # sorts in place descending
print("After sort(reverse=True):", nums)
nums.reverse()                 # reverses the list order in place
print("After reverse():", nums)
print("-" * 70)

# # COPYING
# # --------
# original_list = [1, 2, 3]
# shallow_copy = original_list.copy()  # shallow copy of list
# shallow_copy.append(4)
# # original remains unchanged because .copy() created a separate list object
# print("original_list:", original_list)
# print("shallow_copy:", shallow_copy)
# print("-" * 70)

# LENGTH, MEMBERSHIP, SLICING
# ----------------------------
arr = [10, 20, 30, 40, 50]
print("len(arr) ->", len(arr))
print("30 in arr ->", 30 in arr)

arr = [10, 20, 30, 40, 50]
first_part_new_list = arr[0:3]
print(first_part_new_list)
first_part_new_list = arr[:3]
print(first_part_new_list)


second_part_new_list = arr[3:len(arr)]
print(second_part_new_list)
second_part_new_list = arr[3:]
print(second_part_new_list)
print("-" * 70)


# ---------------------------
# DICTIONARY METHODS
# ---------------------------
print("\n=== DICTIONARY METHODS ===\n")

"""
Dictionary quick notes:
- dict stores key -> value pairs
- keys are unique (if you assign the same key twice, last value wins)
- use dict.get(key, default) for safe access without KeyError
"""

student = {"name": "Rahul", "age": 22, "course": "Python"}

# ACCESS METHODS
# ---------------
# .get(key[, default]) -> safe access (returns default if key missing)
print("student.get('name') ->", student.get("name"))
print("student.get('address') ->", student.get("address"))         # None
print("student.get('address','N/A') ->", student.get("address", "N/A"))
print("-" * 70)

# keys(), values(), items() -> provide views of the dict's contents
print("student.keys()  ->", list(student.keys()))
print("student.values()->", list(student.values()))
print("student.items() ->", list(student.items()))
print("-" * 70)

# ADD / UPDATE
# -------------
employee = {"name": "Akhil", "salary": 50000}
# .update(mapping) -> update existing keys or add new keys
employee.update({"salary": 60000})   # modifies existing salary
employee.update({"dept": "IT"})      # inserts new key 'dept'
print("After update:", employee)
print("-" * 70)

# setdefault(key, default) -> returns existing value or sets default and returns it
profile = {"username": "prudhvi"}
returned_email = profile.setdefault("email", "unknown@example.com")
print("setdefault returned:", returned_email)
print("profile after setdefault:", profile)
# If key already exists, setdefault returns existing value and does not overwrite
print("setdefault existing key:", profile.setdefault("username", "newuser"))
print("profile remains:", profile)
print("-" * 70)

# DELETE METHODS
# ---------------
data = {"a": 1, "b": 2, "c": 3}
# pop(key) -> remove key and return its value; raises KeyError if missing unless default provided
popped_value = data.pop("b")
print("popped 'b':", popped_value)
print("after pop:", data)
# pop with default avoids KeyError on missing key
print("pop missing key with default:", data.pop("x", "Not Found"))
print("-" * 70)

# popitem() removes and returns the last inserted key-value pair (Python 3.7+ insertion-ordered)
pairs = {"x": 10, "y": 20, "z": 30}
print("popitem() returned:", pairs.popitem())
print("pairs after popitem():", pairs)
# clear() removes all items
pairs.clear()
print("pairs after clear():", pairs)
print("-" * 70)

# # COPY METHODS
# # -------------
# user = {"name": "Rahul", "role": "Admin"}
# user_copy = user.copy()   # shallow copy
# user_copy["role"] = "Developer"
# print("original user:", user)
# print("user copy:", user_copy)
# # dict() constructor also makes a shallow copy
# copy2 = dict(user)
# print("copy2 (via dict()):", copy2)
# print("-" * 70)

# CREATION HELPER: fromkeys()
# ---------------------------
keys = ["id", "name", "age"]
default_dict = dict.fromkeys(keys, None)  # {'id': None, 'name': None, 'age': None}
print("fromkeys result:", default_dict)
print("-" * 70)

# REAL-WORLD DICTIONARY EXAMPLES
# ------------------------------

# 1) Frequency count of characters in a string
text = "banana"
freq = {}
# Iteration breakdown:
# char = 'b' -> freq['b'] = 1
# char = 'a' -> freq['a'] = 1
# char = 'n' -> freq['n'] = 1
# char = 'a' -> freq['a'] = 2
# ...
for char in text:
    freq[char] = freq.get(char, 0) + 1
print("Frequency count for 'banana':", freq)
print("-" * 70)

# 2) Shopping cart total (simple lookup + sum)
cart = {"apple": 3, "banana": 2, "milk": 1}   # item -> quantity
prices = {"apple": 10, "banana": 5, "milk": 40} # item -> unit price
# sum(cart[item] * prices[item] for item in cart) -> multiply quantity by price and sum
total_amount = sum(cart[item] * prices[item] for item in cart)
print("Shopping cart total amount:", total_amount)
print("-" * 70)

# 3) Student grade lookup with safe get
grades = {"Rahul": "A", "Akhil": "B", "John": "C"}
lookup_name = "Rahul"
print(f"{lookup_name}'s grade:", grades.get(lookup_name, "Not found"))
print("-" * 70)

print("\nEnd of module.")