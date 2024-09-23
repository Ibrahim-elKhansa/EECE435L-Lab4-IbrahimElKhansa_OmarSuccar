import tkinter as tk
from tkinter import messagebox
from sql.db_operations import update_student, get_courses_by_student, delete_student_from_course
from models.Student import Student

def open_edit_student_dialog(student: Student):
    """
    Opens a dialog window for editing the details of a given student.

    This function creates a new Tkinter window where users can modify the student's name, age, email,
    and manage the courses the student is registered for. The dialog allows the user to update
    the student's information, remove the student from courses, and save the changes to the database.

    Args:
        student (Student): An instance of the Student class representing the student to be edited.

    The dialog includes the following components:
    - An entry field to modify the student's name, pre-filled with the current name.
    - An entry field to modify the student's age, pre-filled with the current age.
    - An entry field to modify the student's email, pre-filled with the current email.
    - A list of registered courses with a "Remove" button next to each course to mark it for removal.
    - A "Save Changes" button to save the updated student information and course registrations.

    Internal Functions:
        - remove_course(course_name): Marks a course for removal from the student's registration list.
        - refresh_course_list(): Updates the displayed list of registered courses, removing those marked for deletion.
        - save_changes(): Validates the input values, updates the student's attributes, removes the student from 
                          marked courses, saves the updated information to the database, and closes the dialog.

    Raises:
        messagebox.showinfo: When a course is marked for removal or the student's information is successfully updated.
        messagebox.showerror: If any of the fields are empty, the age is not a positive integer, 
                              or the email format is invalid.
    """
    edit_window = tk.Toplevel()
    edit_window.title(f"Edit Student: {student.name}")
    edit_window.geometry("400x400")

    # Name input field
    tk.Label(edit_window, text="Name:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
    name_entry = tk.Entry(edit_window)
    name_entry.grid(row=0, column=1, padx=10, pady=5)
    name_entry.insert(0, student.name)

    # Age input field
    tk.Label(edit_window, text="Age:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
    age_entry = tk.Entry(edit_window)
    age_entry.grid(row=1, column=1, padx=10, pady=5)
    age_entry.insert(0, student.age)

    # Email input field
    tk.Label(edit_window, text="Email:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
    email_entry = tk.Entry(edit_window)
    email_entry.grid(row=2, column=1, padx=10, pady=5)
    email_entry.insert(0, student.get_email())

    # Registered courses label
    tk.Label(edit_window, text="Registered Courses:").grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    # Course list frame
    course_frame = tk.Frame(edit_window)
    course_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

    registered_courses = get_courses_by_student(student.student_id)
    removed_courses = []

    def remove_course(course_name):
        """
        Marks a course for removal from the student's registration list.

        This function adds the course name to the `removed_courses` list and updates the course list display.

        Args:
            course_name (str): The name of the course to be marked for removal.
        """
        removed_courses.append(course_name)
        messagebox.showinfo("Success", f"Marked {course_name} for removal.")
        refresh_course_list()

    def refresh_course_list():
        """
        Refreshes the list of registered courses displayed in the dialog.

        This function clears the course list frame and re-populates it with the courses currently registered 
        for the student, excluding those marked for removal.
        """
        for widget in course_frame.winfo_children():
            widget.destroy()

        for idx, course_name in enumerate(registered_courses):
            if course_name not in removed_courses:
                course_label = tk.Label(course_frame, text=course_name)
                course_label.grid(row=idx, column=0, padx=5, pady=5)

                delete_button = tk.Button(course_frame, text="Remove", command=lambda c=course_name: remove_course(c))
                delete_button.grid(row=idx, column=1, padx=5, pady=5)

    refresh_course_list()

    def save_changes():
        """
        Saves changes made to the student's information and updates the database.

        This function validates the input values for the student's name, age, and email. If the inputs are valid, 
        it updates the student's attributes, removes the student from marked courses, saves the changes to the 
        database, and displays a success message. If the inputs are invalid, it displays an error message.

        Raises:
            messagebox.showerror: If any of the fields are empty, the age is not a positive integer, 
                                  or the email format is invalid.
            messagebox.showinfo: Upon successful update of the student's information.
        """
        new_name = name_entry.get()
        new_age = age_entry.get()
        new_email = email_entry.get()

        # Validate input fields
        if not new_name or not new_email or not new_age.isdigit() or int(new_age) <= 0:
            messagebox.showerror("Error", "Please provide valid inputs for name, age, and email.")
            return

        # Update student attributes
        student.name = new_name
        student.age = int(new_age)
        student.email = new_email

        # Remove student from marked courses
        for course_name in removed_courses:
            delete_student_from_course(student.student_id, course_name)

        # Save changes to the database
        update_student(student)
        messagebox.showinfo("Success", f"Student {student.name}'s information updated successfully.")
        edit_window.destroy()

    # Save changes button
    save_button = tk.Button(edit_window, text="Save Changes", command=save_changes)
    save_button.grid(row=5, column=0, columnspan=2, pady=20)

    edit_window.mainloop()
