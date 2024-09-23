import re

class Person:
    """
    A class representing a person with basic attributes like name, age, and email.

    Attributes:
        name (str): The name of the person.
        age (int): The age of the person. Must be a non-negative integer.
        _email (str): The private attribute storing the person's email address. The email is validated before being set.

    Methods:
        __init__(name, age, email):
            Initializes a new instance of the Person class with the given name, age, and email.
        validate_age(age):
            Validates that the given age is non-negative. Raises a ValueError if the age is negative.
        validate_email(email):
            Validates the format of the given email. Raises a ValueError if the email format is invalid.
        introduce():
            Prints a brief introduction of the person.
        get_email():
            Returns the person's email address.
        set_email(email):
            Sets a new email address for the person after validating its format.
    """
    def __init__(self, name, age, email):
        """
        Initializes a new instance of the Person class.

        Args:
            name (str): The name of the person.
            age (int): The age of the person. Must be a non-negative integer.
            email (str): The email address of the person. Must be in a valid email format.

        Raises:
            ValueError: If the age is negative or the email format is invalid.
        """
        self.name = name
        self.age = self.validate_age(age)
        self._email = self.validate_email(email)

    def validate_age(self, age):
        """
        Validates that the given age is non-negative.

        Args:
            age (int): The age to validate.

        Returns:
            int: The validated age.

        Raises:
            ValueError: If the age is negative.
        """
        if age < 0:
            raise ValueError("Age cannot be negative.")
        return age

    def validate_email(self, email):
        """
        Validates the format of the given email.

        Args:
            email (str): The email address to validate.

        Returns:
            str: The validated email address.

        Raises:
            ValueError: If the email format is invalid.
        """
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if re.match(email_regex, email):
            return email
        else:
            raise ValueError("Invalid email format.")

    def introduce(self):
        """
        Prints a brief introduction of the person, including their name and age.
        """
        print(f"Hello, my name is {self.name}. I am {self.age} years old.")
        
    def get_email(self):
        """
        Returns the email address of the person.

        Returns:
            str: The email address of the person.
        """
        return self._email
    
    def set_email(self, email):
        """
        Sets a new email address for the person after validating its format.

        Args:
            email (str): The new email address to set.

        Raises:
            ValueError: If the email format is invalid.
        """
        self._email = self.validate_email(email)
