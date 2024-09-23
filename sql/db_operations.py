import sqlite3
from models.Student import Student
from models.Instructor import Instructor
from models.Course import Course
from sql.create import create_tables

def connect_db():
    """
    Connects to the SQLite database and creates the necessary tables if they do not exist.

    Returns:
        sqlite3.Connection: A connection object to the SQLite database 'sql/school_management.db'.
    """
    create_tables()
    return sqlite3.connect('sql/school_management.db')

### INSERT RECORD FUNCTIONS ###

def insert_student(student):
    """
    Inserts a new student record into the 'students' table.

    Args:
        student (Student): An instance of the Student class containing the student's information.

    Raises:
        sqlite3.IntegrityError: If a student with the same ID or email already exists in the table.
    """
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO students (student_id, name, age, email) VALUES (?, ?, ?, ?)', 
                (student.student_id, student.name, student.age, student.get_email()))
    conn.commit()
    conn.close()

def insert_instructor(instructor):
    """
    Inserts a new instructor record into the 'instructors' table.

    Args:
        instructor (Instructor): An instance of the Instructor class containing the instructor's information.

    Raises:
        sqlite3.IntegrityError: If an instructor with the same ID or email already exists in the table.
    """
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO instructors (instructor_id, name, age, email) VALUES (?, ?, ?, ?)', 
                (instructor.instructor_id, instructor.name, instructor.age, instructor.get_email()))
    conn.commit()
    conn.close()

def insert_course(course):
    """
    Inserts a new course record into the 'courses' table.

    Args:
        course (Course): An instance of the Course class containing the course's information.

    Raises:
        sqlite3.IntegrityError: If a course with the same name already exists in the table.
    """
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO courses (course_name, instructor_id) VALUES (?, ?)', 
                (course.course_name, course.instructor.instructor_id if course.instructor else None))
    conn.commit()
    conn.close()

### REGISTER STUDENT FOR COURSE ###

def register_student_for_course(student_id, course_name):
    """
    Registers a student for a course by inserting a record into the 'student_courses' table.

    Args:
        student_id (int): The ID of the student to register.
        course_name (str): The name of the course to register the student for.

    Raises:
        sqlite3.IntegrityError: If the student is already registered for the course.
    """
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO student_courses (student_id, course_name) VALUES (?, ?)', 
                (student_id, course_name))
    conn.commit()
    conn.close()

def delete_student_from_course(student_id, course_name):
    """
    Unregisters a student from a course by deleting the record from the 'student_courses' table.

    Args:
        student_id (int): The ID of the student to unregister.
        course_name (str): The name of the course to unregister the student from.
    """
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM student_courses WHERE student_id = ? AND course_name = ?', 
                (student_id, course_name))
    conn.commit()
    conn.close()

### RETRIEVE COURSES A STUDENT IS REGISTERED FOR ###

def get_courses_by_student(student_id):
    """
    Retrieves a list of course names a student is registered for.

    Args:
        student_id (int): The ID of the student.

    Returns:
        list: A list of course names the student is registered for.
    """
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('SELECT course_name FROM student_courses WHERE student_id = ?', (student_id,))
    courses_data = cur.fetchall()
    conn.close()
    return [row[0] for row in courses_data]  # Returns a list of course names

### RETRIEVE STUDENTS REGISTERED FOR A COURSE ###

def get_students_by_course(course_name):
    """
    Retrieves a list of student IDs registered for a specific course.

    Args:
        course_name (str): The name of the course.

    Returns:
        list: A list of student IDs registered for the course.
    """
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('SELECT student_id FROM student_courses WHERE course_name = ?', (course_name,))
    students_data = cur.fetchall()
    conn.close()
    return [row[0] for row in students_data]  # Returns a list of student IDs

def is_student_registered_for_course(student_id, course_name):
    """
    Checks if a student is already registered for a specific course.

    Args:
        student_id (int): The ID of the student.
        course_name (str): The name of the course.

    Returns:
        bool: True if the student is registered for the course, False otherwise.
    """
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM student_courses WHERE student_id = ? AND course_name = ?', 
                (student_id, course_name))
    result = cur.fetchone()  # Fetch one result (if any)
    conn.close()
    return result is not None  # Return True if a result is found (student is already registered)

