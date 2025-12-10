"""
======================================================================
PYTHON FUNCTIONAL PROGRAMMING BASICS — map(), filter(), reduce(),
AND COSINE SIMILARITY
======================================================================

This module introduces some powerful functional programming tools
available in Python:

1. map(function, iterable)
   - Applies a function to every item in a list.
   - Useful for transforming or cleaning data.
   - Common in data preprocessing, ETL scripts, and ML pipelines.

2. filter(function, iterable)
   - Keeps only items that satisfy a condition.
   - Used for extracting valid items from datasets (e.g., filter valid emails,
     filter even numbers, remove invalid entries).

3. reduce(function, iterable)
   - Combines all items in a list into a single value.
   - Often used for aggregation tasks like computing sums, products,
     maximums, minimums, longest string, etc.

These three functions help you write cleaner, shorter, and more efficient code,
especially when combined with lambda functions.

----------------------------------------------------------------------
COSINE SIMILARITY
----------------------------------------------------------------------
Cosine similarity is a metric used in:
- Machine Learning
- NLP (Natural Language Processing)
- Search engines
- Recommendation systems

It measures how similar two vectors are by comparing the angle between them.

In real-world applications:
- Used to compare text documents
- Used to find similar customers/products/users
- Used in clustering algorithms and vector embeddings

This module includes:
- Basic map, filter, reduce examples
- Real-world examples (prices, emails, longest word)
- A full cosine similarity implementation without external libraries
- A real-world cosine similarity example for text comparison

The goal is to help beginners understand how functional-style programming
and similarity metrics work together in modern Python applications.
======================================================================
"""

print("\nFUNCTIONAL PROGRAMMING BASICS: map(), filter(), reduce(), COSINE SIMILARITY\n")
# -------------------------------------------------------------
# MAP — Apply a function to every item in a list
# -------------------------------------------------------------

# Basic example: square each number
numbers = [1, 2, 3, 4]
squares = list(map(lambda x: x*x, numbers))
print("Squares:", squares)


# REAL-WORLD EXAMPLE: Convert list of prices from string to float
price_strings = ["10.5", "20.0", "7.99", "100.25"]
prices = list(map(lambda p: float(p), price_strings))

print("Converted Prices:", prices)
print("-" * 70)

# Another example: Sum pairs of numbers in a list of tuples
aList = [(1, 2), (3, 4), (5, 6)]

"""
iteration 1:
    x = (1, 2)
    x[0] + x[1] → 1 + 2 = 3
    return 3
iteration 2:
    x = (3, 4)
    x[0] + x[1] → 3 + 4 = 7
    return 7
iteration 3:
    x = (5, 6)
    x[0] + x[1] → 5 + 6 = 11
    return 11
Final result: [3, 7, 11]
"""

output = list(map(lambda x: x[0] + x[1], aList))  # Returns an iterator

# -------------------------------------------------------------
# FILTER — Keep only items that satisfy a condition
# -------------------------------------------------------------

numbers = [1, 2, 3, 4, 5, 6]
evens = list(filter(lambda x: x % 2 == 0, numbers))
print("Evens:", evens)

# REAL-WORLD EXAMPLE: Filter valid email IDs
emails = ["rahul@gmail.com", "invalid-email", "akhil@yahoo.com", "no-at-sign"]
valid_emails = list(filter(lambda e: "@" in e and "." in e, emails))

print("Valid Emails:", valid_emails)
print("-" * 70)


# -------------------------------------------------------------
# REDUCE — Reduce a list into a single value
# -------------------------------------------------------------
from functools import reduce

numbers = [1, 2, 3, 4]

total = reduce(lambda a, b: a + b, numbers)
print("Sum using reduce:", total)

# REAL-WORLD EXAMPLE: Multiply all numbers (product)
product = reduce(lambda a, b: a * b, numbers)
print("Product using reduce:", product)

# REAL-WORLD EXAMPLE: Find LONGEST word in a list
"""
iteration 1:
    a = "python"
    b = "data"
    len(a) > len(b) → "python"
    return "python"
iteration 2:
    a = "python"
    b = "visualization"
    len(a) > len(b) → "visualization"
    return "visualization"
iteration 3:
    a = "visualization"
    b = "ai"
    len(a) > len(b) → "visualization"
    return "visualization"
Final result: "visualization"
"""

