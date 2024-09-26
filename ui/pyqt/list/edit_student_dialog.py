from PyQt5.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QFormLayout, QGroupBox, QScrollArea, QWidget
)
from sql.db_operations import update_student, get_courses_by_student, delete_student_from_course
from models.Student import Student

def open_edit_student_dialog(student: Student):
    """
    Opens a dialog window for editing the details of a given student using PyQt5.

    This function creates a dialog where users can modify the student's name, age, email,
    and manage the courses the student is registered for. The dialog allows the user to update
    the student's information, remove the student from courses, and save the changes to the database.

    Args:
        student (Student): An instance of the Student class representing the student to be edited.

    The dialog includes:
    - An entry field to modify the student's name, pre-filled with the current name.
    - An entry field to modify the student's age, pre-filled with the current age.
    - An entry field to modify the student's email, pre-filled with the current email.
    - A list of registered courses with a "Remove" button next to each course to mark it for removal.
    - A "Save Changes" button to save the updated student information and course registrations.
    """

    dialog = QDialog()
    dialog.setWindowTitle(f"Edit Student: {student.name}")
    dialog.setGeometry(300, 200, 400, 400)

    layout = QVBoxLayout(dialog)

    # Student Name
    form_layout = QFormLayout()
    name_label = QLabel("Name:")
    name_edit = QLineEdit()
    name_edit.setText(student.name)
    form_layout.addRow(name_label, name_edit)

    # Student Age
    age_label = QLabel("Age:")
    age_edit = QLineEdit()
    age_edit.setText(str(student.age))
    form_layout.addRow(age_label, age_edit)

    # Student Email
    email_label = QLabel("Email:")
    email_edit = QLineEdit()
    email_edit.setText(student.get_email())
    form_layout.addRow(email_label, email_edit)

    layout.addLayout(form_layout)

    # Courses Section
    course_group_box = QGroupBox("Registered Courses")
    course_layout = QVBoxLayout()

    registered_courses = get_courses_by_student(student.student_id)
    removed_courses = []

    def remove_course(course_name):
        """
        Marks a course for removal from the student's registration list.

        Args:
            course_name (str): The name of the course to be marked for removal.
        """
        removed_courses.append(course_name)
        QMessageBox.information(dialog, "Success", f"Marked {course_name} for removal.")
        refresh_course_list()

    def refresh_course_list():
        """
        Refreshes the list of registered courses displayed in the dialog.
        """
        # Clear the current layout
        for i in reversed(range(course_layout.count())):
            widget_to_remove = course_layout.itemAt(i).widget()
            if widget_to_remove is not None:
                widget_to_remove.deleteLater()

        # Add courses that haven't been removed
        for course_name in registered_courses:
            if course_name not in removed_courses:
                course_row = QWidget()
                course_row_layout = QHBoxLayout()
                course_label = QLabel(course_name)
                remove_button = QPushButton("Remove")
                remove_button.clicked.connect(lambda _, c=course_name: remove_course(c))
                course_row_layout.addWidget(course_label)
                course_row_layout.addWidget(remove_button)
                course_row.setLayout(course_row_layout)
                course_layout.addWidget(course_row)

    refresh_course_list()

    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll_content = QWidget()
    scroll_content.setLayout(course_layout)
    scroll.setWidget(scroll_content)

    course_group_box.setLayout(course_layout)
    layout.addWidget(scroll)

    # Save Changes Button
    save_button = QPushButton("Save Changes")
    layout.addWidget(save_button)

    def save_changes():
        """
        Saves changes made to the student's information and updates the database.

        This function validates the input values for the student's name, age, and email. 
        If valid, it updates the student's attributes, removes the student from the marked courses, 
        and saves the changes to the database.
        """
        new_name = name_edit.text()
        new_age = age_edit.text()
        new_email = email_edit.text()

        # Validate inputs
        if not new_name or not new_email or not new_age.isdigit() or int(new_age) <= 0:
            QMessageBox.critical(dialog, "Error", "Please provide valid inputs for name, age, and email.")
            return

        # Update student information
        student.name = new_name
        student.age = int(new_age)
        student.email = new_email

        # Remove student from courses
        for course_name in removed_courses:
            delete_student_from_course(student.student_id, course_name)

        # Save the updated student information to the database
        update_student(student)
        QMessageBox.information(dialog, "Success", f"Student {student.name}'s information updated successfully.")
        dialog.accept()

    save_button.clicked.connect(save_changes)
    dialog.exec_()
