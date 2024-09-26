from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QHBoxLayout, QMessageBox, QSplitter
)
from PyQt5.QtCore import Qt
from sql.db_operations import get_all_students, get_all_instructors, get_all_courses, delete_student, delete_instructor, delete_course
from ui.pyqt.list.edit_student_dialog import open_edit_student_dialog
from ui.pyqt.list.edit_instructor_dialog import open_edit_instructor_dialog
from ui.pyqt.list.edit_course_dialog import open_edit_course_dialog

class ViewRecordsForm(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """
        Initializes the UI with a splitter to separate the frames for 'Students', 'Instructors', and 'Courses'.
        Each section contains a QListWidget displaying the records, and buttons for editing or deleting the selected record.
        """

        layout = QVBoxLayout(self)

        # Create splitter to separate students, instructors, and courses sections
        splitter = QSplitter(Qt.Horizontal)

        # Create Students section
        student_layout = self.create_list_section("Students", self.edit_student, self.delete_student_entry, self.get_all_students)
        self.student_list_widget = student_layout[0]
        splitter.addWidget(student_layout[1])

        # Create Instructors section
        instructor_layout = self.create_list_section("Instructors", self.edit_instructor, self.delete_instructor_entry, self.get_all_instructors)
        self.instructor_list_widget = instructor_layout[0]
        splitter.addWidget(instructor_layout[1])

        # Create Courses section
        course_layout = self.create_list_section("Courses", self.edit_course, self.delete_course_entry, self.get_all_courses)
        self.course_list_widget = course_layout[0]
        splitter.addWidget(course_layout[1])

        layout.addWidget(splitter)

    def create_list_section(self, title, edit_func, delete_func, get_items_func):
        """
        Helper function to create a list section with a label, QListWidget, and edit/delete buttons.

        Args:
            title (str): The title of the section (e.g., "Students").
            edit_func (callable): The function to call when the 'Edit' button is clicked.
            delete_func (callable): The function to call when the 'Delete' button is clicked.
            get_items_func (callable): The function to call to populate the list with items from the database.

        Returns:
            tuple: A tuple containing the QListWidget and the QWidget that holds the section layout.
        """
        section_widget = QWidget()
        section_layout = QVBoxLayout(section_widget)

        # Section title
        section_title = QLabel(title)
        section_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        section_layout.addWidget(section_title)

        # List of records
        list_widget = QListWidget()
        section_layout.addWidget(list_widget)

        # Fetch and populate the list
        records = get_items_func()
        for record in records:
            if title == "Students":
                list_widget.addItem(f"{record.student_id}: {record.name}")
            elif title == "Instructors":
                list_widget.addItem(f"{record.instructor_id}: {record.name}")
            elif title == "Courses":
                list_widget.addItem(f"{record.course_name}")

        # Buttons for Edit and Delete
        button_layout = QHBoxLayout()
        edit_button = QPushButton("Edit")
        edit_button.clicked.connect(lambda: edit_func(list_widget))
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(lambda: delete_func(list_widget))
        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)

        section_layout.addLayout(button_layout)
        return list_widget, section_widget

    def get_all_students(self):
        return get_all_students()

    def get_all_instructors(self):
        return get_all_instructors()

    def get_all_courses(self):
        return get_all_courses()

    def edit_student(self, list_widget):
        selected_student = list_widget.currentItem().text()
        if selected_student:
            student_id = selected_student.split(":")[0]
            students = get_all_students()
            student = next((s for s in students if str(s.student_id) == student_id), None)
            if student:
                open_edit_student_dialog(student)

    def delete_student_entry(self, list_widget):
        selected_student = list_widget.currentItem().text()
        if selected_student:
            student_id = selected_student.split(":")[0]
            delete_student(int(student_id))
            list_widget.takeItem(list_widget.currentRow())
            QMessageBox.information(self, "Delete Student", f"Deleted student with ID: {student_id}")

    def edit_instructor(self, list_widget):
        selected_instructor = list_widget.currentItem().text()
        if selected_instructor:
            instructor_id = selected_instructor.split(":")[0]
            instructors = get_all_instructors()
            instructor = next((i for i in instructors if str(i.instructor_id) == instructor_id), None)
            if instructor:
                open_edit_instructor_dialog(instructor)

    def delete_instructor_entry(self, list_widget):
        selected_instructor = list_widget.currentItem().text()
        if selected_instructor:
            instructor_id = selected_instructor.split(":")[0]
            delete_instructor(int(instructor_id))
            list_widget.takeItem(list_widget.currentRow())
            QMessageBox.information(self, "Delete Instructor", f"Deleted instructor with ID: {instructor_id}")

    def edit_course(self, list_widget):
        selected_course = list_widget.currentItem().text()
        if selected_course:
            courses = get_all_courses()
            course = next((c for c in courses if c.course_name == selected_course), None)
            if course:
                open_edit_course_dialog(course)

    def delete_course_entry(self, list_widget):
        selected_course = list_widget.currentItem().text()
        if selected_course:
            delete_course(selected_course)
            list_widget.takeItem(list_widget.currentRow())
            QMessageBox.information(self, "Delete Course", f"Deleted course: {selected_course}")
