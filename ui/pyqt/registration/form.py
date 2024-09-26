from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QPushButton, QVBoxLayout, QMessageBox
from sql.db_operations import get_all_students, get_all_courses, register_student_for_course, is_student_registered_for_course

def create_registration_form(tab):
    """
    Creates a form for registering students for courses in a given PyQt5 tab.

    This function sets up a registration form with dropdown menus for selecting a student and a course.
    It includes a "Register Student" button that, when clicked, validates the selection and registers 
    the student for the chosen course in the database.

    Args:
        tab (QWidget): The PyQt5 widget (typically a frame or tab) where the form will be created.

    The form includes the following components:
    - A dropdown menu to select a student from the list of all students in the database.
    - A dropdown menu to select a course from the list of all courses in the database.
    - A "Register Student" button that triggers the student registration process.

    Internal Functions:
        - register_student(): Validates the selected student and course, checks if the student is 
                              already registered for the course, and registers the student if not.

    Raises:
        QMessageBox: If either student or course is not selected, or if the student is already 
                     registered for the selected course.
    """
    # Clear existing widgets from the tab layout
    for i in reversed(range(tab.layout().count())): 
        tab.layout().itemAt(i).widget().deleteLater()

    def register_student():
        """
        Registers the selected student for the selected course.

        This function retrieves the student ID and course name from the dropdown menus, checks if the 
        student is already registered for the course, and registers the student if they are not. 
        It displays an error message if either selection is missing or if the student is already 
        registered for the course, and a success message upon successful registration.

        Raises:
            QMessageBox: If either student or course is not selected, or if the student is already 
                         registered for the selected course.
        """
        student_id = student_dropdown.currentText()
        course_name = course_dropdown.currentText()

        # Validate that both student and course are selected
        if student_id == "None" or course_name == "None":
            QMessageBox.critical(tab, "Error", "Please select both a student and a course.")
            return

        # Check if student is already registered for the course
        if is_student_registered_for_course(int(student_id), course_name):
            QMessageBox.critical(tab, "Error", "Student is already registered for this course.")
            return

        # Register student for the course
        register_student_for_course(int(student_id), course_name)
        QMessageBox.information(tab, "Success", "Student registered for the course successfully.")

        # Reset dropdown selections
        student_dropdown.setCurrentIndex(0)
        course_dropdown.setCurrentIndex(0)

    # Set up the layout
    layout = QVBoxLayout()

    # Create and populate student dropdown
    label_student = QLabel("Select Student:")
    students = get_all_students()
    student_ids = ["None"] + [str(student.student_id) for student in students]
    student_dropdown = QComboBox()
    student_dropdown.addItems(student_ids)

    # Create and populate course dropdown
    label_course = QLabel("Select Course:")
    courses = get_all_courses()
    course_names = ["None"] + [course.course_name for course in courses]
    course_dropdown = QComboBox()
    course_dropdown.addItems(course_names)

    # Register student button
    register_button = QPushButton("Register Student")
    register_button.clicked.connect(register_student)

    # Add widgets to layout
    layout.addWidget(label_student)
    layout.addWidget(student_dropdown)
    layout.addWidget(label_course)
    layout.addWidget(course_dropdown)
    layout.addWidget(register_button)

    # Set the layout to the tab
    tab.setLayout(layout)
