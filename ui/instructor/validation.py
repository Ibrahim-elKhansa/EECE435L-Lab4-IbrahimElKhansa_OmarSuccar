from sql.db_operations import get_all_instructors

def is_unique_instructor_id(instructor_id):
    """
    Checks if a given instructor ID is unique within the database.

    This function retrieves all instructors from the database and iterates through them 
    to check if any instructor has the same ID as the provided `instructor_id`.

    Args:
        instructor_id (int): The ID of the instructor to be checked for uniqueness.

    Returns:
        bool: 
            - True if the instructor ID is unique and not already present in the database.
            - False if an instructor with the same ID already exists in the database.
    """
    instructors = get_all_instructors()
    for instructor in instructors:
        if instructor.instructor_id == instructor_id:
            return False
    return True
