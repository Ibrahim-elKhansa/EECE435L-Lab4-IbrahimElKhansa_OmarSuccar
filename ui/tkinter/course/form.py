import tkinter as tk
from tkinter import messagebox, ttk
from sql.db_operations import insert_course, get_all_instructors
from ui.tkinter.course.validation import is_unique_course_name
from models.Course import Course

def create_course_form(tab):
    """
    Creates a form for adding new courses in a given Tkinter tab.

    This function sets up a form with fields to input a course name and select an instructor 
    from a dropdown menu. The form also includes a "Create Course" button that, when clicked, 
    validates the input and creates a new course in the database.

    Args:
        tab (tk.Widget): The Tkinter widget (typically a frame or tab) where the form will be created.

    The form includes the following components:
    - A text entry field for the course name.
    - A dropdown menu populated with instructor IDs from the database.
    - A button labeled "Create Course" that triggers the course creation process.
    
    The function also clears any existing widgets in the tab before creating the form.
    
    The internal `create_course` function:
        - Retrieves the entered course name and selected instructor ID.
        - Validates that the course name is not empty and is unique.
        - Creates a `Course` object and inserts it into the database using `insert_course`.
        - Displays appropriate success or error messages.
        - Resets the form fields after successful creation.

    Raises:
        messagebox.showerror: If the course name is empty or already exists in the database.
    """

    # Clear existing widgets from the tab
    for widget in tab.winfo_children():
        widget.destroy()
        
    def create_course():
        """
        Handles the creation of a new course.

        This function retrieves the entered course name and selected instructor ID,
        validates the input, and inserts a new course into the database. It also
        displays success or error messages as appropriate and resets the form fields
        upon successful course creation.

        Raises:
            messagebox.showerror: If the course name is empty or already exists in the database.
            messagebox.showinfo: Upon successful course creation.
        """
        course_name = entry_course_name.get()
        instructor_id = instructor_dropdown.get()

        # Validate course name
        if not course_name:
            messagebox.showerror("Error", "Course name is required.")
            return

        # Check if course name is unique
        if not is_unique_course_name(course_name):
            messagebox.showerror("Error", "Course name already exists.")
            return

        # Get instructor object if an instructor is selected
        instructor = None
        if instructor_id != "None":
            instructor = next((inst for inst in get_all_instructors() if inst.instructor_id == int(instructor_id)), None)

        # Create Course object and insert it into the database
        course = Course(course_name=course_name, instructor=instructor)
        insert_course(course)

        # Show success message and reset form fields
        messagebox.showinfo("Success", "Course created successfully.")
        entry_course_name.delete(0, tk.END)
        instructor_dropdown.set("None")

    # Create input fields and buttons
    global entry_course_name, instructor_dropdown

    tk.Label(tab, text="Course Name:").grid(row=0, column=0, padx=10, pady=10)
    entry_course_name = tk.Entry(tab)
    entry_course_name.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(tab, text="Instructor:").grid(row=1, column=0, padx=10, pady=10)
    
    instructors = get_all_instructors()
    instructor_ids = [str(inst.instructor_id) for inst in instructors]
    instructor_ids.insert(0, "None")
    
    instructor_dropdown = ttk.Combobox(tab, values=instructor_ids)
    instructor_dropdown.grid(row=1, column=1, padx=10, pady=10)
    instructor_dropdown.set("None")

    tk.Button(tab, text="Create Course", command=create_course).grid(row=2, column=0, columnspan=2, pady=10)
