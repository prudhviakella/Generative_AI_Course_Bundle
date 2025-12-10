"""
======================================================================
PYTHON OBJECT ORIENTED PROGRAMMING (OOP) — COMPLETE BEGINNER MODULE
======================================================================

OOP allows us to structure code using **classes** and **objects**.

KEY TERMS:
----------
Class:
    - A blueprint/template for creating objects.
    - Example: Car, Student, BankAccount.

Object:
    - A real instance created from a class.
    - Example: car1, car2, a_student, my_account.

Attributes:
    - Variables inside a class (data/properties).

Methods:
    - Functions inside a class (actions/behavior).

Constructor (__init__):
    - Special method that runs when an object is created.
    - Used to initialize object attributes.

self:
    - Refers to the current object.
    - Used to access attributes/methods inside the class.

OOP Concepts Covered:
---------------------
1. Class & Object
2. Attributes & Methods
3. Constructor (__init__)
4. Encapsulation (private attributes)
5. Inheritance
6. Polymorphism (method overriding)
7. Real-world examples
======================================================================
"""

print("\nOBJECT ORIENTED PROGRAMMING BASICS\n")

# -------------------------------------------------------------
# BASIC CLASS AND OBJECT
# -------------------------------------------------------------
class Student:
    # attributes + methods will go here
    pass

# creating objects
s1 = Student()
s2 = Student()

print("Two student objects created:", s1, s2)
print("-" * 70)

# -------------------------------------------------------------
# CLASS WITH ATTRIBUTES AND METHODS
# -------------------------------------------------------------
class Car:
    def __init__(self, brand, model):
        self.brand = brand      # attribute
        self.model = model      # attribute

    def show_info(self):         # method
        print(f"Car: {self.brand} {self.model}")

car1 = Car("Toyota", "Innova")
car2 = Car("Honda", "City")

car1.show_info()
car2.show_info()
print("-" * 70)

# -------------------------------------------------------------
# REAL-WORLD EXAMPLE: BANK ACCOUNT
# -------------------------------------------------------------
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited {amount}. New balance = {self.balance}")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient Balance!")
        else:
            self.balance -= amount
            print(f"Withdrawn {amount}. Remaining balance = {self.balance}")

acct = BankAccount("Rahul", 5000)
acct.deposit(1000)
acct.withdraw(3000)
acct.withdraw(5000)
print("-" * 70)

# -------------------------------------------------------------
# ENCAPSULATION (PRIVATE ATTRIBUTES)
# -------------------------------------------------------------
class BankAccount:
    bank_name = "XYZ" # class level attribute
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.set_balance(balance)

    def set_balance(self, new_balance):
        # Validation
        self.__balance = new_balance

    def get_balance(self):
        # Validation
        return self.__balance

    def deposit(self, amount):
        self.__balance += amount
        print(f"Deposited {amount}. New balance = {self.__balance}")

    def withdraw(self, amount):
        if amount > self.__balance:
            print("Insufficient Balance!")
        else:
            self.__balance -= amount
            print(f"Withdrawn {amount}. Remaining balance = {self.__balance}")

acct = BankAccount("Rahul", 5000)
acct.deposit(1000)
acct.withdraw(3000)
acct.withdraw(5000)
print("-" * 70)
print(acct.get_balance())

class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.__salary = salary   # private attribute

    def show_salary(self):
        print(f"{self.name}'s salary is {self.__salary}")

    def set_salary(self, new_salary):
        if new_salary > 0:
            self.__salary = new_salary
        else:
            print("Invalid salary")

e = Employee("Akhil", 50000)
e.show_salary()
e.set_salary(60000)
e.show_salary()

e.__salary  # This will raise error (private variable)
print("-" * 70)

# -------------------------------------------------------------
# INHERITANCE
# -------------------------------------------------------------
class Animal:
    def speak(self):
        print("Animal makes a sound")

class Dog(Animal):   # Dog inherits speak() from Animal
    def bark(self):
        print("Dog barks: Woof!")

d = Dog()
d.speak()   # inherited
d.bark()    # own method
print("-" * 70)

# -------------------------------------------------------------
# POLYMORPHISM (same method, different behavior)
# -------------------------------------------------------------
class Bird:
    def sound(self):
        print("Bird sound")

class Sparrow(Bird):
    def sound(self):                    # overriding
        print("Sparrow chirps")

class Crow(Bird):
    def sound(self):
        print("Crow caws")

birds = [Sparrow(), Crow(), Bird()]

for b in birds:
    b.sound()   # different output for each object
print("-" * 70)

# -------------------------------------------------------------
# REAL-WORLD EXAMPLE: EMPLOYEE MANAGEMENT
# -------------------------------------------------------------
class Employee:
    def __init__(self, name, emp_id, role):
        self.name = name
        self.emp_id = emp_id
        self.role = role

    def show_details(self):
        print(f"{self.name} ({self.emp_id}) - {self.role}")

