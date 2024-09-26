from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from sql.db_operations import insert_student
from ui.pyqt.student.validation import validate_email, is_unique_student_id
from models.Student import Student

def create_student_form(tab):
    """
    Creates a form for adding new students in a given PyQt5 tab.

    This function sets up a form with fields to input student details such as name, age, email, 
    and a unique student ID. It also includes a "Create Student" button that, when clicked, 
    validates the input and creates a new student record in the database.

    Args:
        tab (QWidget): The PyQt5 widget (typically a frame or tab) where the form will be created.

    The form includes the following components:
    - A text entry field for the student's name.
    - A text entry field for the student's age.
    - A text entry field for the student's email.
    - A text entry field for the student's unique ID.
    - A button labeled "Create Student" that triggers the student creation process.

    Internal Functions:
        - create_student(): Validates the input values, checks for uniqueness of the student ID, 
                            and inserts a new student into the database if all validations pass.

    Raises:
        QMessageBox: If any field is empty, the age or ID is not a positive number, 
                              the email format is invalid, or the student ID already exists.
        QMessageBox: Upon successful creation of the student record.
    """

    # Clear existing widgets from the tab layout
    for i in reversed(range(tab.layout().count())): 
        tab.layout().itemAt(i).widget().deleteLater()

    def create_student():
        """
        Handles the creation of a new student.

        This function retrieves the entered name, age, email, and student ID, validates the input, 
        and inserts a new student into the database. It also displays success or error messages 
        as appropriate and resets the form fields upon successful student creation.

        Raises:
            QMessageBox: If any field is empty, the age or ID is not a positive number, 
                                  the email format is invalid, or the student ID already exists.
            QMessageBox: Upon successful creation of the student record.
        """
        name = entry_name.text()
        age = entry_age.text()
        email = entry_email.text()
        student_id = entry_student_id.text()

        # Validate that all fields are filled
        if not name or not age or not email or not student_id:
            QMessageBox.critical(tab, "Error", "All fields are required.")
            return
        
        # Validate that age is a positive integer
        try:
            age = int(age)
            if age <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.critical(tab, "Error", "Age must be a positive number.")
            return

        # Validate that student ID is a positive integer
        try:
            student_id = int(student_id)
            if student_id <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.critical(tab, "Error", "Student ID must be a positive integer.")
            return

        # Validate email format
        if not validate_email(email):
            QMessageBox.critical(tab, "Error", "Invalid email format.")
            return

        # Check if student ID is unique
        if not is_unique_student_id(student_id):
            QMessageBox.critical(tab, "Error", "Student ID already exists.")
            return

        # Create Student object and insert it into the database
        student = Student(name=name, age=age, email=email, student_id=student_id)
        insert_student(student)

        # Show success message and reset form fields
        QMessageBox.information(tab, "Success", "Student created successfully.")
        entry_name.clear()
        entry_age.clear()
        entry_email.clear()
        entry_student_id.clear()

    # Set up the layout
    layout = QVBoxLayout()

    # Create input fields and labels
    label_name = QLabel("Student Name:")
    entry_name = QLineEdit()

    label_age = QLabel("Student Age:")
    entry_age = QLineEdit()

    label_email = QLabel("Student Email:")
    entry_email = QLineEdit()

    label_student_id = QLabel("Student ID:")
    entry_student_id = QLineEdit()

    # Create Student button
    create_button = QPushButton("Create Student")
    create_button.clicked.connect(create_student)

    # Add widgets to layout
    layout.addWidget(label_name)
    layout.addWidget(entry_name)
    layout.addWidget(label_age)
    layout.addWidget(entry_age)
    layout.addWidget(label_email)
    layout.addWidget(entry_email)
    layout.addWidget(label_student_id)
    layout.addWidget(entry_student_id)
    layout.addWidget(create_button)

    # Set the layout to the tab
    tab.setLayout(layout)
