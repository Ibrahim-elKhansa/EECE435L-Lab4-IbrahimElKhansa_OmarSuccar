import tkinter as tk
from tkinter import messagebox, ttk
from sql.db_operations import update_course, get_students_by_course, delete_student_from_course, get_all_instructors
from models.Course import Course

def open_edit_course_dialog(course: Course):
    """
    Opens a dialog window for editing the details of a given course.

    This function creates a new Tkinter window where users can modify the instructor assigned to the course
    and manage the students registered for it. The dialog allows the user to change the instructor via a dropdown menu 
    and remove students from the course. Upon saving changes, the updated course information is stored in the database.

    Args:
        course (Course): An instance of the Course class representing the course to be edited.

    The dialog includes the following components:
    - A dropdown menu to select or change the instructor assigned to the course.
    - A list of students registered for the course, each with a "Remove" button to mark the student for removal.
    - A "Save Changes" button to save any changes made to the course and update the database.

    Internal Functions:
        - remove_student(student_id): Marks a student for removal from the course.
        - refresh_student_list(): Updates the displayed list of registered students, removing those marked for deletion.
        - save_changes(): Updates the course information, removes marked students, and saves changes to the database.

    Raises:
        messagebox.showinfo: When a student is marked for removal or the course information is successfully updated.
        messagebox.showerror: If an error occurs during validation or database update.
    """
    edit_window = tk.Toplevel()
    edit_window.title(f"Edit Course: {course.course_name}")
    edit_window.geometry("400x400")

    tk.Label(edit_window, text="Instructor:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
    
    instructors = get_all_instructors()
    instructor_names = ["None"] + [f"{instructor.instructor_id}: {instructor.name}" for instructor in instructors]  # Add "None" at the start
    instructor_dropdown = ttk.Combobox(edit_window, values=instructor_names)
    
    if course.instructor:
        instructor_dropdown.set(f"{course.instructor.instructor_id}: {course.instructor.name}")
    else:
        instructor_dropdown.set("None")
    instructor_dropdown.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(edit_window, text="Registered Students:").grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    student_frame = tk.Frame(edit_window)
    student_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

    registered_students = get_students_by_course(course.course_name)
    removed_students = []

    def remove_student(student_id):
        """
        Marks a student for removal from the course.

        This function adds the student ID to the `removed_students` list and updates the student list display.

        Args:
            student_id (int): The ID of the student to be marked for removal.
        """
        removed_students.append(student_id)
        messagebox.showinfo("Success", f"Marked student ID {student_id} for removal.")
        refresh_student_list()

    def refresh_student_list():
        """
        Refreshes the list of registered students displayed in the dialog.

        This function clears the student list frame and re-populates it with the students currently registered 
        for the course, excluding those marked for removal.
        """
        for widget in student_frame.winfo_children():
            widget.destroy()

        for idx, student_id in enumerate(registered_students):
            if student_id not in removed_students:
                student_label = tk.Label(student_frame, text=f"Student ID: {student_id}")
                student_label.grid(row=idx, column=0, padx=5, pady=5)

                delete_button = tk.Button(student_frame, text="Remove", command=lambda s=student_id: remove_student(s))
                delete_button.grid(row=idx, column=1, padx=5, pady=5)

    refresh_student_list()

    def save_changes():
        """
        Saves changes made to the course and updates the database.

        This function updates the instructor assigned to the course, removes students marked for deletion 
        from the course, and saves the updated course information to the database.

        Raises:
            messagebox.showinfo: Upon successful update of course information.
            messagebox.showerror: If an error occurs during database update.
        """
        selected_instructor = instructor_dropdown.get()

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

        messagebox.showinfo("Success", f"Course {course.course_name}'s information updated successfully.")
        edit_window.destroy()

    save_button = tk.Button(edit_window, text="Save Changes", command=save_changes)
    save_button.grid(row=3, column=0, columnspan=2, pady=20)

    edit_window.mainloop()
