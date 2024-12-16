import oracledb

from data_access.database import DatabaseConnection

def get_student_personal_info(user_id):
    """
    Retrieve personal information for a student from the database.

    """
    connection = DatabaseConnection.get_connection()
    if not connection:
        print("Database connection is not established.")
        return None

    try:
        with connection.cursor() as cursor:
            # Define the query
            query = """
                SELECT 
                    s.student_id,
                    s.first_name,
                    s.last_name,
                    s.date_of_birth,
                    s.current_academic_year,
                    s.email,
                    s.major,
                    s.enrollment_date,
                    s.password
                FROM students s
                WHERE s.user_id = :user_id
            """
            # Execute the query
            cursor.execute(query, {"user_id": user_id})

            # Fetch the result
            row = cursor.fetchone()

            # If no result is found, return None
            if not row:
                return None

            # Map the result to a dictionary
            student_info = {
                "student_id": row[0],
                "first_name": row[1],
                "last_name": row[2],
                "date_of_birth": row[3],
                "current_academic_year": row[4],
                "email": row[5],
                "major": row[6],
                "enrollment_date": row[7],
                "password": row[8],
            }
            return student_info

    except oracledb.Error as e:
        print(f"Error retrieving student personal information for user_id {user_id}: {e}")
        return None
    
def get_student_id_by_user_id(user_id):
    """
    Retrieve the student_id associated with the given user_id from the database.
    """
    connection = DatabaseConnection.get_connection()
    if not connection:
        print("Database connection is not established.")
        return None

    try:
        with connection.cursor() as cursor:
            # Define the query
            query = """
                SELECT student_id
                FROM students
                WHERE user_id = :user_id
            """
            # Execute the query
            cursor.execute(query, {"user_id": user_id})

            # Fetch the result
            row = cursor.fetchone()

            if not row:
                return None

            # Return the teacher_id
            return row[0]

    except oracledb.Error as e:
        print("Error retrieving student_id:", e)
        return None
    

def get_student_courses(student_id):
    """
    Retrieve all courses for a specific student.

    """
    connection = DatabaseConnection.get_connection()
    if not connection:
        print("Database connection is not established.")
        return None

    try:
        with connection.cursor() as cursor:
            # Define the query
            query = """
                SELECT 
                    c.course_name,
                    c.description,
                    c.credit_hours,
                    t.first_name || ' ' || t.last_name AS teacher_name,
                    c.day_of_week,
                    c.start_time,
                    c.end_time,
                    c.semester
                FROM 
                    student_courses sc
                INNER JOIN 
                    courses c ON sc.course_id = c.course_id
                INNER JOIN 
                    teachers t ON c.teacher_id = t.teacher_id
                WHERE 
                    sc.student_id = :student_id
            """
            # Execute the query
            cursor.execute(query, {"student_id": student_id})

            # Fetch all results
            rows = cursor.fetchall()

            # Map the results to a list of dictionaries
            courses = [
                {
                    "course_name": row[0],
                    "description": row[1],
                    "credit_hours": row[2],
                    "teacher_name": row[3],
                    "day_of_week": row[4],
                    "start_time": row[5],
                    "end_time": row[6],
                    "semester": row[7],
                }
                for row in rows
            ]
            return courses

    except oracledb.Error as e:
        print(f"Error retrieving courses for student ID {student_id}: {e}")
        return None


def get_all_grades_for_student_course(student_id, course_name):
    """
    Retrieve all grades for a specific student and course from the database.
    """
    connection = DatabaseConnection.get_connection()
    if not connection:
        print("Database connection is not established.")
        return None

    try:
        with connection.cursor() as cursor:
            # Query to fetch all grades for the student and course
            query = """
                SELECT 
                    g.grade,
                    g.grade_type,
                    g.assigned_at
                FROM 
                    grades g
                INNER JOIN 
                    courses c ON g.course_id = c.course_id
                WHERE 
                    g.student_id = :student_id AND c.course_name = :course_name
            """
            cursor.execute(query, {"student_id": student_id, "course_name": course_name})

            # Fetch all results
            rows = cursor.fetchall()

            # Map the results to a list of dictionaries
            grades = [
                {
                    "grade": row[0],  # Numeric grade
                    "grade_type": row[1],  # Grade type 
                    "assigned_at": row[2],  # Timestamp of grade assignment
                }
                for row in rows
            ]
            return grades

    except oracledb.Error as e:
        print(f"Error retrieving grades for student ID {student_id} and course {course_name}: {e}")
        return None







def get_attendance_for_course(student_id, course_name):
    """
    Retrieve the attendance record for a specific course from the database.

    """
    connection = DatabaseConnection.get_connection()
    if not connection:
        print("Database connection is not established.")
        return None

    try:
        with connection.cursor() as cursor:
            # Define the query
            query = """
                SELECT 
                    a.is_present,
                    a.marked_at
                FROM 
                    attendance a
                INNER JOIN 
                    courses c ON a.course_id = c.course_id
                WHERE 
                    a.student_id = :student_id AND c.course_name = :course_name
            """
            # Execute the query
            cursor.execute(query, {"student_id": student_id, "course_name": course_name})

            # Fetch the result
            row = cursor.fetchone()

            # If no result is found, return None
            if not row:
                return None

            # Map the result to a dictionary
            attendance_details = {
                "is_present": bool(row[0]),
                "marked_at": row[1],
            }
            return attendance_details

    except oracledb.Error as e:
        print(f"Error retrieving attendance for student ID {student_id} and course {course_name}: {e}")
        return None