class Manager(Employee):

    def assign_task(self):
        print(f"{self.name} assigns tasks to the team.")

class Developer(Employee):
    def __init__(self, name, emp_id, role):
        super().__init__(name, emp_id, role)

    def write_code(self):
        print(f"{self.name} writes Python code.")

m = Manager("Prudhvi", 101, "Manager")
d = Developer("Rahul", 102, "Developer")

m.show_details()
m.assign_task()

d.show_details()
d.write_code()
print("-" * 70)

# -------------------------------------------------------------
# ABSTRACT BASE CLASS (INTERFACE-LIKE)
# -------------------------------------------------------------
from abc import ABC, abstractmethod

class Notifiable(ABC):
    """
    Abstract Base Class (interface-like).

    Any subclass MUST implement:
    - connect()
    - notify(message)
    - disconnect()

    This mimics real-world notification systems where:
      • You connect to a service (email server/SMS gateway/device)
      • Send notification
      • Disconnect safely
    """

    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def notify(self, message: str) -> None:
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass

class EmailNotifier(Notifiable):
    def __init__(self, email_address: str):
        self.email_address = email_address

    def connect(self):
        print(f"Connecting to Email Server for {self.email_address}...")

    def notify(self, message: str):
        print(f"[EMAIL to {self.email_address}] {message}")

    def disconnect(self):
        print("Email server connection closed.")


class SMSNotifier(Notifiable):
    def __init__(self, phone: str):
        self.phone = phone

    def connect(self):
        print(f"Connecting to SMS Gateway for {self.phone}...")

    def notify(self, message: str):
        print(f"[SMS to {self.phone}] {message}")

    def disconnect(self):
        print("SMS gateway connection closed.")


class PushNotifier(Notifiable):
    def __init__(self, device_id: str):
        self.device_id = device_id

    def connect(self):
        print(f"Connecting to Push Notification Service for device {self.device_id}...")

    def notify(self, message: str):
        print(f"[PUSH NOTIFICATION to {self.device_id}] {message}")

    def disconnect(self):
        print("Push service connection closed.")

email = EmailNotifier("student@example.com")
sms = SMSNotifier("+911234567890")
push = PushNotifier("DEVICE-123")

for notifier in (email, sms, push):
    notifier.connect()
    notifier.notify("Your book is due tomorrow!")
    notifier.disconnect()
    print("-" * 50)


from abc import ABC, abstractmethod


class A:

    def __init__(self,a):
        self.a = a
    def class_a_method(self):
        print(f"class_a_method, a value is {self.a}")

class B:
    def __init__(self,b):
        self.b = b

    def class_b_method(self):
        print(f"class_b_method, b value is {self.b}")


class C(ABC):
    @abstractmethod
    def class_c_method(self):
        pass

class D(A,B,C):
    def __init__(self,a,b):
        super().__init__(a)
        B.__init__(self,b)


    def class_c_method(self):
        print(f"class_c_method, implemented in class D")


d = D(1,2)
d.class_a_method()
d.class_b_method()
d.class_c_method()

# -------------------------
# 2) CLASSMETHOD vs STATICMETHOD
# -------------------------
print("\n2) classmethod vs staticmethod\n")


class IDGenerator:
    """
    This class demonstrates the difference between:

    1. Class Variables
    2. @classmethod
    3. @staticmethod

    WHERE THEY ARE USED IN REAL LIFE:
    ---------------------------------
    ✔ classmethod
       - Used when you want to work with CLASS-LEVEL data shared
         across ALL objects.
       - Example: auto-increment IDs, counters, configuration.

    ✔ staticmethod
       - Used for helper/utility functions that do not touch class or object.
       - Example: string validation, number checks, formatters.

    CLASS VARIABLE:
    ---------------
    _next_id is a class variable:
    - It is shared by ALL instances of IDGenerator.
    - This makes it perfect for generating unique IDs.
    """
    _next_id = 1  # class variable (shared across all instances)

    # -------------------------------------------------------------
    # CLASSMETHOD
    # -------------------------------------------------------------
    @classmethod
    def next_id(cls) -> int:
        """
        CLASSMETHOD DETAILS:
        ---------------------
        - Python passes the CLASS itself as the first argument (cls)
        - Allows method to modify class-level variables
        - Can be called using:
              IDGenerator.next_id()
              OR
              obj.next_id()   # but class is passed internally

        WHAT THIS METHOD DOES:
        -----------------------
        1. Reads the current value of cls._next_id
        2. Returns it
        3. Increments it for the next call
        """
        id_ = cls._next_id  # read class variable
        cls._next_id += 1  # modify class variable
        return id_

    # -------------------------------------------------------------
    # STATICMETHOD
    # -------------------------------------------------------------
    @staticmethod
    def is_valid_isbn(isbn: str) -> bool:
        """
        STATICMETHOD DETAILS:
        ----------------------
        - Does NOT receive self or cls
        - Cannot access object attributes or class variables directly
        - Behaves like a normal function placed inside a class

        WHY USE A STATIC METHOD?
        -------------------------
        To group logically related helper functions inside a class.

        WHAT THIS METHOD DOES:
        -----------------------
        Very naive ISBN validation:
        - string must be non-empty
        - after removing hyphens, remaining characters must be digits
        """
        return isinstance(isbn, str) and isbn.replace("-", "").isdigit()


