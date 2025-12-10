"""
===============================================================
PYTHON FUNCTIONS — INTRODUCTION FOR BEGINNERS
===============================================================

WHAT IS A FUNCTION?
-------------------
A function is a reusable block of code that:

1. Takes input (optional)
2. Executes some logic
3. Returns output (optional)

We create functions so we don't repeat the same code again and again.

BASIC FUNCTION SYNTAX:
----------------------
def function_name(parameters):
    # function body
    return value   # optional

Example:
def add(a, b):
    return a + b
"""

print("\nFUNCTION BASICS\n")


# -------------------------------------------------------------
# 1. SIMPLE FUNCTION WITH NO INPUT AND NO RETURN
# -------------------------------------------------------------
# This function does not take any parameter.
# It simply prints a welcome message.
def greet():
    print("Hello, welcome to Python functions!")

greet()  # calling the function
print("-" * 70)


# -------------------------------------------------------------
# 2. FUNCTION WITH INPUT (PARAMETERS)
# -------------------------------------------------------------
# 'name' is a parameter. The caller must provide a value.
def say_hello(name):
    print("Hello", name)

say_hello("Rahul")
say_hello("Students")
print("-" * 70)


# -------------------------------------------------------------
# 3. FUNCTION WITH RETURN VALUE
# -------------------------------------------------------------
# This function performs a calculation and RETURNS a result
def add(a, b):
    return a + b

result = add(10, 20)  # returned value is stored in variable
print("Result of add(10, 20):", result)
print("-" * 70)


# -------------------------------------------------------------
# 4. FUNCTION WITH DEFAULT PARAMETERS
# -------------------------------------------------------------
# If caller does NOT pass a value, default value ("Guest") is used.
def greet_person(name="Guest"):
    print("Hello", name)

greet_person()          # uses default value
greet_person("Prudhvi") # overrides default
print("-" * 70)


# -------------------------------------------------------------
# 5. FUNCTION RETURNING MULTIPLE VALUES
# -------------------------------------------------------------
# Python allows returning multiple values (as a tuple)
def get_stats(numbers):
    total = sum(numbers)
    length = len(numbers)
    average = total / length
    return total, length, average  # returning 3 values

# unpacking multiple returned values
total, length, average = get_stats([10, 20, 30, 40])
print("Total:", total)
print("Length:", length)
print("Average:", average)
print("-" * 70)


# -------------------------------------------------------------
# 6. FUNCTION WITH DOCSTRING (VERY IMPORTANT)
# -------------------------------------------------------------
# A docstring describes what the function does and is used by tools and documentation.
def multiply(a, b):
    """
    Multiplies two numbers and returns the result.

    Parameters:
        a (int or float)
        b (int or float)

    Returns:
        int or float: The multiplication result
    """
    return a * b

print("multiply(4, 5) =", multiply(4, 5))
print("Function docstring:")
print(multiply.__doc__)
print("-" * 70)


# -------------------------------------------------------------
# *ARGS - multiple positional arguments
# -------------------------------------------------------------
# *args collects all extra positional values into a TUPLE
def add_numbers(*args):
    print("Numbers received:", args)
    print("Sum:", sum(args))

add_numbers(1, 2, 3)
add_numbers(10, 20, 30, 40, 50)
print("-" * 70)

# -------------------------------------------------------------
# **KWARGS - multiple keyword arguments
# -------------------------------------------------------------
# **kwargs collects all keyword arguments into a DICTIONARY
def show_profile(**kwargs):
    print("Profile data:", kwargs)

show_profile(name="Rahul", city="Pune", skills=["Python", "SQL"])
print("-" * 70)

# -------------------------------------------------------------
# COMBINING ALL ARGUMENT TYPES
# -------------------------------------------------------------
# a, b → positional
# *args → extra positional
# c, d → keyword-only with default values
# **kwargs → extra keyword arguments
def demo(a, b, *args, c=10, d=20, **kwargs):
    print("a:", a)
    print("b:", b)
    print("args:", args)
    print("c:", c)
    print("d:", d)
    print("kwargs:", kwargs)

demo(1, 2, 3, 4, 5, c=99, x=100, y=200)
print("-" * 70)


# -------------------------------------------------------------
# REAL WORLD EXAMPLE
# -------------------------------------------------------------
def create_user(username, email, *roles, active=True, **extra_info):
    """
    Creates a user profile with flexible arguments.
    * username, email → required positional arguments
    * *roles → variable-length roles, stored as tuple
    * active → keyword argument with default
    * **extra_info → extra fields like country, age, etc.
    """
    print("Username:", username)
    print("Email:", email)
    print("Roles:", roles)
    print("Active:", active)
    print("Extra info:", extra_info)

create_user(
    "rahul123",
    "rahul@example.com",
    "admin", "editor",
    active=False,
    country="India",
    age=33
)
print("-" * 70)


# -------------------------------------------------------------
# GLOBAL KEYWORD: Demonstration
# -------------------------------------------------------------
# A global variable exists outside all functions
counter = 0

# Without global keyword, assignment will create a LOCAL variable
def increment_with_global():
    global counter  # tells Python to use global 'counter'
    counter = counter + 1  # modifies the global variable

print("Before increment_with_global():", counter)
increment_with_global()
print("After increment_with_global():", counter)  # global variable updated
print("-" * 70)


# -------------------------------------------------------------
# Lambda Functions — one-line, anonymous functions
# -------------------------------------------------------------
# A lambda function is useful when we need a small simple function

# normal function
def square(x):
    return x*x

# equivalent lambda function
square_lambda = lambda x: x*x

print("Normal square function:", square(5))
print("Lambda square function:", square_lambda(5))
print("-" * 40)

#-----------------------------------------------------
# More lambda examples
add = lambda a, b: a + b
print("Lambda add:", add(10, 20))

#-----------------------------------------------------
is_even = lambda n: n % 2 == 0
print("Lambda is_even:", is_even(4), is_even(7))

# Lambdas are often used with map(), filter(), reduce() in real projects
print("-" * 70)