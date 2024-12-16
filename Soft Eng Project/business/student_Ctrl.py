from data_access.studentDatabase import get_student_personal_info, get_student_id_by_user_id, get_student_courses, get_all_grades_for_student_course, get_attendance_for_course


def ctrl_layer_get_student_info(user_id):
    """
    Retrieve student information through the business layer.
    """
    try:
        return get_student_personal_info(user_id)
    except Exception as e:
        print(f"Error in business layer fetching student information for user_id {user_id}: {e}")
        return None


def ctrl_layer_get_student_courses(user_id):
    """
    Retrieve all courses for a student based on their user_id.
    """
    student_id = get_student_id_by_user_id(user_id)
    if not student_id:
        raise ValueError(f"No student found for user ID {user_id}.")

    return get_student_courses(student_id)


def business_layer_get_all_grades_for_course(user_id, course_name):
    """
    Retrieve all grades for a specific course.
    """
    # Get student_id from user_id
    student_id = get_student_id_by_user_id(user_id)
    if not student_id:
        raise ValueError(f"No student found for user ID {user_id}.")

    return get_all_grades_for_student_course(student_id, course_name)


def ctrl_layer_get_attendance_for_course(user_id, course_name):
    """
    Retrieve the attendance for a specific course.
    """
    # Get student_id from user_id
    student_id = get_student_id_by_user_id(user_id)
    if not student_id:
        raise ValueError(f"No student found for user ID {user_id}.")

    return get_attendance_for_course(student_id, course_name)


def business_layer_get_mean_grade_for_course(user_id, course_name):
    """
    Calculate the mean grade for a specific course.

    """
    # Get student_id from user_id
    student_id = get_student_id_by_user_id(user_id)
    if not student_id:
        raise ValueError(f"No student found for user ID {user_id}.")

    grades = get_all_grades_for_student_course(student_id, course_name)
    if not grades:
        return 0.0  # Return 0 if no grades are found

    # Extract grade values and calculate the mean
    grade_values = [grade["grade"] for grade in grades if grade["grade"] is not None]
    if grade_values:
        return sum(grade_values) / len(grade_values)
    else:
        return 0.0
