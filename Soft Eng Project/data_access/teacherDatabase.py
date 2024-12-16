import oracledb

from data_access.database import DatabaseConnection

def retrieve_teacher_info(user_id):
    """
    Retrieve teacher information from the database for the given user_id.
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
                   teacher_id, user_id, first_name, last_name, date_of_birth, email, enrollment_date, 
                    department, courses_taught, password
                FROM teachers
                WHERE user_id = :user_id
            """
            # Execute the query
            cursor.execute(query, {"user_id": user_id})

            # Fetch the result
            row = cursor.fetchone()

            # If no result is found, return None
            if not row:
                return None
            
            courses_taught = row[8].read() if row[8] else None

            # Map the result to a dictionary
            teacher_info = {
                "teacher_id": row[0], "user_id": row[1], "first_name": row[2], "last_name": row[3],
                "date_of_birth": row[4], "email": row[5], "enrollment_date": row[6], "department": row[7],
                "courses_taught": courses_taught, "password": row[9],
            }
            return teacher_info

    except oracledb.Error as e:
        print("Error retrieving teacher information:", e)
        return None


def get_teacher_id_by_user_id(user_id):
    """
    Retrieve the teacher_id associated with the given user_id from the database.
    """
    connection = DatabaseConnection.get_connection()
    if not connection:
        print("Database connection is not established.")
        return None

    try:
        with connection.cursor() as cursor:
            # Define the query
            query = """
                SELECT teacher_id
                FROM teachers
                WHERE user_id = :user_id
            """
            # Execute the query
            cursor.execute(query, {"user_id": user_id})

            # Fetch the result
            row = cursor.fetchone()

            # If no result is found, return None
            if not row:
                return None

            # Return the teacher_id
            return row[0]

    except oracledb.Error as e:
        print("Error retrieving teacher_id:", e)
        return None



def get_courses_by_teacher_id(teacher_id):
    """
    Retrieve all courses taught by the teacher with the given teacher_id.
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
                    course_id, course_name, description, credit_hours, department, 
                    day_of_week, start_time, end_time, semester
                FROM courses
                WHERE teacher_id = :teacher_id
            """
            # Execute the query
            cursor.execute(query, {"teacher_id": teacher_id})

            # Fetch all results
            rows = cursor.fetchall()

            # If no results are found, return an empty list
            if not rows:
                return []

            # Map the results to a list of dictionaries
            courses = []
            for row in rows:
                courses.append({
                    "course_id": row[0],
                    "course_name": row[1],
                    "description": row[2].read() if row[2] else None,
                    "credit_hours": row[3],
                    "department": row[4],
                    "day_of_week": row[5],
                    "start_time": row[6],
                    "end_time": row[7],
                    "semester": row[8],
                })
            return courses

    except oracledb.Error as e:
        print("Error retrieving courses:", e)
        return None




def get_students_by_class_name(class_name):
    """
    Retrieves the students enrolled in a specific class from the database.

    """
    connection = DatabaseConnection.get_connection()
    if not connection:
        print("Database connection is not established.")
        return None

    try:
        with connection.cursor() as cursor:
            # Define the query to fetch students by class
            query = """
                SELECT students.student_id, students.first_name, students.last_name
                FROM students
                INNER JOIN student_courses ON students.student_id = student_courses.student_id
                INNER JOIN courses ON student_courses.course_id = courses.course_id
                WHERE courses.course_name = :class_name
            """
            # Execute the query
            cursor.execute(query, {"class_name": class_name})

            # Fetch all results
            rows = cursor.fetchall()

            # Map the results to a list of dictionaries
            students = [
                {"student_id": row[0], "name": f"{row[1]} {row[2]}"}
                for row in rows
            ]
            return students

    except oracledb.Error as e:
        print(f"Error retrieving students for class {class_name}:", e)
        return None


def get_course_id_by_class_name_and_teacher(class_name, teacher_id):
    """
    Retrieve the course ID for a given class name and teacher ID.
    """
    connection = DatabaseConnection.get_connection()
    if not connection:
        print("Database connection is not established.")
        return None

    try:
        with connection.cursor() as cursor:
            query = """
                SELECT course_id
                FROM courses
                WHERE course_name = :class_name AND teacher_id = :teacher_id
            """
            cursor.execute(query, {"class_name": class_name, "teacher_id": teacher_id})
            row = cursor.fetchone()
            return row[0] if row else None
    except oracledb.Error as e:
        print(f"Error retrieving course ID: {e}")
        return None


def insert_new_grade(student_id, course_id, teacher_id, grade, grade_type):
    """
    Insert a new grade for a specific student and course with grade type.

    """
    connection = DatabaseConnection.get_connection()
    if not connection:
        print("Database connection is not established.")
        return

    try:
        with connection.cursor() as cursor:
            # Insert a new grade with grade_type
            insert_query = """
                INSERT INTO grades (student_id, course_id, teacher_id, grade, assigned_at, grade_type)
                VALUES (:student_id, :course_id, :teacher_id, :grade, CURRENT_TIMESTAMP, :grade_type)
            """
            cursor.execute(insert_query, {
                "student_id": student_id,
                "course_id": course_id,
                "teacher_id": teacher_id,
                "grade": grade,
                "grade_type": grade_type
            })

            # Commit the transaction
            connection.commit()
            print(f"Grade successfully inserted for student_id={student_id}, course_id={course_id}, grade_type={grade_type}.")
    except oracledb.Error as e:
        print(f"Error inserting grade: {e}")





def get_class_grades(course_id):
    """
    Retrieve grades for all students in a specific course.
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
                    g.grade
                FROM 
                    grades g
                INNER JOIN 
                    students s ON g.student_id = s.student_id
                WHERE 
                    g.course_id = :course_id
            """
            # Execute the query
            cursor.execute(query, {"course_id": course_id})

            # Fetch all results
            rows = cursor.fetchall()

            # Map the results to a list of dictionaries
            grades = [
                {
                    "student_id": row[0],
                    "first_name": row[1],
                    "last_name": row[2],
                    "grade": row[3],
                }
                for row in rows
            ]
            return grades

    except oracledb.Error as e:
        print(f"Error retrieving grades for course ID {course_id}: {e}")
        return None



def record_attendance(student_id, course_id, teacher_id, is_present):
    """
    Record attendance for a specific student in a class.
    """
    connection = DatabaseConnection.get_connection()
    if not connection:
        print("Database connection is not established.")
        return

    try:
        with connection.cursor() as cursor:
            query = """
                MERGE INTO attendance a
                USING (SELECT :student_id AS student_id, :course_id AS course_id, :teacher_id AS teacher_id FROM dual) b
                ON (a.student_id = b.student_id AND a.course_id = b.course_id)
                WHEN MATCHED THEN
                    UPDATE SET is_present = :is_present, marked_at = CURRENT_TIMESTAMP
                WHEN NOT MATCHED THEN
                    INSERT (student_id, course_id, teacher_id, is_present, marked_at)
                    VALUES (:student_id, :course_id, :teacher_id, :is_present, CURRENT_TIMESTAMP)
            """
            cursor.execute(query, {
                "student_id": student_id,
                "course_id": course_id,
                "teacher_id": teacher_id,
                "is_present": is_present
            })
            connection.commit()
    except oracledb.Error as e:
        print(f"Error recording attendance for student ID {student_id}: {e}")
