class Course:
    """
    A class representing a course in the school management system.

    Attributes:
        course_name (str): The name of the course. This should be unique and serves as the identifier for the course.
        instructor (Instructor, optional): An instance of the Instructor class representing the instructor assigned to the course.
            Defaults to None if no instructor is assigned.

    Methods:
        __init__(course_name, instructor=None):
            Initializes a new instance of the Course class with the given course name and optional instructor.
    """
    def __init__(self, course_name, instructor=None):
        """
        Initializes a new instance of the Course class.

        Args:
            course_name (str): The name of the course.
            instructor (Instructor, optional): An instance of the Instructor class representing the instructor assigned to the course.
                Defaults to None if no instructor is assigned.
        """
        self.course_name = course_name
        self.instructor = instructor