# -------------------------------------------------------------
# USAGE DEMO
# -------------------------------------------------------------

# Calling next_id() increments the class variable.
print("Generated IDs:", IDGenerator.next_id(), IDGenerator.next_id())
# Output example: Generated IDs: 1 2

# staticmethod usage:
print("ISBN valid check (12345):", IDGenerator.is_valid_isbn("12345"))
# True → contains digits only

print("ISBN valid check (abc):", IDGenerator.is_valid_isbn("abc"))
# False → not numeric


# -------------------------
# 3) OPERATOR OVERLOADING/ Magic or Dunder Methods
# -------------------------
print("\n3) OPERATOR OVERLOADING\n")

class Book:
    """
    Book model with operator overloads.

    Why Operator Overloading?
    -------------------------
    Operator overloading lets your objects behave like built-in types.
    Example:
        If you do 3 + 5 → Python calls int.__add__(3, 5)
        If you do book1 == book2 → Python calls Book.__eq__(book1, book2)
        If you sort a list of Book objects → Python calls Book.__lt__()

    We overload:
      - __str__   → Human-friendly printing (used by print())
      - __repr__  → Developer-friendly representation (used in debugging, REPL)
      - __eq__    → Compare books by ISBN (equality)
      - __lt__    → Compare books by title (sorting)
    """

    def __init__(self, isbn: str, title: str, author: str, copies: int = 1):
        # Object attributes
        self.isbn = isbn
        self.title = title
        self.author = author
        self.copies = copies

    # -------------------------------------------------------------
    # __str__ → Human readable string (used by print(), str())
    # -------------------------------------------------------------
    # Purpose: When you print the object, show user-friendly info.
    # Example: print(book1)
    # Output:  Python 101 by A. Author (ISBN: 978-1111) - Copies: 3
    def __str__(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn}) - Copies: {self.copies}"

    # -------------------------------------------------------------
    # __repr__ → Developer readable (used in debugging and REPL)
    # -------------------------------------------------------------
    # Purpose: A precise representation useful for debugging.
    # Example: typing `book1` in Python shell prints repr(book1)
    def __repr__(self):
        return f"Book({self.isbn!r}, {self.title!r}, {self.author!r}, copies={self.copies})"

    # -------------------------------------------------------------
    # __eq__ → Equality operator (==)
    # -------------------------------------------------------------
    # Purpose: Decide when two Book objects are "equal".
    # We consider books equal if their ISBN matches.
    #
    # Python internally translates:
    #    book1 == book2
    # into:
    #    Book.__eq__(book1, book2)
    def __eq__(self, other):
        if not isinstance(other, Book):
            return NotImplemented  # Let Python handle type mismatch
        return self.isbn == other.isbn

    # -------------------------------------------------------------
    # __lt__ → Less than operator (<)
    # -------------------------------------------------------------
    # Purpose: Allow sorting of Book objects using `sorted()` or `.sort()`.
    #
    # Python internally calls:
    #   book1 < book2
    # as:
    #   Book.__lt__(book1, book2)
    #
    # We compare based on TITLE alphabetically.
    def __lt__(self, other):
        if not isinstance(other, Book):
            return NotImplemented
        return self.title < other.title

    # Normal class methods
    def add_copies(self, n: int = 1):
        self.copies += n

    def remove_copy(self):
        if self.copies <= 0:
            raise ValueError("No copies available to remove")
        self.copies -= 1


# -------------------------------------------------------------
# Demo showing all overloaded operators in action
# -------------------------------------------------------------
b1 = Book("978-1111", "Python 101", "A. Author", copies=3)
b2 = Book("978-2222", "Advanced Python", "B. Author", copies=2)

# __str__():
# When print() is used → Python calls b1.__str__()
print(str(b1))

# __repr__():
# Used mostly for debugging, printing in lists, REPL
print(repr(b2))

# __eq__():
# Compares only ISBN — titles/authors don't matter here
print("Equality by ISBN:", b1 == Book("978-1111", "Dummy", "X"))

# __lt__():
# Allows sorting by title automatically
print("Sorted by title:", sorted([b2, b1]))