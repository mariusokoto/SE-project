from data_access.adminManageClasses import view_courses,create_course_in_db, add_student_to_course, get_students_in_course

def ctrl_view_courses():
    """Fetch all courses from the database."""
    return view_courses()


def ctrl_create_course_in_db(course_name, description, credit_hours, department, teacher_id, day_of_week, start_time, end_time, semester, max_students):
    """
    Controller logic to create a new course.
    """
    # Validate inputs
    if not all([course_name, credit_hours, day_of_week, start_time, end_time, semester, max_students]):
        raise ValueError("All fields except description and teacher ID are required.")

    if start_time >= end_time:
        raise ValueError("Start time must be before end time.")

    # Call the model function to insert the course
    return create_course_in_db(
        course_name, description, credit_hours, department, teacher_id,
        day_of_week, start_time, end_time, semester, max_students
    )


def ctrl_add_student_to_course(student_id, course_id):
    """
    add a student to a course.
    Validates inputs and interacts with the database layer.
    """
    # Validate inputs
    if not isinstance(student_id, int) or student_id <= 0:
        raise ValueError("Invalid Student ID. It must be a positive integer.")
    if not isinstance(course_id, int) or course_id <= 0:
        raise ValueError("Invalid Course ID. It must be a positive integer.")

    # Call the database layer to add the student to the course
    return add_student_to_course(student_id, course_id)



def ctrl_get_students_in_course(course_id):
    """
    get students enrolled in a course.
    Validates the course_id and fetches the data from the database.
    """
    # Validate course_id
    if not isinstance(course_id, int) or course_id <= 0:
        raise ValueError("Invalid Course ID. It must be a positive integer.")

    return get_students_in_course(course_id)
