import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
from sql.db_operations import get_all_students, get_all_instructors, get_all_courses, get_students_by_course
from ui.tkinter.student.form import create_student_form
from ui.tkinter.instructor.form import create_instructor_form
from ui.tkinter.course.form import create_course_form
from ui.tkinter.registration.form import create_registration_form
from ui.tkinter.list.form import create_view_records_form

def main():
    """
    Initializes and runs the School Management System application.

    This function sets up the main GUI window using Tkinter with a tabbed interface for managing students, 
    instructors, courses, and registrations. It also includes functionality to export all data to CSV files.

    GUI Components:
        - Notebook Tabs:
            - "Create Student": Opens a form to add new students.
            - "Create Instructor": Opens a form to add new instructors.
            - "Create Course": Opens a form to add new courses.
            - "Register Student": Opens a form to register students for courses.
            - "View Records": Displays lists of students, instructors, and courses, with options to edit or delete records.
        
        - Export Button:
            - "Export Data": Exports all students, instructors, courses, and student-course registrations to CSV files.

    Functions:
        - on_tab_change(event): Handles tab selection changes to load the appropriate form or view.
        - export_data(): Exports the student, instructor, course, and registration data to CSV files in the selected directory.

    Raises:
        messagebox.showerror: If an error occurs during data export.
        messagebox.showinfo: Upon successful data export.

    Note:
        The application starts with the "Create Student" form loaded in the "Create Student" tab by default.
    """
    root = tk.Tk()
    root.title("School Management System")
    root.geometry("900x650")

    # Create Notebook widget for tabbed interface
    notebook = ttk.Notebook(root)

    # Create frames for each tab
    tab_create_student = ttk.Frame(notebook)
    tab_create_instructor = ttk.Frame(notebook)
    tab_create_course = ttk.Frame(notebook)
    tab_register_student_course = ttk.Frame(notebook)
    tab_view_records = ttk.Frame(notebook)

    # Add tabs to the notebook
    notebook.add(tab_create_student, text="Create Student")
    notebook.add(tab_create_instructor, text="Create Instructor")
    notebook.add(tab_create_course, text="Create Course")
    notebook.add(tab_register_student_course, text="Register Student")
    notebook.add(tab_view_records, text="View Records")
    notebook.pack(expand=True, fill='both')

    def on_tab_change(event):
        """
        Handles tab change events to load the appropriate form or view.

        Args:
            event (tk.Event): The event object triggered by tab change.
        """
        selected_tab = event.widget.select()
        tab_text = notebook.tab(selected_tab, "text")

        if tab_text == "Create Student":
            create_student_form(tab_create_student)
        elif tab_text == "Create Instructor":
            create_instructor_form(tab_create_instructor)
        elif tab_text == "Create Course":
            create_course_form(tab_create_course)
        elif tab_text == "Register Student":
            create_registration_form(tab_register_student_course)
        elif tab_text == "View Records":
            create_view_records_form(tab_view_records)

    notebook.bind("<<NotebookTabChanged>>", on_tab_change)

    # Initialize the "Create Student" form in the default tab
    create_student_form(tab_create_student)

    def export_data():
        """
        Exports student, instructor, course, and student-course data to CSV files in the selected directory.

        This function prompts the user to select a directory, then exports the data to four CSV files:
        'students.csv', 'instructors.csv', 'courses.csv', and 'student_courses.csv'.
        
        Raises:
            messagebox.showerror: If an error occurs during data export.
            messagebox.showinfo: Upon successful data export.
        """
        export_path = filedialog.askdirectory(title="Select Export Directory")
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

            messagebox.showinfo("Export Data", "Data exported successfully!")
        except Exception as e:
            messagebox.showerror("Export Data", f"Error exporting data: {e}")

    # Export Data button
    export_button = ttk.Button(root, text="Export Data", command=export_data)
    export_button.pack(pady=10, side=tk.BOTTOM)

    root.mainloop()

if __name__ == "__main__":
    main()
