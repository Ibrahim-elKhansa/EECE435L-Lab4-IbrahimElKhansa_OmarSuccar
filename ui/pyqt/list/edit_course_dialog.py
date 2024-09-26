from PyQt5.QtWidgets import (
    QDialog, QLabel, QComboBox, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QMessageBox, QListWidgetItem
)
from sql.db_operations import update_course, get_students_by_course, delete_student_from_course, get_all_instructors
from models.Course import Course

def open_edit_course_dialog(course: Course):
    """
    Opens a dialog window for editing the details of a given course using PyQt5.

    This function creates a new dialog where users can modify the instructor assigned to the course
    and manage the students registered for it. The dialog allows the user to change the instructor via a dropdown menu 
    and remove students from the course. Upon saving changes, the updated course information is stored in the database.

    Args:
        course (Course): An instance of the Course class representing the course to be edited.

    The dialog includes the following components:
    - A dropdown menu to select or change the instructor assigned to the course.
    - A list of students registered for the course, each with a "Remove" button to mark the student for removal.
    - A "Save Changes" button to save any changes made to the course and update the database.

    Raises:
        QMessageBox.information: When a student is marked for removal or the course information is successfully updated.
        QMessageBox.critical: If an error occurs during validation or database update.
    """
    dialog = QDialog()
    dialog.setWindowTitle(f"Edit Course: {course.course_name}")
    dialog.setGeometry(300, 200, 400, 400)

    layout = QVBoxLayout()

    # Instructor label and dropdown
    label_instructor = QLabel("Instructor:")
    layout.addWidget(label_instructor)

    instructors = get_all_instructors()
    instructor_names = ["None"] + [f"{instructor.instructor_id}: {instructor.name}" for instructor in instructors]
    instructor_dropdown = QComboBox()
    instructor_dropdown.addItems(instructor_names)

    if course.instructor:
        instructor_dropdown.setCurrentText(f"{course.instructor.instructor_id}: {course.instructor.name}")
    else:
        instructor_dropdown.setCurrentText("None")
    layout.addWidget(instructor_dropdown)

    # Student list
    label_students = QLabel("Registered Students:")
    layout.addWidget(label_students)

    student_list_widget = QListWidget()
    registered_students = get_students_by_course(course.course_name)
    removed_students = []

    def remove_student(student_id):
        """
        Marks a student for removal from the course and refreshes the student list.
        """
        removed_students.append(student_id)
        QMessageBox.information(dialog, "Success", f"Marked student ID {student_id} for removal.")
        refresh_student_list()

    def refresh_student_list():
        """
        Refreshes the list of registered students displayed in the dialog.
        """
        student_list_widget.clear()

        for student_id in registered_students:
            if student_id not in removed_students:
                item = QListWidgetItem(f"Student ID: {student_id}")
                remove_button = QPushButton("Remove")
                remove_button.clicked.connect(lambda _, s=student_id: remove_student(s))

                list_item_layout = QHBoxLayout()
                list_item_layout.addWidget(QLabel(f"Student ID: {student_id}"))
                list_item_layout.addWidget(remove_button)

                student_list_widget.addItem(item)

    refresh_student_list()
    layout.addWidget(student_list_widget)

    def save_changes():
        """
        Saves changes made to the course and updates the database.
        """
        selected_instructor = instructor_dropdown.currentText()

        if selected_instructor == "None":
            course.instructor = None
        else:
            instructor_id = selected_instructor.split(":")[0]
            selected_instructor_obj = next((inst for inst in instructors if str(inst.instructor_id) == instructor_id), None)

            if selected_instructor_obj:
                course.instructor = selected_instructor_obj

        for student_id in removed_students:
            delete_student_from_course(student_id, course.course_name)

        update_course(course)

        QMessageBox.information(dialog, "Success", f"Course {course.course_name}'s information updated successfully.")
        dialog.accept()

    save_button = QPushButton("Save Changes")
    save_button.clicked.connect(save_changes)
    layout.addWidget(save_button)

    dialog.setLayout(layout)
    dialog.exec_()
