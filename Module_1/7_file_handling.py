"""
======================================================================
PYTHON FILE HANDLING — READ, WRITE, APPEND, SAFE ACCESS
======================================================================

File handling lets Python programs interact with external datasets such as:
- text datasets (.txt)
- CSV datasets
- log datasets
- configuration datasets

Common modes:
-------------
"r"  → READ ONLY (file must already exist)
"w"  → WRITE (creates a file or overwrites an existing one)
"a"  → APPEND (adds content at the end, does not erase)
"r+" → READ + WRITE (file must exist)
"w+" → WRITE + READ (clears the file first)
"a+" → APPEND + READ (keeps existing data)

Always prefer:
    with open(filename, mode) as f:
because it:
- automatically closes the file,
- avoids memory leaks,
- handles exceptions more safely.

This module demonstrates:
- Writing text
- Writing lists of lines
- Reading entire datasets
- Line-by-line reading
- Appending data
- Logging example
- Reading config datasets
======================================================================
"""

print("\nFILE HANDLING BASICS\n")

# -------------------------------------------------------------
# WRITING TO A FILE (creates if not exists, overwrites if exists)
# -------------------------------------------------------------
# Using "w" will erase any existing content and start fresh.
# "\n" must be added manually to create new lines.
with open("example.txt", "w") as f:
    f.write("Hello!\n")
    f.write("This is a new file created using Python.\n")

print("File written successfully.")
print("-" * 70)

# -------------------------------------------------------------
# WRITING A LIST OF LINES TO A FILE
# -------------------------------------------------------------
# writelines() writes each string in the list exactly as-is.
# It DOES NOT automatically add newline characters.
lines = [
    "Python is powerful.\n",
    "File handling is easy.\n",
    "Writing lists saves time!\n"
]

with open("list_output.txt", "w") as f:
    f.writelines(lines)

print("List of lines written successfully to list_output.txt")
print("-" * 70)

# -------------------------------------------------------------
# READING A FULL FILE INTO A SINGLE STRING
# -------------------------------------------------------------
# read() loads *entire* content into one string.
with open("example.txt", "r") as f:
    content = f.read()

print("File content:\n", content)
print("-" * 70)

# -------------------------------------------------------------
# APPENDING DATA TO A FILE (does not delete existing data)
# -------------------------------------------------------------
# "a" opens the file and moves the cursor to the end.
# New writes always go after the last existing line.
with open("example.txt", "a") as f:
    f.write("Adding one more line to the file.\n")

print("Line appended successfully.")
print("-" * 70)

# -------------------------------------------------------------
# READING LINE-BY-LINE USING A LOOP (memory-efficient)
# -------------------------------------------------------------
# Iterating over `f` gives one line per iteration.
# strip() removes newline characters for cleaner printing.
print("Reading file line by line:")
with open("example.txt", "r") as f:
    for line in f:
        print("Line:", line.strip())

print("-" * 70)

# -------------------------------------------------------------
# READING ALL LINES INTO A LIST USING readlines()
# -------------------------------------------------------------
# Each line becomes one item in a Python list.
with open("example.txt", "r") as f:
    lines = f.readlines()

print("Lines list:", lines)
print("-" * 70)

# -------------------------------------------------------------
# REAL-WORLD EXAMPLE: WRITING TO A LOG FILE
# -------------------------------------------------------------
# Log datasets typically use append mode and timestamped entries.
import datetime

# Generate a log entry with the current date/time.
log_message = f"{datetime.datetime.now()} - User logged in\n"

with open("app.log", "a") as f:
    f.write(log_message)

print("Log entry added to app.log")
print("-" * 70)

# -------------------------------------------------------------
# REAL-WORLD EXAMPLE: READING A SIMPLE CONFIG FILE
# -------------------------------------------------------------
# Step 1: Write a small config file with key=value format.
with open("config.txt", "w") as f:
    f.write("url=https://api.example.com\n")
    f.write("timeout=30\n")

# Step 2: Read and parse the config file.
# split("=") separates the key and value in each line.
with open("config.txt", "r") as f:
    for line in f:
        key, value = line.strip().split("=")
        print(key, ":", value)

print("-" * 70)