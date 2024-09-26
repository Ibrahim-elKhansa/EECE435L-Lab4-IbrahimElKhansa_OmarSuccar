# School Management System

A GUI-based application built using Python and Tkinter to manage school records including students, instructors, and courses. The system supports adding, editing, searching, and deleting records from the database. The application uses SQLite as the database engine and Tkinter for the user interface.

## Authors:

TKINTER: Ibrahim El Khansa 202151253 ike06@mail.aub.edu

PYQT: Omar Succar 202101374 oms21@mail.aub.edu

## Features:

- **Manage Students:**
  Add, search, edit, and delete students. Assign students to courses.

- **Manage Instructors:**
  Add, search, edit, and delete instructors. Assign instructors to courses.
 
- **Manage Courses:**
  Add, search, edit, and delete courses. Assign instructors to courses and enroll students.
  
- **Database Support:**
  Uses SQLite for storing student, instructor, and course information.
  
- **GUI Application:**
 A user-friendly graphical interface built using Tkinter and PYQT.


## Structure:

### Models
- **Includes python files of course, instructors, courses, etc.**

### SQL
- **Includes a file that handles db operations:**

### UI
- **Includes a version for PYQT and another for TKinter.**
- **Includes files for the gui of each page and a validation form, like an email regex, a boolean to check whether ID exists or no, if course exists or no, and so on.**

## Getting Started

### Prerequisites
Ensure you have the following installed:

- Node.js with a version >=14.x
- MongoDB with a version>=4.x
- npm (Node Package Manager) or yarn

### Installation

1. **Clone the repository:**
```git clone https://github.com/Ibrahim-elKhansa/EECE435L-Lab4-IbrahimElKhansa_OmarSuccar.git```

2. **Navigate Project Directory:**
```cd school-management-system```

3. **Run the Project:**
```python3 main_tkinter.py``` or
```python3 main_pyqt.py```
if there is no db, then the db will automatically be created.

## Database Setup

- **If there is no db, then the db will automatically be created.**




