import tkinter as tk
from tkinter import messagebox
from sql.db_operations import insert_student
from ui.tkinter.student.validation import validate_email, is_unique_student_id
from models.Student import Student

def create_student_form(tab):
    """
    Creates a form for adding new students in a given Tkinter tab.

    This function sets up a form with fields to input student details such as name, age, email, 
    and a unique student ID. It also includes a "Create Student" button that, when clicked, 
    validates the input and creates a new student record in the database.

    Args:
        tab (tk.Widget): The Tkinter widget (typically a frame or tab) where the form will be created.

    The form includes the following components:
    - A text entry field for the student's name.
    - A text entry field for the student's age.
    - A text entry field for the student's email.
    - A text entry field for the student's unique ID.
    - A button labeled "Create Student" that triggers the student creation process.

    Internal Functions:
        - create_student(): Validates the input values, checks for uniqueness of the student ID, 
                            and inserts a new student into the database if all validations pass.

    Raises:
        messagebox.showerror: If any field is empty, the age or ID is not a positive number, 
                              the email format is invalid, or the student ID already exists.
        messagebox.showinfo: Upon successful creation of the student record.
    """
    # Clear existing widgets from the tab
    for widget in tab.winfo_children():
        widget.destroy()
    
    def create_student():
        """
        Handles the creation of a new student.

        This function retrieves the entered name, age, email, and student ID, validates the input, 
        and inserts a new student into the database. It also displays success or error messages 
        as appropriate and resets the form fields upon successful student creation.

        Raises:
            messagebox.showerror: If any field is empty, the age or ID is not a positive number, 
                                  the email format is invalid, or the student ID already exists.
            messagebox.showinfo: Upon successful creation of the student record.
        """
        name = entry_name.get()
        age = entry_age.get()
        email = entry_email.get()
        student_id = entry_student_id.get()

        # Validate that all fields are filled
        if not name or not age or not email or not student_id:
            messagebox.showerror("Error", "All fields are required.")
            return
        
        # Validate that age is a positive integer
        try:
            age = int(age)
            if age <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Age must be a positive number.")
            return

        # Validate that student ID is a positive integer
        try:
            student_id = int(student_id)
            if student_id <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Student ID must be a positive integer.")
            return

        # Validate email format
        if not validate_email(email):
            messagebox.showerror("Error", "Invalid email format.")
            return

        # Check if student ID is unique
        if not is_unique_student_id(student_id):
            messagebox.showerror("Error", "Student ID already exists.")
            return

        # Create Student object and insert it into the database
        student = Student(name=name, age=age, email=email, student_id=student_id)
        insert_student(student)

        # Show success message and reset form fields
        messagebox.showinfo("Success", "Student created successfully.")
        entry_name.delete(0, tk.END)
        entry_age.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_student_id.delete(0, tk.END)

    global entry_name, entry_age, entry_email, entry_student_id

    # Create input fields and labels
    tk.Label(tab, text="Student Name:").grid(row=0, column=0, padx=10, pady=10)
    entry_name = tk.Entry(tab)
    entry_name.grid(row=0, column=1, padx=10, pady=10)
    
    tk.Label(tab, text="Student Age:").grid(row=1, column=0, padx=10, pady=10)
    entry_age = tk.Entry(tab)
    entry_age.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(tab, text="Student Email:").grid(row=2, column=0, padx=10, pady=10)
    entry_email = tk.Entry(tab)
    entry_email.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(tab, text="Student ID:").grid(row=3, column=0, padx=10, pady=10)
    entry_student_id = tk.Entry(tab)
    entry_student_id.grid(row=3, column=1, padx=10, pady=10)

    # Create Student button
    tk.Button(tab, text="Create Student", command=create_student).grid(row=4, column=0, columnspan=2, pady=10)
