import tkinter as tk
from tkinter import ttk, messagebox
from sql.db_operations import get_all_students, get_all_instructors, get_all_courses, delete_student, delete_instructor, delete_course
from ui.list.edit_student_dialog import open_edit_student_dialog
from ui.list.edit_instructor_dialog import open_edit_instructor_dialog
from ui.list.edit_course_dialog import open_edit_course_dialog

def create_view_records_form(tab):
    """
    Creates a form for viewing and managing records of students, instructors, and courses in a given Tkinter tab.

    This function sets up a multi-pane window with separate sections for viewing, editing, and deleting records 
    from the 'students', 'instructors', and 'courses' tables in the database. Each section includes a listbox 
    displaying the records and buttons for editing and deleting the selected record.

    Args:
        tab (tk.Widget): The Tkinter widget (typically a frame or tab) where the form will be created.

    The form includes the following components:
    - A PanedWindow containing three frames for 'Students', 'Instructors', and 'Courses'.
    - Each frame contains a Listbox displaying the respective records and buttons to edit or delete the selected record.

    Internal Functions:
        - edit_student(student_list): Opens a dialog to edit the selected student.
        - delete_student_entry(student_list): Deletes the selected student from the database and updates the listbox.
        - edit_instructor(instructor_list): Opens a dialog to edit the selected instructor.
        - delete_instructor_entry(instructor_list): Deletes the selected instructor from the database and updates the listbox.
        - edit_course(course_list): Opens a dialog to edit the selected course.
        - delete_course_entry(course_list): Deletes the selected course from the database and updates the listbox.

    Raises:
        messagebox.showinfo: Upon successful deletion of a record.
        messagebox.showerror: If an error occurs during deletion or when no record is selected.
    """
    # Clear existing widgets from the tab
    for widget in tab.winfo_children():
        widget.destroy()
        
    # Create PanedWindow for separating the frames
    paned_window = tk.PanedWindow(tab, orient=tk.HORIZONTAL)
    paned_window.pack(fill=tk.BOTH, expand=True)

    # Student frame and listbox
    student_frame = ttk.Frame(paned_window, relief=tk.SUNKEN, borderwidth=1)
    paned_window.add(student_frame)
    tk.Label(student_frame, text="Students", font=('Arial', 14)).pack(anchor=tk.N, pady=10)
    student_list = tk.Listbox(student_frame)
    student_list.pack(fill=tk.BOTH, expand=True)
    students = get_all_students()
    for student in students:
        student_list.insert(tk.END, f"{student.student_id}: {student.name}")
    student_button_frame = ttk.Frame(student_frame)
    student_button_frame.pack(fill=tk.X, pady=5)
    ttk.Button(student_button_frame, text="Edit", command=lambda: edit_student(student_list)).pack(side=tk.LEFT, padx=5)
    ttk.Button(student_button_frame, text="Delete", command=lambda: delete_student_entry(student_list)).pack(side=tk.LEFT, padx=5)

    # Instructor frame and listbox
    instructor_frame = ttk.Frame(paned_window, relief=tk.SUNKEN, borderwidth=1)
    paned_window.add(instructor_frame)
    tk.Label(instructor_frame, text="Instructors", font=('Arial', 14)).pack(anchor=tk.N, pady=10)
    instructor_list = tk.Listbox(instructor_frame)
    instructor_list.pack(fill=tk.BOTH, expand=True)
    instructors = get_all_instructors()
    for instructor in instructors:
        instructor_list.insert(tk.END, f"{instructor.instructor_id}: {instructor.name}")
    instructor_button_frame = ttk.Frame(instructor_frame)
    instructor_button_frame.pack(fill=tk.X, pady=5)
    ttk.Button(instructor_button_frame, text="Edit", command=lambda: edit_instructor(instructor_list)).pack(side=tk.LEFT, padx=5)
    ttk.Button(instructor_button_frame, text="Delete", command=lambda: delete_instructor_entry(instructor_list)).pack(side=tk.LEFT, padx=5)

    # Course frame and listbox
    course_frame = ttk.Frame(paned_window, relief=tk.SUNKEN, borderwidth=1)
    paned_window.add(course_frame)
    tk.Label(course_frame, text="Courses", font=('Arial', 14)).pack(anchor=tk.N, pady=10)
    course_list = tk.Listbox(course_frame)
    course_list.pack(fill=tk.BOTH, expand=True)
    courses = get_all_courses()
    for course in courses:
        course_list.insert(tk.END, f"{course.course_name}")
    course_button_frame = ttk.Frame(course_frame)
    course_button_frame.pack(fill=tk.X, pady=5)
    ttk.Button(course_button_frame, text="Edit", command=lambda: edit_course(course_list)).pack(side=tk.LEFT, padx=5)
    ttk.Button(course_button_frame, text="Delete", command=lambda: delete_course_entry(course_list)).pack(side=tk.LEFT, padx=5)

    # Internal function to edit a selected student
    def edit_student(student_list):
        selected_student = student_list.get(tk.ACTIVE)
        if selected_student:
            student_id = selected_student.split(":")[0]
            students = get_all_students()
            student = next((s for s in students if str(s.student_id) == student_id), None)
            if student:
                open_edit_student_dialog(student)

    # Internal function to delete a selected student
    def delete_student_entry(student_list):
        selected_student = student_list.get(tk.ACTIVE)
        if selected_student:
            student_id = selected_student.split(":")[0]
            delete_student(int(student_id))
            student_list.delete(tk.ACTIVE)
            messagebox.showinfo("Delete Student", f"Deleted student with ID: {student_id}")

    # Internal function to edit a selected instructor
    def edit_instructor(instructor_list):
        selected_instructor = instructor_list.get(tk.ACTIVE)
        if selected_instructor:
            instructor_id = selected_instructor.split(":")[0]
            instructors = get_all_instructors()
            instructor = next((i for i in instructors if str(i.instructor_id) == instructor_id), None)
            if instructor:
                open_edit_instructor_dialog(instructor)

    # Internal function to delete a selected instructor
    def delete_instructor_entry(instructor_list):
        selected_instructor = instructor_list.get(tk.ACTIVE)
        if selected_instructor:
            instructor_id = selected_instructor.split(":")[0]
            delete_instructor(int(instructor_id))
            instructor_list.delete(tk.ACTIVE)
            messagebox.showinfo("Delete Instructor", f"Deleted instructor with ID: {instructor_id}")

    # Internal function to edit a selected course
    def edit_course(course_list):
        selected_course = course_list.get(tk.ACTIVE)
        if selected_course:
            course_name = selected_course
            courses = get_all_courses()
            course = next((c for c in courses if c.course_name == course_name), None)
            if course:
                open_edit_course_dialog(course)

    # Internal function to delete a selected course
    def delete_course_entry(course_list):
        selected_course = course_list.get(tk.ACTIVE)
        if selected_course:
            course_name = selected_course
            delete_course(course_name)
            course_list.delete(tk.ACTIVE)
            messagebox.showinfo("Delete Course", f"Deleted course: {course_name}")