# REAL-WORLD EXAMPLE: Find LONGEST word in a list
words = ["python", "data", "visualization", "ai"]
longest = reduce(lambda a, b: a if len(a) > len(b) else b, words)

print("Longest word:", longest)
print("-" * 70)

# Without using reduce()
longest = ""
for word in enumerate(words):
    a = word[0]
    b = word[1]
    if longest is not None:
        a = longest
    if len(a) > len(b):
        longest = a
    else:
        longest = b

print(longest)

"""
======================================================================
COSINE SIMILARITY — FORMULA + STEP-BY-STEP PYTHON IMPLEMENTATION
======================================================================

Cosine similarity measures how similar two vectors are by calculating
the cosine of the angle between them.

FORMULA:
--------
            A · B
cos(θ) = --------------------
          ||A|| * ||B||

Where:
- A · B = dot product of vectors A and B
- ||A|| = magnitude (length) of vector A
- ||B|| = magnitude (length) of vector B

Step-by-step:
-------------
1. Compute dot product:
       A · B = a1*b1 + a2*b2 + a3*b3 + ...  
2. Compute magnitude of A:
       ||A|| = sqrt(a1² + a2² + a3² + ...)
3. Compute magnitude of B:
       ||B|| = sqrt(b1² + b2² + b3² + ...)
4. Divide dot product by magnitudes.

Cosine similarity value:
- 1 → vectors are exactly similar (same direction)
- 0 → vectors are unrelated (90-degree angle)
- -1 → vectors are opposite (completely opposite direction)
"""

import math


def cosine_similarity(vec1, vec2):
    # ---------------------------------------------------------
    # DOT PRODUCT
    # ---------------------------------------------------------
    # zip(vec1, vec2) pairs elements:
    # vec1=[1,2,3], vec2=[4,5,6]
    # zip gives → (1,4), (2,5), (3,6)
    #
    # sum(a*b for a,b in zip()) does:
    # 1*4 + 2*5 + 3*6
    # = 4 + 10 + 18
    # = 32
    dot = sum(a * b for a, b in zip(vec1, vec2))

    # ---------------------------------------------------------
    # MAGNITUDE OF VECTOR 1
    # ---------------------------------------------------------
    # sum(a*a for a in vec1) does:
    # 1² + 2² + 3²
    # = 1 + 4 + 9
    # = 14
    #
    # magnitude = sqrt(14)
    mag1 = math.sqrt(sum(a * a for a in vec1))

    # ---------------------------------------------------------
    # MAGNITUDE OF VECTOR 2
    # ---------------------------------------------------------
    # sum(b*b for b in vec2) does:
    # 4² + 5² + 6²
    # = 16 + 25 + 36
    # = 77
    #
    # magnitude = sqrt(77)
    mag2 = math.sqrt(sum(b * b for b in vec2))

    # ---------------------------------------------------------
    # ZERO DIVISION PROTECTION
    # ---------------------------------------------------------
    # If either vector is [0,0,0], its magnitude = 0.
    # Cosine similarity cannot divide by zero.
    if mag1 == 0 or mag2 == 0:
        return 0

    # ---------------------------------------------------------
    # FINAL COSINE SIMILARITY
    # ---------------------------------------------------------
    # dot / (mag1 * mag2)
    # = 32 / (sqrt(14) * sqrt(77))
    # ≈ 0.9746
    return dot / (mag1 * mag2)


# Example vectors
v1 = [1, 2, 3]
v2 = [4, 5, 6]

print("Cosine Similarity:", cosine_similarity(v1, v2))

# -------------------------------------------------------------
# REAL-WORLD COSINE SIMILARITY EXAMPLE
# -------------------------------------------------------------
# Compare text similarity using simple word counts (bag-of-words)
sentence1 = "I love Python programming"
sentence2 = "Python programming is something I love"

# Common vocabulary
vocab = list(set(sentence1.split()) | set(sentence2.split()))

# Convert each sentence to vector (word counts)
vec_s1 = [sentence1.split().count(word) for word in vocab]
vec_s2 = [sentence2.split().count(word) for word in vocab]

print("Sentence Similarity:", cosine_similarity(vec_s1, vec_s2))
print("-" * 70)