### GET ALL RECORDS FUNCTIONS ###

def get_all_students():
    """
    Retrieves all student records from the 'students' table.

    Returns:
        list: A list of Student instances representing all students in the database.
    """
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM students')
    students_data = cur.fetchall()
    conn.close()

    # Map to Student class instances
    students = [Student(name=row[1], age=row[2], email=row[3], student_id=row[0]) for row in students_data]
    return students

def get_all_instructors():
    """
    Retrieves all instructor records from the 'instructors' table.

    Returns:
        list: A list of Instructor instances representing all instructors in the database.
    """
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM instructors')
    instructors_data = cur.fetchall()
    conn.close()

    # Map to Instructor class instances
    instructors = [Instructor(name=row[1], age=row[2], email=row[3], instructor_id=row[0]) for row in instructors_data]
    return instructors

def get_all_courses():
    """
    Retrieves all course records from the 'courses' table.

    Returns:
        list: A list of Course instances representing all courses in the database.
    """
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM courses')
    courses_data = cur.fetchall()
    conn.close()

    # Map to Course class instances
    courses = []
    for row in courses_data:
        instructor = get_instructor_by_id(row[1]) if row[1] else None  # Get the instructor object if available
        courses.append(Course(course_name=row[0], instructor=instructor))
    return courses

### UPDATE RECORD FUNCTIONS ###

def update_student(student):
    """
    Updates the details of a student in the 'students' table.

    Args:
        student (Student): An instance of the Student class containing the updated student information.
    """
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('UPDATE students SET name = ?, age = ?, email = ? WHERE student_id = ?', 
                (student.name, student.age, student.email, student.student_id))
    conn.commit()
    conn.close()

def update_instructor(instructor):
    """
    Updates the details of an instructor in the 'instructors' table.

    Args:
        instructor (Instructor): An instance of the Instructor class containing the updated instructor information.
    """
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('UPDATE instructors SET name = ?, age = ?, email = ? WHERE instructor_id = ?', 
                (instructor.name, instructor.age, instructor.email, instructor.instructor_id))
    conn.commit()
    conn.close()

def update_course(course):
    """
    Updates the instructor assigned to a course in the 'courses' table.

    Args:
        course (Course): An instance of the Course class containing the updated course information.
    """
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('UPDATE courses SET instructor_id = ? WHERE course_name = ?', 
                (course.instructor.instructor_id if course.instructor else None, course.course_name))
    conn.commit()
    conn.close()

### DELETE RECORD FUNCTIONS ###

def delete_student(student_id):
    """
    Deletes a student record from the 'students' table.

    Args:
        student_id (int): The ID of the student to be deleted.
    """
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM students WHERE student_id = ?', (student_id,))
    conn.commit()
    conn.close()

def delete_instructor(instructor_id):
    """
    Deletes an instructor record from the 'instructors' table.

    Args:
        instructor_id (int): The ID of the instructor to be deleted.
    """
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM instructors WHERE instructor_id = ?', (instructor_id,))
    conn.commit()
    conn.close()

def delete_course(course_name):
    """
    Deletes a course record from the 'courses' table.

    Args:
        course_name (str): The name of the course to be deleted.
    """
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM courses WHERE course_name = ?', (course_name,))
    conn.commit()
    conn.close()

### HELPER FUNCTIONS ###

def get_instructor_by_id(instructor_id):
    """
    Retrieves an instructor record by their ID from the 'instructors' table.

    Args:
        instructor_id (int): The ID of the instructor.

    Returns:
        Instructor: An instance of the Instructor class representing the instructor, or None if not found.
    """
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM instructors WHERE instructor_id = ?', (instructor_id,))
    instructor_data = cur.fetchone()
    conn.close()
    if instructor_data:
        return Instructor(name=instructor_data[1], age=instructor_data[2], email=instructor_data[3], instructor_id=instructor_data[0])
    return None
