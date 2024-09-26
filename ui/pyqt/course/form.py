from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox
from sql.db_operations import insert_course, get_all_instructors
from ui.pyqt.course.validation import is_unique_course_name
from models.Course import Course

def create_course_form(tab):
    """
    Creates a form for adding new courses in a given PyQt5 widget tab.

    This function sets up a form with fields to input a course name and select an instructor 
    from a dropdown menu. The form also includes a "Create Course" button that, when clicked, 
    validates the input and creates a new course in the database.

    Args:
        tab (QWidget): The PyQt5 widget (typically a QWidget or tab) where the form will be created.

    The form includes the following components:
    - A text entry field for the course name.
    - A dropdown menu populated with instructor IDs from the database.
    - A button labeled "Create Course" that triggers the course creation process.
    
    The function also clears any existing widgets in the tab before creating the form.
    
    The internal `create_course` function:
        - Retrieves the entered course name and selected instructor ID.
        - Validates that the course name is not empty and is unique.
        - Creates a `Course` object and inserts it into the database using `insert_course`.
        - Displays appropriate success or error messages.
        - Resets the form fields after successful creation.
    """
    # Clear existing widgets from the tab
    for i in reversed(range(tab.layout().count())): 
        tab.layout().itemAt(i).widget().deleteLater()

    def create_course():
        """
        Handles the creation of a new course.

        This function retrieves the entered course name and selected instructor ID,
        validates the input, and inserts a new course into the database. It also
        displays success or error messages as appropriate and resets the form fields
        upon successful course creation.
        """
        course_name = entry_course_name.text()
        instructor_id = instructor_dropdown.currentText()

        # Validate course name
        if not course_name:
            QMessageBox.critical(tab, "Error", "Course name is required.")
            return

        # Check if course name is unique
        if not is_unique_course_name(course_name):
            QMessageBox.critical(tab, "Error", "Course name already exists.")
            return

        # Get instructor object if an instructor is selected
        instructor = None
        if instructor_id != "None":
            instructor = next((inst for inst in get_all_instructors() if inst.instructor_id == int(instructor_id)), None)

        # Create Course object and insert it into the database
        course = Course(course_name=course_name, instructor=instructor)
        insert_course(course)

        # Show success message and reset form fields
        QMessageBox.information(tab, "Success", "Course created successfully.")
        entry_course_name.clear()
        instructor_dropdown.setCurrentIndex(0)

    # Set up the layout
    layout = QVBoxLayout()

    # Create input fields and buttons
    label_course_name = QLabel("Course Name:")
    entry_course_name = QLineEdit()

    label_instructor = QLabel("Instructor:")
    instructors = get_all_instructors()
    instructor_ids = ["None"] + [str(inst.instructor_id) for inst in instructors]
    instructor_dropdown = QComboBox()
    instructor_dropdown.addItems(instructor_ids)

    create_course_button = QPushButton("Create Course")
    create_course_button.clicked.connect(create_course)

    # Add widgets to layout
    layout.addWidget(label_course_name)
    layout.addWidget(entry_course_name)
    layout.addWidget(label_instructor)
    layout.addWidget(instructor_dropdown)
    layout.addWidget(create_course_button)

    # Set the layout to the tab
    tab.setLayout(layout)
