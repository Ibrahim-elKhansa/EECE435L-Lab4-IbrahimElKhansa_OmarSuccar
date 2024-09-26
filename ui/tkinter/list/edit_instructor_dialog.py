import tkinter as tk
from tkinter import messagebox
from sql.db_operations import update_instructor
from models.Instructor import Instructor

def open_edit_instructor_dialog(instructor: Instructor):
    """
    Opens a dialog window for editing the details of a given instructor.

    This function creates a new Tkinter window where users can modify the instructor's name, age, and email.
    Upon saving changes, the updated instructor information is stored in the database.

    Args:
        instructor (Instructor): An instance of the Instructor class representing the instructor to be edited.

    The dialog includes the following components:
    - An entry field to modify the instructor's name, pre-filled with the current name.
    - An entry field to modify the instructor's age, pre-filled with the current age.
    - An entry field to modify the instructor's email, pre-filled with the current email.
    - A "Save Changes" button that triggers the instructor information update process.

    Internal Functions:
        - save_changes(): Validates the input values, updates the instructor's attributes, 
                          saves the updated information to the database, and closes the dialog.

    Raises:
        messagebox.showerror: If any of the fields are empty, the age is not a positive integer, 
                              or the email format is invalid.
        messagebox.showinfo: Upon successful update of the instructor information.
    """
    edit_window = tk.Toplevel()
    edit_window.title(f"Edit Instructor: {instructor.name}")
    edit_window.geometry("400x300")

    tk.Label(edit_window, text="Name:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
    name_entry = tk.Entry(edit_window)
    name_entry.grid(row=0, column=1, padx=10, pady=5)
    name_entry.insert(0, instructor.name)

    tk.Label(edit_window, text="Age:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
    age_entry = tk.Entry(edit_window)
    age_entry.grid(row=1, column=1, padx=10, pady=5)
    age_entry.insert(0, instructor.age)

    tk.Label(edit_window, text="Email:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
    email_entry = tk.Entry(edit_window)
    email_entry.grid(row=2, column=1, padx=10, pady=5)
    email_entry.insert(0, instructor.get_email())

    def save_changes():
        """
        Saves changes made to the instructor's information and updates the database.

        This function validates the input values for the instructor's name, age, and email. 
        If the inputs are valid, it updates the instructor's attributes, saves the changes to the database, 
        and displays a success message. If the inputs are invalid, it displays an error message.

        Raises:
            messagebox.showerror: If any of the fields are empty, the age is not a positive integer, 
                                  or the email format is invalid.
            messagebox.showinfo: Upon successful update of the instructor information.
        """
        new_name = name_entry.get()
        new_age = age_entry.get()
        new_email = email_entry.get()

        # Validate input fields
        if not new_name or not new_email or not new_age.isdigit() or int(new_age) <= 0:
            messagebox.showerror("Error", "Please provide valid inputs for name, age, and email.")
            return

        # Update instructor attributes
        instructor.name = new_name
        instructor.age = int(new_age)
        instructor.email = new_email

        # Save changes to the database
        update_instructor(instructor)
        messagebox.showinfo("Success", f"Instructor {instructor.name}'s information updated successfully.")
        edit_window.destroy()

    save_button = tk.Button(edit_window, text="Save Changes", command=save_changes)
    save_button.grid(row=3, column=0, columnspan=2, pady=20)

    edit_window.mainloop()
