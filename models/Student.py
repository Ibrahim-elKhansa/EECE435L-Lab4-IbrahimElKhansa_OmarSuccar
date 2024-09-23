from models.Person import Person

class Student(Person):
    """
    A class representing a student in the school management system, inheriting from the Person class.

    Attributes:
        name (str): The name of the student, inherited from the Person class.
        age (int): The age of the student, inherited from the Person class.
        email (str): The email of the student, inherited from the Person class.
        student_id (int): A unique identifier for the student.

    Methods:
        __init__(name, age, email, student_id):
            Initializes a new instance of the Student class with the given name, age, email, and student ID.
    """
    def __init__(self, name, age, email, student_id):
        """
        Initializes a new instance of the Student class.

        Args:
            name (str): The name of the student.
            age (int): The age of the student.
            email (str): The email address of the student.
            student_id (int): A unique identifier for the student.
        """
        super().__init__(name, age, email)
        self.student_id = student_id
