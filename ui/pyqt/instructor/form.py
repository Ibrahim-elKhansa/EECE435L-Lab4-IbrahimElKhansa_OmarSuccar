from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from sql.db_operations import insert_instructor
from ui.pyqt.student.validation import validate_email
from ui.pyqt.instructor.validation import is_unique_instructor_id
from models.Instructor import Instructor

def create_instructor_form(tab):
    """
    Creates a form for adding new instructors in a given PyQt5 tab.

    This function sets up a form with fields to input instructor details such as name, age, email, 
    and a unique instructor ID. It also includes a "Create Instructor" button that, when clicked, 
    validates the input and creates a new instructor in the database.

    Args:
        tab (QWidget): The PyQt5 widget (typically a tab or frame) where the form will be created.

    The form includes the following components:
    - A text entry field for the instructor's name.
    - A text entry field for the instructor's age.
    - A text entry field for the instructor's email.
    - A text entry field for the instructor's unique ID.
    - A button labeled "Create Instructor" that triggers the instructor creation process.

    Raises:
        QMessageBox: If any field is empty, the age or ID is not a positive number, 
                     the email format is invalid, or the instructor ID already exists.
    """

    # Clear existing widgets from the tab layout
    for i in reversed(range(tab.layout().count())): 
        tab.layout().itemAt(i).widget().deleteLater()

    def create_instructor():
        """
        Handles the creation of a new instructor.

        This function retrieves the entered name, age, email, and instructor ID, validates the input, 
        and inserts a new instructor into the database. It also displays success or error messages 
        as appropriate and resets the form fields upon successful instructor creation.
        """
        name = entry_name.text()
        age = entry_age.text()
        email = entry_email.text()
        instructor_id = entry_instructor_id.text()

        # Validate that all fields are filled
        if not name or not age or not email or not instructor_id:
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

        # Validate that instructor ID is a positive integer
        try:
            instructor_id = int(instructor_id)
            if instructor_id <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.critical(tab, "Error", "Instructor ID must be a positive integer.")
            return

        # Validate email format
        if not validate_email(email):
            QMessageBox.critical(tab, "Error", "Invalid email format.")
            return

        # Check if instructor ID is unique
        if not is_unique_instructor_id(instructor_id):
            QMessageBox.critical(tab, "Error", "Instructor ID already exists.")
            return

        # Create Instructor object and insert it into the database
        instructor = Instructor(name=name, age=age, email=email, instructor_id=instructor_id)
        insert_instructor(instructor)

        # Show success message and reset form fields
        QMessageBox.information(tab, "Success", "Instructor created successfully.")
        entry_name.clear()
        entry_age.clear()
        entry_email.clear()
        entry_instructor_id.clear()

    # Set up the layout
    layout = QVBoxLayout()

    # Create input fields and buttons
    label_name = QLabel("Instructor Name:")
    entry_name = QLineEdit()

    label_age = QLabel("Instructor Age:")
    entry_age = QLineEdit()

    label_email = QLabel("Instructor Email:")
    entry_email = QLineEdit()

    label_instructor_id = QLabel("Instructor ID:")
    entry_instructor_id = QLineEdit()

    create_instructor_button = QPushButton("Create Instructor")
    create_instructor_button.clicked.connect(create_instructor)

    # Add widgets to layout
    layout.addWidget(label_name)
    layout.addWidget(entry_name)
    layout.addWidget(label_age)
    layout.addWidget(entry_age)
    layout.addWidget(label_email)
    layout.addWidget(entry_email)
    layout.addWidget(label_instructor_id)
    layout.addWidget(entry_instructor_id)
    layout.addWidget(create_instructor_button)

    # Set the layout to the tab
    tab.setLayout(layout)
