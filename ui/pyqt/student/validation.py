import re
from sql.db_operations import get_all_students

def validate_email(email):
    """
    Validates the format of a given email address.

    This function uses a regular expression to check if the provided email address 
    matches the standard format for email addresses.

    Args:
        email (str): The email address to validate.

    Returns:
        bool: 
            - True if the email address is in a valid format.
            - False if the email address is not in a valid format.
    """
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email)

def is_unique_student_id(student_id):
    """
    Checks if a given student ID is unique within the database.

    This function retrieves all students from the database and iterates through them 
    to check if any student has the same ID as the provided `student_id`.

    Args:
        student_id (int): The ID of the student to be checked for uniqueness.

    Returns:
        bool: 
            - True if the student ID is unique and not already present in the database.
            - False if a student with the same ID already exists in the database.
    """
    students = get_all_students()
    for student in students:
        if student.student_id == student_id:
            return False
    return True
