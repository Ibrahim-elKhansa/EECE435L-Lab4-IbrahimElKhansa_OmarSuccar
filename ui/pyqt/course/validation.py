from sql.db_operations import get_all_courses

def is_unique_course_name(course_name):
    """
    Checks if a given course name is unique within the database.

    This function retrieves all courses from the database and iterates through them 
    to check if any course has the same name as the provided `course_name`. 

    Args:
        course_name (str): The name of the course to be checked for uniqueness.

    Returns:
        bool: 
            - True if the course name is unique and not already present in the database.
            - False if a course with the same name already exists in the database.
    """
    courses = get_all_courses()
    for course in courses:
        if course.course_name == course_name:
            return False
    return True
