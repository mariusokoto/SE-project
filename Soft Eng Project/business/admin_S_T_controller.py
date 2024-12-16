from data_access.adminManageTeachersStudents import add_student,view_students, modify_student, delete_student
from data_access.adminManageTeachersStudents import add_teacher,view_teachers,modify_teacher,delete_teacher



def ctrl_add_student(first_name, last_name, date_of_birth, year, email, major, enrollment_date, password):
    """add a student."""
    if not all([first_name, last_name, date_of_birth, year, email, major, enrollment_date, password]):
        raise ValueError("All fields are required!")
    if year < 1 or year > 12:
        raise ValueError("Academic Year must be between 1 and 12.")
    
    return add_student(first_name, last_name, date_of_birth, year, email, major, enrollment_date, password)


def ctrl_view_students():
    """Fetch all student records."""
    rows, columns = view_students()
    return rows, columns


def ctrl_modify_student(student_id, user_id, first_name, last_name, date_of_birth, year, email, major, enrollment_date, password):
    """modify a student."""
    if not student_id or not user_id:
        raise ValueError("Student ID and User ID are required!")
    if year < 1 or year > 12:
        raise ValueError("Academic Year must be between 1 and 12.")

    return modify_student(student_id, user_id, first_name, last_name, date_of_birth, year, email, major, enrollment_date, password)



def ctrl_delete_student(student_id, user_id, last_name):
    """delete a student."""
    if not student_id or not user_id or not last_name:
        raise ValueError("Student ID, User ID, and Last Name are required!")

    return delete_student(student_id, user_id, last_name)



def ctrl_add_teacher(first_name, last_name, date_of_birth, email, enrollment_date, department, courses_taught, password):
    """add a teacher."""
    if not all([first_name, last_name, date_of_birth, email, enrollment_date, department, courses_taught, password]):
        raise ValueError("All fields are required!")

    # Split and validate courses
    courses = [course.strip() for course in courses_taught.split(",") if course.strip()]
    if not courses:
        raise ValueError("Courses Taught must include at least one course.")

    return add_teacher(first_name, last_name, date_of_birth, email, enrollment_date, department, courses, password)


def ctrl_add_teacher(first_name, last_name, date_of_birth, email, enrollment_date, department, courses_taught, password):
    """
    Controller logic to add a teacher.
    """
    if not all([first_name, last_name, date_of_birth, email, enrollment_date, department, courses_taught, password]):
        raise ValueError("All fields are required!")

    if not isinstance(courses_taught, str) or not courses_taught.strip():
        raise ValueError("Courses Taught must be a comma-separated string.")

    # Call the model to add the teacher
    return add_teacher(
        first_name, last_name, date_of_birth, email,
        enrollment_date, department, courses_taught, password
    )



def ctrl_view_teachers():
    """Fetch all teacher records."""
    rows, columns = view_teachers()
    return rows, columns

def ctrl_modify_teacher(teacher_id, user_id, first_name, last_name, date_of_birth, email, enrollment_date, department, courses_taught, password=None):
    """Modify a teacher's record."""
    if not teacher_id or not user_id:
        raise ValueError("Teacher ID and User ID are required!")
    
    if password and not password.strip():
        raise ValueError("Password cannot be blank if provided.")
    
    return modify_teacher(
        teacher_id, user_id, first_name, last_name, date_of_birth, email,
        enrollment_date, department, courses_taught, password
    )

def ctrl_delete_teacher(teacher_id, user_id, last_name):
    """Delete a teacher's record."""
    if not teacher_id or not user_id or not last_name:
        raise ValueError("Teacher ID, User ID, and Last Name are required!")
    
    return delete_teacher(teacher_id, user_id, last_name)






