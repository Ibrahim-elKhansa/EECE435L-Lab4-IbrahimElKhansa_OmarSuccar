import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox, QTableWidget, QTableWidgetItem
)
import csv
from sql.db_operations import get_all_students, get_all_instructors, get_all_courses, get_students_by_course
from ui.pyqt.student.form import create_student_form
from ui.pyqt.instructor.form import create_instructor_form
from ui.pyqt.course.form import create_course_form
from ui.pyqt.registration.form import create_registration_form
from ui.pyqt.list.form import create_view_records_form

class SchoolManagementSystem(QMainWindow):
    """
    Main window for the School Management System using PyQt5.

    This window contains tabs for managing students, instructors, courses, and student registrations.
    It also includes a feature to export data to CSV files.
    """
    def __init__(self):
        super().__init__()

        self.setWindowTitle("School Management System")
        self.setGeometry(100, 100, 900, 650)

        # Create the tab widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Create tabs for managing students, instructors, courses, and registrations
        self.tab_create_student = QWidget()
        self.tab_create_instructor = QWidget()
        self.tab_create_course = QWidget()
        self.tab_register_student = QWidget()
        self.tab_view_records = QWidget()

        # Add tabs to the tab widget
        self.tabs.addTab(self.tab_create_student, "Create Student")
        self.tabs.addTab(self.tab_create_instructor, "Create Instructor")
        self.tabs.addTab(self.tab_create_course, "Create Course")
        self.tabs.addTab(self.tab_register_student, "Register Student")
        self.tabs.addTab(self.tab_view_records, "View Records")

        # Load forms when tabs change
        self.tabs.currentChanged.connect(self.on_tab_change)

        # Load the first tab (Create Student) initially
        self.create_student_tab()

        # Export button to export data to CSV files
        self.export_button = QPushButton("Export Data", self)
        self.export_button.clicked.connect(self.export_data)
        self.statusBar().addPermanentWidget(self.export_button)

    def on_tab_change(self, index):
        """
        Load the appropriate form or view when a tab is selected.
        """
        if index == 0:
            self.create_student_tab()
        elif index == 1:
            self.create_instructor_tab()
        elif index == 2:
            self.create_course_tab()
        elif index == 3:
            self.create_registration_tab()
        elif index == 4:
            self.create_view_records_tab()

    def create_student_tab(self):
        """
        Create and load the student form in the "Create Student" tab.
        """
        layout = QVBoxLayout()
        label = QLabel("Create a new student")
        layout.addWidget(label)

        # Add custom student form
        create_student_form(self.tab_create_student, layout)

        self.tab_create_student.setLayout(layout)

    def create_instructor_tab(self):
        """
        Create and load the instructor form in the "Create Instructor" tab.
        """
        layout = QVBoxLayout()
        label = QLabel("Create a new instructor")
        layout.addWidget(label)

        # Add custom instructor form
        create_instructor_form(self.tab_create_instructor, layout)

        self.tab_create_instructor.setLayout(layout)

    def create_course_tab(self):
        """
        Create and load the course form in the "Create Course" tab.
        """
        layout = QVBoxLayout()
        label = QLabel("Create a new course")
        layout.addWidget(label)

        create_course_form(self.tab_create_course, layout)

        self.tab_create_course.setLayout(layout)

    def create_registration_tab(self):
        """
        Create and load the registration form in the "Register Student" tab.
        """
        layout = QVBoxLayout()
        label = QLabel("Register a student for a course")
        layout.addWidget(label)

        create_registration_form(self.tab_register_student, layout)

        self.tab_register_student.setLayout(layout)

    def create_view_records_tab(self):
        """
        Create and load the record viewing form in the "View Records" tab.
        """
        layout = QVBoxLayout()
        label = QLabel("View records of students, instructors, and courses")
        layout.addWidget(label)

        create_view_records_form(self.tab_view_records, layout)

        self.tab_view_records.setLayout(layout)

    def export_data(self):
        """
        Export student, instructor, course, and student-course data to CSV files.
        """
        export_path = QFileDialog.getExistingDirectory(self, "Select Export Directory")

        if not export_path:
            return

        try:
            # Export students data
            with open(f'{export_path}/students.csv', mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Student ID', 'Name', 'Age', 'Email'])
                students = get_all_students()
                for student in students:
                    writer.writerow([student.student_id, student.name, student.age, student.get_email()])

            # Export instructors data
            with open(f'{export_path}/instructors.csv', mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Instructor ID', 'Name', 'Age', 'Email'])
                instructors = get_all_instructors()
                for instructor in instructors:
                    writer.writerow([instructor.instructor_id, instructor.name, instructor.age, instructor.get_email()])

            # Export courses data
            with open(f'{export_path}/courses.csv', mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Course Name', 'Instructor ID'])
                courses = get_all_courses()
                for course in courses:
                    instructor_id = course.instructor.instructor_id if course.instructor else 'None'
                    writer.writerow([course.course_name, instructor_id])

            # Export student-courses data
            with open(f'{export_path}/student_courses.csv', mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Student ID', 'Course Name'])
                courses = get_all_courses()
                for course in courses:
                    registered_students = get_students_by_course(course.course_name)
                    for student_id in registered_students:
                        writer.writerow([student_id, course.course_name])

            QMessageBox.information(self, "Export Data", "Data exported successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Export Data", f"Error exporting data: {e}")

def main():
    """
    Entry point for the School Management System application.
    """
    app = QApplication(sys.argv)
    window = SchoolManagementSystem()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
