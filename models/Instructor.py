from models.Person import Person

class Instructor(Person):
    """
    A class representing an instructor in the school management system, inheriting from the Person class.

    Attributes:
        name (str): The name of the instructor, inherited from the Person class.
        age (int): The age of the instructor, inherited from the Person class.
        email (str): The email of the instructor, inherited from the Person class.
        instructor_id (int): A unique identifier for the instructor.

    Methods:
        __init__(name, age, email, instructor_id):
            Initializes a new instance of the Instructor class with the given name, age, email, and instructor ID.
    """
    def __init__(self, name, age, email, instructor_id):
        """
        Initializes a new instance of the Instructor class.

        Args:
            name (str): The name of the instructor.
            age (int): The age of the instructor.
            email (str): The email address of the instructor.
            instructor_id (int): A unique identifier for the instructor.
        """
        super().__init__(name, age, email)
        self.instructor_id = instructor_id
