from data_access.teacherDatabase import retrieve_teacher_info,get_courses_by_teacher_id,get_teacher_id_by_user_id, get_students_by_class_name

from data_access.teacherDatabase import get_course_id_by_class_name_and_teacher, insert_new_grade, get_class_grades, record_attendance

def ctrl_retrieve_teacher_info(user_id):
    """
    Handles business logic for retrieving teacher information.
    """
    if not isinstance(user_id, int):
        raise ValueError("Invalid user ID provided.")
    
    return retrieve_teacher_info(user_id)



def ctrl_layer_get_teacher_courses(user_id):
    """
    Retrieves the courses taught by a professor based on their user_id.
    """
    # Validate input
    if not isinstance(user_id, int):
        raise ValueError("Invalid user ID provided.")

    # Retrieve teacher_id from the teachers table
    teacher_id = get_teacher_id_by_user_id(user_id)
    if not teacher_id:
        raise ValueError("Teacher not found for the given user ID.")

    # Retrieve courses for the teacher_id
    return get_courses_by_teacher_id(teacher_id)



def ctrl_layer_get_students_in_class(class_name):
    """
    Retrieves the students enrolled in a specific class.

    """
    if not class_name:
        raise ValueError("Class name cannot be empty.")

    # Pass to database layer
    students = get_students_by_class_name(class_name)
    return students


def ctrl_assign_grades_to_students(user_id, class_name, student_grades):
    """
    Assign grades to students for a specific class.
    """
    try:
        teacher_id = get_teacher_id_by_user_id(user_id)
        if not teacher_id:
            print(f"Error: No teacher found for user_id {user_id}")
            return False

        # Fetch course_id for the class
        course_id = get_course_id_by_class_name_and_teacher(class_name, teacher_id)
        if not course_id:
            print(f"Error: Course not found for class {class_name} and teacher ID {teacher_id}")
            return False

        # Assign grades for each student
        for student_id, grades in student_grades.items():
            for grade_info in grades:
                grade_type = grade_info.get("grade_type")
                grade = grade_info.get("grade")
                if grade and grade_type:  # Ensure both grade and grade_type are not empty
                    insert_new_grade(student_id, course_id, teacher_id, grade, grade_type)

        return True
    except Exception as e:
        print(f"Error assigning grades: {e}")
        return False



def ctrl_layer_get_class_grades(user_id, class_name):
    """
    Retrieve grades for all students in a specific class.

    """
    # Get teacher_id from user_id
    teacher_id = get_teacher_id_by_user_id(user_id)
    if not teacher_id:
        raise ValueError(f"No teacher found for user ID {user_id}.")

    # Get course_id for the class
    course_id = get_course_id_by_class_name_and_teacher(class_name, teacher_id)
    if not course_id:
        raise ValueError(f"No course found for class {class_name} and teacher ID {teacher_id}.")

    # Retrieve grades from the database
    return get_class_grades(course_id)



def ctrl_save_attendance(user_id, class_name, attendance_records):
    """
    Save attendance for students in a specific class.
    """
    try:
        # Get teacher_id from user_id
        teacher_id = get_teacher_id_by_user_id(user_id)
        if not teacher_id:
            raise ValueError(f"No teacher found for user ID {user_id}.")

        # Get course_id for the class
        course_id = get_course_id_by_class_name_and_teacher(class_name, teacher_id)
        if not course_id:
            raise ValueError(f"No course found for class {class_name} and teacher ID {teacher_id}.")

        # Save attendance for each student
        for student_id, is_present in attendance_records.items():
            record_attendance(student_id, course_id, teacher_id, is_present)

        return True
    except Exception as e:
        print(f"Error saving attendance: {e}")
        return False
