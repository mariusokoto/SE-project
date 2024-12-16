import oracledb
from data_access.database import DatabaseConnection



def get_attendance_summary():
    """
    Retrieve attendance summary data from the database.

    """
    connection = DatabaseConnection.get_connection()
    if not connection:
        print("Database connection is not established.")
        return None

    try:
        with connection.cursor() as cursor:
            query = """
                SELECT 
                    c.course_name,
                    COUNT(CASE WHEN a.is_present = 1 THEN 1 END) AS total_present,
                    COUNT(CASE WHEN a.is_present = 0 THEN 1 END) AS total_absent,
                    COUNT(*) AS total_records
                FROM 
                    attendance a
                INNER JOIN 
                    courses c ON a.course_id = c.course_id
                GROUP BY 
                    c.course_name
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            # Map results to a list of dictionaries
            attendance_summary = [
                {
                    "Course Name": row[0],
                    "Total Present": row[1],
                    "Total Absent": row[2],
                    "Total Records": row[3],
                }
                for row in rows
            ]
            return attendance_summary

    except oracledb.Error as e:
        print(f"Error retrieving attendance summary: {e}")
        return None


def get_course_mean_of_means():
    """
    Retrieve the mean of mean grades for each course.

    """
    connection = DatabaseConnection.get_connection()
    if not connection:
        print("Database connection is not established.")
        return None

    try:
        with connection.cursor() as cursor:
            # SQL query to calculate mean of means for each course
            query = """
                SELECT 
                    c.course_name,
                    AVG(student_means.mean_grade) AS mean_of_means,
                    COUNT(DISTINCT student_means.student_id) AS total_students
                FROM 
                    courses c
                INNER JOIN (
                    SELECT 
                        g.student_id, 
                        g.course_id, 
                        AVG(g.grade) AS mean_grade
                    FROM 
                        grades g
                    GROUP BY 
                        g.student_id, g.course_id
                ) student_means
                ON 
                    c.course_id = student_means.course_id
                GROUP BY 
                    c.course_name
            """
            cursor.execute(query)

            rows = cursor.fetchall()

            # Map results to a list of dictionaries
            grade_report = [
                {
                    "course_name": row[0],
                    "mean_of_means": round(row[1], 2),  # Rounded to 2 decimal places
                    "total_students": row[2],
                }
                for row in rows
            ]
            return grade_report

    except oracledb.Error as e:
        print(f"Error generating grade report: {e}")
        return None




def get_course_enrollment_summary():
    """
    Retrieve course enrollment summary data from the database.

    """
    connection = DatabaseConnection.get_connection()
    if not connection:
        print("Database connection is not established.")
        return None

    try:
        with connection.cursor() as cursor:
            query = """
                SELECT 
                    c.course_name,
                    COUNT(sc.student_id) AS total_enrolled
                FROM 
                    student_courses sc
                INNER JOIN 
                    courses c ON sc.course_id = c.course_id
                GROUP BY 
                    c.course_name
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            # Map results to a list of dictionaries
            enrollment_summary = [
                {
                    "Course Name": row[0],
                    "Total Enrolled": row[1],
                }
                for row in rows
            ]
            return enrollment_summary

    except oracledb.Error as e:
        print(f"Error retrieving course enrollment summary: {e}")
        return None



def get_course_enrollment_data():
    """
    Retrieve enrollment data for all courses, including enrolled students and total capacity.

    """
    connection = DatabaseConnection.get_connection()
    if not connection:
        print("Database connection is not established.")
        return None

    try:
        with connection.cursor() as cursor:
            # Query to fetch course enrollment and capacity
            query = """
                SELECT 
                    c.course_name,
                    COUNT(sc.student_id) AS enrolled,
                    c.max_students AS capacity
                FROM 
                    courses c
                LEFT JOIN 
                    student_courses sc ON c.course_id = sc.course_id
                GROUP BY 
                    c.course_name, c.max_students
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            enrollment_data = [
                {
                    "course_name": row[0],
                    "enrolled": row[1],
                    "capacity": row[2],
                }
                for row in rows
            ]
            return enrollment_data

    except oracledb.Error as e:
        print(f"Error retrieving enrollment data: {e}")
        return None



def get_top_students_per_course():
    """
    Retrieve the student with the highest mean grade for each course.

    """
    connection = DatabaseConnection.get_connection()
    if not connection:
        print("Database connection is not established.")
        return None

    try:
        with connection.cursor() as cursor:
            query = """
                WITH student_means AS (
                    SELECT 
                        g.student_id,
                        g.course_id,
                        AVG(g.grade) AS mean_grade
                    FROM 
                        grades g
                    GROUP BY 
                        g.student_id, g.course_id
                ),
                ranked_students AS (
                    SELECT 
                        c.course_name,
                        s.student_id,
                        s.first_name || ' ' || s.last_name AS student_name,
                        student_means.mean_grade,
                        RANK() OVER (PARTITION BY student_means.course_id ORDER BY student_means.mean_grade DESC) AS rnk
                    FROM 
                        student_means
                    INNER JOIN 
                        courses c ON student_means.course_id = c.course_id
                    INNER JOIN 
                        students s ON student_means.student_id = s.student_id
                )
                SELECT 
                    course_name,
                    student_id,
                    student_name,
                    ROUND(mean_grade, 2) AS top_mean_grade
                FROM 
                    ranked_students
                WHERE 
                    rnk = 1
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            # Map results to a list of dictionaries
            top_students = [
                {
                    "course_name": row[0],
                    "student_id": row[1],
                    "student_name": row[2],
                    "top_mean_grade": row[3],
                }
                for row in rows
            ]
            return top_students

    except oracledb.Error as e:
        print(f"Error retrieving top students for courses: {e}")
        return None
