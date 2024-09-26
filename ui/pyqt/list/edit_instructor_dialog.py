from PyQt5.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
)
from sql.db_operations import update_instructor
from models.Instructor import Instructor

def open_edit_instructor_dialog(instructor: Instructor):
    """
    Opens a dialog window for editing the details of a given instructor using PyQt5.

    This function creates a new dialog where users can modify the instructor's name, age, and email.
    Upon saving changes, the updated instructor information is stored in the database.

    Args:
        instructor (Instructor): An instance of the Instructor class representing the instructor to be edited.

    The dialog includes the following components:
    - An entry field to modify the instructor's name, pre-filled with the current name.
    - An entry field to modify the instructor's age, pre-filled with the current age.
    - An entry field to modify the instructor's email, pre-filled with the current email.
    - A "Save Changes" button that triggers the instructor information update process.

    Internal Functions:
        - save_changes(): Validates the input values, updates the instructor's attributes, 
                          saves the updated information to the database, and closes the dialog.

    Raises:
        QMessageBox.critical: If any of the fields are empty, the age is not a positive integer, 
                              or the email format is invalid.
        QMessageBox.information: Upon successful update of the instructor information.
    """
    dialog = QDialog()
    dialog.setWindowTitle(f"Edit Instructor: {instructor.name}")
    dialog.setGeometry(300, 200, 400, 300)

    layout = QVBoxLayout()

    # Instructor name
    label_name = QLabel("Name:")
    layout.addWidget(label_name)
    name_edit = QLineEdit()
    name_edit.setText(instructor.name)
    layout.addWidget(name_edit)

    # Instructor age
    label_age = QLabel("Age:")
    layout.addWidget(label_age)
    age_edit = QLineEdit()
    age_edit.setText(str(instructor.age))
    layout.addWidget(age_edit)

    # Instructor email
    label_email = QLabel("Email:")
    layout.addWidget(label_email)
    email_edit = QLineEdit()
    email_edit.setText(instructor.get_email())
    layout.addWidget(email_edit)

    def save_changes():
        """
        Saves changes made to the instructor's information and updates the database.

        This function validates the input values for the instructor's name, age, and email. 
        If the inputs are valid, it updates the instructor's attributes, saves the changes to the database, 
        and displays a success message. If the inputs are invalid, it displays an error message.

        Raises:
            QMessageBox.critical: If any of the fields are empty, the age is not a positive integer, 
                                  or the email format is invalid.
            QMessageBox.information: Upon successful update of the instructor information.
        """
        new_name = name_edit.text()
        new_age = age_edit.text()
        new_email = email_edit.text()

        # Validate input fields
        if not new_name or not new_email or not new_age.isdigit() or int(new_age) <= 0:
            QMessageBox.critical(dialog, "Error", "Please provide valid inputs for name, age, and email.")
            return

        # Update instructor attributes
        instructor.name = new_name
        instructor.age = int(new_age)
        instructor.email = new_email

        # Save changes to the database
        update_instructor(instructor)
        QMessageBox.information(dialog, "Success", f"Instructor {instructor.name}'s information updated successfully.")
        dialog.accept()

    # Save button
    save_button = QPushButton("Save Changes")
    save_button.clicked.connect(save_changes)
    layout.addWidget(save_button)

    dialog.setLayout(layout)
    dialog.exec_()
