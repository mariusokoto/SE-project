import oracledb


from data_access.database import DatabaseConnection


def view_courses():
    """
    Fetch all courses from the courses table and handle LOB types.
    """
    connection = DatabaseConnection.get_connection()
    if not connection:
        print("Database connection could not be established.")
        return None, None

    try:
        with connection.cursor() as cursor:
            query = """
                SELECT course_id, course_name, description, credit_hours, department,
                       teacher_id, day_of_week, start_time, end_time, semester,
                       max_students, created_at, updated_at
                FROM courses
            """
            print("Executing query to fetch courses...")
            cursor.execute(query)

            # Initialize list for rows
            rows = []
            for row in cursor:
                # Convert row to a list for modification
                row = list(row)

                # Handle CLOB types 
                if isinstance(row[2], oracledb.LOB):  
                    row[2] = row[2].read()  # Convert CLOB to string

                rows.append(row)

            # Retrieve column names
            columns = [col[0] for col in cursor.description]

            print(f"Fetched {len(rows)} rows from courses table.")
            return rows, columns

    except oracledb.DatabaseError as e:
        print(f"Error fetching courses: {e}")
        return None, None




from datetime import datetime

def create_course_in_db(course_name, description, credit_hours, department, teacher_id, 
                        day_of_week, start_time, end_time, semester, max_students):
    """
    Insert a new course into the courses table with updated structure, ensuring the teacher_id exists.
    """
    connection = DatabaseConnection.get_connection()
    if not connection:
        print("Database connection could not be established.")
        return False

    try:
        with connection.cursor() as cursor:
            # Verify if the teacher_id exists (only if a teacher_id is provided)
            if teacher_id:
                teacher_check_query = "SELECT COUNT(*) FROM teachers WHERE teacher_id = :teacher_id"
                cursor.execute(teacher_check_query, {"teacher_id": teacher_id})
                teacher_exists = cursor.fetchone()[0]
                if not teacher_exists:
                    print(f"Teacher ID {teacher_id} does not exist.")
                    return False

            # Convert start_time and end_time to datetime objects
            today = datetime.today()
            start_time = datetime.combine(today, start_time)  # Combine current date with start_time
            end_time = datetime.combine(today, end_time)      # Combine current date with end_time

            # Insert the course
            query = """
            INSERT INTO courses (
                course_name, description, credit_hours, department, teacher_id, 
                day_of_week, start_time, end_time, semester, max_students
            ) VALUES (
                :course_name, :description, :credit_hours, :department, :teacher_id, 
                :day_of_week, :start_time, :end_time, :semester, :max_students
            )
            """
            # Execute the query with parameters
            cursor.execute(query, {
                "course_name": course_name,
                "description": description,
                "credit_hours": credit_hours,
                "department": department,
                "teacher_id": teacher_id,
                "day_of_week": day_of_week,
                "start_time": start_time,
                "end_time": end_time,
                "semester": semester,
                "max_students": max_students
            })
            
            # Commit the transaction
            connection.commit()
            print("Course created successfully.")
            return True

    except oracledb.DatabaseError as e:
        print(f"Failed to create course: {e}")
        return False



def add_student_to_course(student_id, course_id):
    """
    Add a student to a course in the student_courses table.

    """
    connection = DatabaseConnection.get_connection()
    if not connection:
        print("Database connection could not be established.")
        return False

    try:
        with connection.cursor() as cursor:
            # Check if the student exists
            student_check_query = "SELECT COUNT(*) FROM students WHERE student_id = :student_id"
            cursor.execute(student_check_query, {"student_id": student_id})
            student_exists = cursor.fetchone()[0]

            if not student_exists:
                print(f"Student ID {student_id} does not exist.")
                return False

            # Check if the course exists
            course_check_query = "SELECT COUNT(*) FROM courses WHERE course_id = :course_id"
            cursor.execute(course_check_query, {"course_id": course_id})
            course_exists = cursor.fetchone()[0]

            if not course_exists:
                print(f"Course ID {course_id} does not exist.")
                return False

            # Check if the student is already enrolled in the course
            enrollment_check_query = """
            SELECT COUNT(*) FROM student_courses 
            WHERE student_id = :student_id AND course_id = :course_id
            """
            cursor.execute(enrollment_check_query, {"student_id": student_id, "course_id": course_id})
            already_enrolled = cursor.fetchone()[0]

            if already_enrolled:
                print(f"Student ID {student_id} is already enrolled in Course ID {course_id}.")
                return False

            # Add the student to the course
            enrollment_query = """
            INSERT INTO student_courses (student_id, course_id, enrollment_date)
            VALUES (:student_id, :course_id, CURRENT_TIMESTAMP)
            """
            cursor.execute(enrollment_query, {"student_id": student_id, "course_id": course_id})
            connection.commit()

            print(f"Student ID {student_id} successfully added to Course ID {course_id}.")
            return True

    except oracledb.DatabaseError as e:
        print(f"Failed to add student {student_id} to course {course_id}: {e}")
        return False





def get_students_in_course(course_id):
    """
    Fetch the list of students enrolled in a course.

    Args:
        course_id (int): The ID of the course.

    Returns:
        tuple: A tuple containing rows (list of tuples) and columns (list of column names).
               Returns (None, None) if the operation fails.
    """
    connection = DatabaseConnection.get_connection()
    if not connection:
        print("Database connection could not be established.")
        return None, None

    try:
        with connection.cursor() as cursor:
            # Check if the course exists
            course_check_query = "SELECT COUNT(*) FROM courses WHERE course_id = :course_id"
            cursor.execute(course_check_query, {"course_id": course_id})
            course_exists = cursor.fetchone()[0]

            if not course_exists:
                print(f"Course ID {course_id} does not exist.")
                return None, None

            # Query to fetch enrolled students
            query = """
            SELECT 
                s.student_id,
                s.user_id,
                s.first_name,
                s.last_name,
                s.email,
                s.major,
                s.current_academic_year,
                sc.enrollment_date
            FROM student_courses sc
            INNER JOIN students s ON sc.student_id = s.student_id
            WHERE sc.course_id = :course_id
            """
            print(f"Executing query to fetch students for Course ID {course_id}...")
            cursor.execute(query, {"course_id": course_id})

            # Fetch rows and column names
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]

            print(f"Found {len(rows)} students enrolled in Course ID {course_id}.")
            return rows, columns

    except oracledb.DatabaseError as e:
        print(f"Database error while fetching students for course {course_id}: {e}")
        return None, None
