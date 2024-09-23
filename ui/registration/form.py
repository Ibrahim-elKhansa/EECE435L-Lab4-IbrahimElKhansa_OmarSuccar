import tkinter as tk
from tkinter import messagebox, ttk
from sql.db_operations import get_all_students, get_all_courses, register_student_for_course, is_student_registered_for_course

def create_registration_form(tab):
    """
    Creates a form for registering students for courses in a given Tkinter tab.

    This function sets up a registration form with dropdown menus for selecting a student and a course.
    It includes a "Register Student" button that, when clicked, validates the selection and registers 
    the student for the chosen course in the database.

    Args:
        tab (tk.Widget): The Tkinter widget (typically a frame or tab) where the form will be created.

    The form includes the following components:
    - A dropdown menu to select a student from the list of all students in the database.
    - A dropdown menu to select a course from the list of all courses in the database.
    - A "Register Student" button that triggers the student registration process.

    Internal Functions:
        - register_student(): Validates the selected student and course, checks if the student is 
                              already registered for the course, and registers the student if not.

    Raises:
        messagebox.showerror: If either student or course is not selected, or if the student is already 
                              registered for the selected course.
        messagebox.showinfo: Upon successful registration of the student for the selected course.
    """
    # Clear existing widgets from the tab
    for widget in tab.winfo_children():
        widget.destroy()
        
    def register_student():
        """
        Registers the selected student for the selected course.

        This function retrieves the student ID and course name from the dropdown menus, checks if the 
        student is already registered for the course, and registers the student if they are not. 
        It displays an error message if either selection is missing or if the student is already 
        registered for the course, and a success message upon successful registration.

        Raises:
            messagebox.showerror: If either student or course is not selected, or if the student is already 
                                  registered for the selected course.
            messagebox.showinfo: Upon successful registration of the student for the selected course.
        """
        student_id = student_dropdown.get()
        course_name = course_dropdown.get()

        # Validate that both student and course are selected
        if student_id == "None" or course_name == "None":
            messagebox.showerror("Error", "Please select both a student and a course.")
            return

        # Check if student is already registered for the course
        if is_student_registered_for_course(int(student_id), course_name):
            messagebox.showerror("Error", "Student is already registered for this course.")
            return

        # Register student for the course
        register_student_for_course(int(student_id), course_name)
        messagebox.showinfo("Success", "Student registered for the course successfully.")

        # Reset dropdown selections
        student_dropdown.set("None")
        course_dropdown.set("None")

    global student_dropdown, course_dropdown

    # Create and populate student dropdown
    tk.Label(tab, text="Select Student:").grid(row=0, column=0, padx=10, pady=10)
    students = get_all_students()
    student_ids = [str(student.student_id) for student in students]
    student_ids.insert(0, "None")
    student_dropdown = ttk.Combobox(tab, values=student_ids)
    student_dropdown.grid(row=0, column=1, padx=10, pady=10)
    student_dropdown.set("None")

    # Create and populate course dropdown
    tk.Label(tab, text="Select Course:").grid(row=1, column=0, padx=10, pady=10)
    courses = get_all_courses()
    course_names = [course.course_name for course in courses]
    course_names.insert(0, "None")
    course_dropdown = ttk.Combobox(tab, values=course_names)
    course_dropdown.grid(row=1, column=1, padx=10, pady=10)
    course_dropdown.set("None")

    # Register student button
    tk.Button(tab, text="Register Student", command=register_student).grid(row=2, column=0, columnspan=2, pady=10)
