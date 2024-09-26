import tkinter as tk
from tkinter import messagebox
from sql.db_operations import insert_instructor
from ui.tkinter.student.validation import validate_email
from ui.tkinter.instructor.validation import is_unique_instructor_id
from models.Instructor import Instructor

def create_instructor_form(tab):
    """
    Creates a form for adding new instructors in a given Tkinter tab.

    This function sets up a form with fields to input instructor details such as name, age, email, 
    and a unique instructor ID. It also includes a "Create Instructor" button that, when clicked, 
    validates the input and creates a new instructor in the database.

    Args:
        tab (tk.Widget): The Tkinter widget (typically a frame or tab) where the form will be created.

    The form includes the following components:
    - A text entry field for the instructor's name.
    - A text entry field for the instructor's age.
    - A text entry field for the instructor's email.
    - A text entry field for the instructor's unique ID.
    - A button labeled "Create Instructor" that triggers the instructor creation process.

    Raises:
        messagebox.showerror: If any field is empty, the age or ID is not a positive number, 
                              the email format is invalid, or the instructor ID already exists.
    """
    # Clear existing widgets from the tab
    for widget in tab.winfo_children():
        widget.destroy()
        
    def create_instructor():
        """
        Handles the creation of a new instructor.

        This function retrieves the entered name, age, email, and instructor ID, validates the input, 
        and inserts a new instructor into the database. It also displays success or error messages 
        as appropriate and resets the form fields upon successful instructor creation.

        Raises:
            messagebox.showerror: If any field is empty, the age or ID is not a positive number, 
                                  the email format is invalid, or the instructor ID already exists.
            messagebox.showinfo: Upon successful instructor creation.
        """
        name = entry_name.get()
        age = entry_age.get()
        email = entry_email.get()
        instructor_id = entry_instructor_id.get()

        # Validate that all fields are filled
        if not name or not age or not email or not instructor_id:
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

        # Validate that instructor ID is a positive integer
        try:
            instructor_id = int(instructor_id)
            if instructor_id <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Instructor ID must be a positive integer.")
            return

        # Validate email format
        if not validate_email(email):
            messagebox.showerror("Error", "Invalid email format.")
            return

        # Check if instructor ID is unique
        if not is_unique_instructor_id(instructor_id):
            messagebox.showerror("Error", "Instructor ID already exists.")
            return

        # Create Instructor object and insert it into the database
        instructor = Instructor(name=name, age=age, email=email, instructor_id=instructor_id)
        insert_instructor(instructor)

        # Show success message and reset form fields
        messagebox.showinfo("Success", "Instructor created successfully.")
        entry_name.delete(0, tk.END)
        entry_age.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_instructor_id.delete(0, tk.END)

    # Create input fields and buttons
    global entry_name, entry_age, entry_email, entry_instructor_id

    tk.Label(tab, text="Instructor Name:").grid(row=0, column=0, padx=10, pady=10)
    entry_name = tk.Entry(tab)
    entry_name.grid(row=0, column=1, padx=10, pady=10)
    
    tk.Label(tab, text="Instructor Age:").grid(row=1, column=0, padx=10, pady=10)
    entry_age = tk.Entry(tab)
    entry_age.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(tab, text="Instructor Email:").grid(row=2, column=0, padx=10, pady=10)
    entry_email = tk.Entry(tab)
    entry_email.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(tab, text="Instructor ID:").grid(row=3, column=0, padx=10, pady=10)
    entry_instructor_id = tk.Entry(tab)
    entry_instructor_id.grid(row=3, column=1, padx=10, pady=10)

    tk.Button(tab, text="Create Instructor", command=create_instructor).grid(row=4, column=0, columnspan=2, pady=10)
