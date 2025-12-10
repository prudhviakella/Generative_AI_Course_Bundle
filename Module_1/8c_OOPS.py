from abc import ABC, abstractmethod


# ===== INTERFACE / ABSTRACT BASE CLASS =====
# An Abstract Base Class (ABC) is a class that cannot be instantiated directly.
# It serves as a blueprint/contract for derived classes.
#
# An Interface is a special type of ABC that only contains abstract methods (no implementation).
# In Python, we achieve this using the ABC module and @abstractmethod decorator.
#
# Purpose: Enforces a common structure across all subclasses - any class inheriting
# from Mobile MUST implement all abstract methods.

class Mobile(ABC):
    """
    Abstract Base Class representing a Mobile phone interface.
    Defines the contract that all mobile implementations must follow.
    """

    @abstractmethod
    def speaker(self):
        """Abstract method - must be implemented by subclasses"""
        pass

    @abstractmethod
    def camera(self):
        """Abstract method - must be implemented by subclasses"""
        pass

    @abstractmethod
    def keypad(self):
        """Abstract method - must be implemented by subclasses"""
        pass

    @abstractmethod
    def resolution(self):
        """Abstract method - must be implemented by subclasses"""
        pass

    @abstractmethod
    def screen_type(self):
        """Abstract method - must be implemented by subclasses"""
        pass

    def mic(self):
        """
        Concrete method with default implementation.
        Can be used as-is or overridden by subclasses.
        """
        return "This is a genric mic"


# ===== INHERITANCE =====
# Inheritance is a mechanism where a child class acquires properties and behaviors
# from a parent class. It promotes code reuse and establishes a hierarchical relationship.
#
# Types demonstrated here:
# 1. Single Inheritance: Nokia inherits from Mobile
# 2. Multi-level Inheritance: Nokia_110 -> Nokia -> Mobile (3 levels)
# 3. Hierarchical Inheritance: Multiple classes (Nokia_110, Nokia_120) inherit from Nokia

class Nokia(Mobile):
    """
    Intermediate abstract class inheriting from Mobile.
    Inherits all abstract methods but doesn't implement them yet.
    Provides common attribute (company_name) for all Nokia models.
    """
    company_name = "nokia"


class Nokia_110(Nokia):
    """
    Concrete implementation of Nokia mobile.
    Implements most abstract methods from the Mobile interface.
    Note: resolution() and screen_type() still pass - technically incomplete but Python allows it.
    """
    model = "110"

    def speaker(self):
        return f"{self.company_name}{self.model} speaking"

    def camera(self):
        return f"{self.company_name}{self.model} clicking"

    def keypad(self):
        return f"{self.company_name}{self.model} touch"

    def resolution(self):
        pass  # Still not fully implemented

    def screen_type(self):
        pass  # Still not fully implemented


# ===== RUNTIME POLYMORPHISM (METHOD OVERRIDING) =====
# Polymorphism means "many forms" - the ability of different classes to respond
# to the same method call in different ways.
#
# Runtime Polymorphism (Method Overriding): Child class provides its own implementation
# of a method already defined in the parent class. The decision of which method to
# call is made at runtime based on the object type.

class Nokia_110a(Nokia_110):
    """
    Demonstrates Runtime Polymorphism through Method Overriding.
    Inherits from Nokia_110 but overrides specific methods with enhanced behavior.
    """
    model = "110a"

    def speaker(self):
        """
        RUNTIME POLYMORPHISM: Overrides parent's speaker() method.
        When nokia_110a.speaker() is called, this version executes, not the parent's.
        """
        return f"{self.company_name}{self.model} ATMOS speaking"

    def screen_type(self):
        """
        RUNTIME POLYMORPHISM: Provides actual implementation for previously empty method.
        """
        return f"{self.company_name}{self.model} gorilla"


class Nokia_120(Nokia):
    """
    Another concrete implementation demonstrating the same interface with different model.
    Shows how multiple classes can implement the same contract differently.
    """
    model = "120"

    def speaker(self):
        return f"{self.company_name}{self.model} speaking"

    def camera(self):
        return f"{self.company_name}{self.model} clicking"

    def keypad(self):
        return f"{self.company_name}{self.model} touch"

    def resolution(self):
        pass

    def screen_type(self):
        pass


# ===== DEMONSTRATION OF CONCEPTS =====

# Creating instance of Nokia_110
nokia_110 = Nokia_110()
print(nokia_110.camera())  # Calls Nokia_110's camera() implementation
print(nokia_110.keypad())  # Calls Nokia_110's keypad() implementation
print(nokia_110.speaker())  # Calls Nokia_110's speaker() implementation
print(nokia_110.mic())  # Inherited from Mobile (base class) - demonstrates inheritance

print("###############")

# Creating instance of Nokia_110a - demonstrates RUNTIME POLYMORPHISM
nokia_110a = Nokia_110a()
print(nokia_110a.camera())  # Inherited from Nokia_110 (parent class)
print(nokia_110a.keypad())  # Inherited from Nokia_110 (parent class)
print(nokia_110a.speaker())  # OVERRIDDEN in Nokia_110a - shows "ATMOS" instead of basic speaker
# This is RUNTIME POLYMORPHISM - different behavior for same method

print("##############")

# Creating instance of Nokia_120 - shows different implementation of same interface
nokia_120 = Nokia_120()
print(nokia_120.camera())  # Different model number in output
print(nokia_120.keypad())  # Different model number in output
print(nokia_120.speaker())  # Different model number in output

# ===== KEY CONCEPTS SUMMARY =====
#
# 1. ABSTRACT CLASS/INTERFACE (Mobile):
#    - Cannot be instantiated: Mobile() would raise TypeError
#    - Defines contract for all subclasses
#    - Forces consistent API across implementations
#
# 2. INHERITANCE (Nokia -> Mobile, Nokia_110 -> Nokia):
#    - Child classes inherit attributes and methods from parents
#    - Enables code reuse (company_name from Nokia, mic() from Mobile)
#    - Creates IS-A relationship: Nokia_110 IS-A Nokia IS-A Mobile
#
# 3. RUNTIME POLYMORPHISM (Nokia_110a.speaker() override):
#    - Same method name, different implementations
#    - Decision made at runtime based on actual object type
#    - Enables flexible, extensible code
#    - Nokia_110a responds differently to speaker() than Nokia_110