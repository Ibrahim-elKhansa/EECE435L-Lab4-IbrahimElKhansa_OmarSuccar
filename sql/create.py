import sqlite3

def create_tables():
    """
    Creates the necessary tables for the school management system database.

    This function connects to the SQLite database located at 'sql/school_management.db'.
    It then creates the following tables if they do not already exist:

    1. `students`: Stores information about students, including a unique student ID, name, age, and email.
    2. `instructors`: Stores information about instructors, including a unique instructor ID, name, age, and email.
    3. `courses`: Stores information about courses, with each course having a unique name and an associated instructor.
    4. `student_courses`: A many-to-many relationship table that links students to courses they are enrolled in.

    Each table has the following structure:

    - `students`:
        - `student_id` (INTEGER): Primary key, unique identifier for each student.
        - `name` (TEXT): Name of the student, not nullable.
        - `age` (INTEGER): Age of the student, not nullable.
        - `email` (TEXT): Email of the student, must be unique, not nullable.

    - `instructors`:
        - `instructor_id` (INTEGER): Primary key, unique identifier for each instructor.
        - `name` (TEXT): Name of the instructor, not nullable.
        - `age` (INTEGER): Age of the instructor, not nullable.
        - `email` (TEXT): Email of the instructor, must be unique, not nullable.

    - `courses`:
        - `course_name` (TEXT): Primary key, unique name of the course.
        - `instructor_id` (INTEGER): Foreign key, references `instructors` table.

    - `student_courses`:
        - `student_id` (INTEGER): Foreign key, references `students` table.
        - `course_name` (TEXT): Foreign key, references `courses` table.
        - Primary key is a combination of `student_id` and `course_name`.

    After creating the tables, the changes are committed to the database and the connection is closed.
    """
    conn = sqlite3.connect('sql/school_management.db')
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS students (
                    student_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    email TEXT NOT NULL UNIQUE)''')

    cur.execute('''CREATE TABLE IF NOT EXISTS instructors (
                    instructor_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    email TEXT NOT NULL UNIQUE)''')

    cur.execute('''CREATE TABLE IF NOT EXISTS courses (
                    course_name TEXT PRIMARY KEY,
                    instructor_id INTEGER,
                    FOREIGN KEY (instructor_id) REFERENCES instructors (instructor_id))''')

    cur.execute('''CREATE TABLE IF NOT EXISTS student_courses (
                    student_id INTEGER,
                    course_name TEXT,
                    PRIMARY KEY (student_id, course_name),
                    FOREIGN KEY (student_id) REFERENCES students (student_id),
                    FOREIGN KEY (course_name) REFERENCES courses (course_name))''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    print("Tables created successfully.")
