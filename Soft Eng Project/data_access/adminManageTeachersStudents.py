
from datetime import datetime
import oracledb
from data_access.database import DatabaseConnection

def add_student(first_name, last_name, date_of_birth, current_academic_year, email, major, enrollment_date, password):
    """
    Insert a new student into the students table and create a corresponding user in the users table.

    Returns:
        bool: True if the operation is successful, False otherwise.
    """
    connection = DatabaseConnection.get_connection()
    if not connection:
        print("Database connection could not be established.")
        return False

    try:
        with connection.cursor() as cursor:
            # Insert into users table and fetch user_id
            user_query = """
            INSERT INTO users (email, password, role)
            VALUES (:email, :password, :role)
            RETURNING user_id INTO :user_id
            """
            user_id_var = cursor.var(oracledb.NUMBER)  # Oracle-compatible variable
            cursor.execute(user_query, {
                "email": email,
                "password": password,
                "role": "student",
                "user_id": user_id_var
            })
            user_id = int(user_id_var.getvalue()[0])  # Get the returned user_id as an integer

            # Insert into students table
            student_query = """
            INSERT INTO students (
                user_id, first_name, last_name, date_of_birth, 
                current_academic_year, email, major, enrollment_date, password
            ) VALUES (:user_id, :first_name, :last_name, :date_of_birth, 
                      :current_academic_year, :email, :major, :enrollment_date, :password)
            """
            cursor.execute(student_query, {
                "user_id": user_id,
                "first_name": first_name,
                "last_name": last_name,
                "date_of_birth": date_of_birth,
                "current_academic_year": current_academic_year,
                "email": email,
                "major": major,
                "enrollment_date": enrollment_date,
                "password": password
            })

            # Commit the transaction
            connection.commit()
            print(f"Student {first_name} {last_name} added successfully with User ID {user_id}.")
            return True

    except oracledb.DatabaseError as e:
        print(f"Failed to add student: {e}")
        # Rollback the transaction on failure
        connection.rollback()
        return False



def view_students():
    """
    Fetch all students from the students table.

    """
    connection = DatabaseConnection.get_connection()
    if not connection:
        print("Database connection could not be established.")
        return None, None

    try:
        with connection.cursor() as cursor:
            # Query to fetch all students
            query = """
            SELECT 
                student_id, user_id, first_name, last_name, date_of_birth,
                current_academic_year, email, major, enrollment_date, password
            FROM students
            """
            print("Executing query to fetch all students...")
            cursor.execute(query)

            # Fetch rows and column names
            rows = cursor.fetchall()  # Fetch all rows
            columns = [col[0] for col in cursor.description]  # Get column names

            print(f"Fetched {len(rows)} students from the database.")
            return rows, columns

    except oracledb.DatabaseError as e:
        print(f"Failed to fetch students: {e}")
        return None, None



def modify_student(student_id, user_id, first_name, last_name, date_of_birth, 
                   current_academic_year, email, major, enrollment_date, password=None):
    """
    Modify an existing student record by student_id, and update the email or password in the users table if changed.
    Returns:
        bool: True if the operation is successful, False otherwise.
    """
    connection = DatabaseConnection.get_connection()
    if not connection:
        print("Database connection could not be established.")
        return False

    try:
        with connection.cursor() as cursor:
            # Fetch the current email and password from the database
            query = "SELECT email, password FROM students WHERE student_id = :student_id"
            cursor.execute(query, {"student_id": student_id})
            current_data = cursor.fetchone()

            if not current_data:
                print(f"No student found with ID {student_id}.")
                return False

            current_email, current_password = current_data

            # Use the provided password or keep the current one
            new_password = password if password else current_password

            # Update the students table
            student_query = """
            UPDATE students
            SET first_name = :first_name, last_name = :last_name, date_of_birth = :date_of_birth,
                current_academic_year = :current_academic_year, email = :email, major = :major,
                enrollment_date = :enrollment_date, password = :password
            WHERE student_id = :student_id
            """
            cursor.execute(student_query, {
                "first_name": first_name,
                "last_name": last_name,
                "date_of_birth": date_of_birth,
                "current_academic_year": current_academic_year,
                "email": email,
                "major": major,
                "enrollment_date": enrollment_date,
                "password": new_password,
                "student_id": student_id
            })

            # Update the users table if email or password has changed
            if email != current_email or (password and password != current_password):
                user_update_query = """
                UPDATE users
                SET email = :email, password = :password
                WHERE user_id = :user_id
                """
                cursor.execute(user_update_query, {
                    "email": email,
                    "password": new_password,
                    "user_id": user_id
                })

            connection.commit()
            print(f"Student with ID {student_id} and corresponding user updated successfully.")
            return True

    except oracledb.DatabaseError as e:
        print(f"Failed to modify student: {e}")
        connection.rollback()  # Rollback the transaction on failure
        return False



def delete_student(student_id, user_id, last_name):
    """
    Deletes a student and the corresponding user from the database.
    """
    connection = DatabaseConnection.get_connection()
    if not connection:
        print("Failed to connect to the database.")
        return False

    try:
        with connection.cursor() as cursor:
            # Begin transaction
            print("Starting deletion process...")

            # Delete student record
            delete_student_query = """
            DELETE FROM students
            WHERE student_id = :student_id AND last_name = :last_name
            """
            cursor.execute(delete_student_query, {
                "student_id": student_id,
                "last_name": last_name
            })

            # Check if any student rows were affected
            if cursor.rowcount == 0:
                print(f"No student found with ID {student_id} and last name {last_name}.")
                return False
            print(f"Student with ID {student_id} and last name {last_name} deleted successfully.")

            # Delete corresponding user record
            delete_user_query = """
            DELETE FROM users
            WHERE user_id = :user_id
            """
            cursor.execute(delete_user_query, {
                "user_id": user_id
            })

            # Check if the user was deleted
            if cursor.rowcount == 0:
                print(f"No user found with ID {user_id}. Rolling back transaction.")
                connection.rollback()
                return False
            print(f"User with ID {user_id} deleted successfully.")

            # Commit transaction
            connection.commit()
            print("Deletion process completed successfully.")
            return True

    except oracledb.DatabaseError as e:
        print(f"An error occurred while deleting the student: {e}")
        connection.rollback()  # Rollback the transaction on error
        return False



def add_teacher(first_name, last_name, date_of_birth, email, enrollment_date, department, courses_taught, password):
    """
    Insert a new teacher into the teachers table and create a corresponding user in the users table.

    Args:
        first_name (str): Teacher's first name.
        last_name (str): Teacher's last name.
        date_of_birth (datetime): Teacher's date of birth.
        email (str): Teacher's email address.
        enrollment_date (datetime): Teacher's enrollment date.
        department (str): Teacher's department.
        courses_taught (str): JSON or string of courses taught by the teacher.
        password (str): Teacher's password.

    Returns:
        bool: True if the operation is successful, False otherwise.
    """
    connection = DatabaseConnection.get_connection()
    if not connection:
        print("Failed to connect to the database.")
        return False

    try:
        with connection.cursor() as cursor:
            # Insert into users table and fetch user_id
            user_query = """
            INSERT INTO users (email, password, role)
            VALUES (:email, :password, :role)
            RETURNING user_id INTO :user_id
            """
            user_id_var = cursor.var(oracledb.NUMBER)  # Oracle-compatible variable
            cursor.execute(user_query, {
                "email": email,
                "password": password,
                "role": "teacher",
                "user_id": user_id_var
            })
            user_id = int(user_id_var.getvalue()[0])  # Get the returned user_id as an integer

            # Insert into teachers table
            teacher_query = """
            INSERT INTO teachers (
                user_id, first_name, last_name, date_of_birth,
                email, enrollment_date, department, courses_taught, password
            ) VALUES (:user_id, :first_name, :last_name, :date_of_birth, 
                      :email, :enrollment_date, :department, :courses_taught, :password)
            """
            cursor.execute(teacher_query, {
                "user_id": user_id,
                "first_name": first_name,
                "last_name": last_name,
                "date_of_birth": date_of_birth,
                "email": email,
                "enrollment_date": enrollment_date,
                "department": department,
                "courses_taught": courses_taught,
                "password": password
            })

            connection.commit()
            print(f"Teacher {first_name} {last_name} added successfully with User ID {user_id}.")
            return True

    except oracledb.DatabaseError as e:
        print(f"Failed to add teacher: {e}")
        connection.rollback()  # Rollback the transaction on failure
        return False



def view_teachers():
    """
    Fetch all teachers from the teachers table.

    Returns:
        tuple: A tuple containing the list of rows and column names.
    """
    connection = DatabaseConnection.get_connection()
    if not connection:
        print("Database connection could not be established.")
        return [], []

    try:
        with connection.cursor() as cursor:
            query = """
            SELECT teacher_id, user_id, first_name, last_name, date_of_birth,
                   email, enrollment_date, department, courses_taught, password
            FROM teachers
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            # Convert LOBs to strings
            if rows:
                rows = [
                    [
                        str(value.read()) if isinstance(value, oracledb.LOB) else value
                        for value in row
                    ]
                    for row in rows
                ]

            # Get column names
            columns = [col[0] for col in cursor.description]
            return rows, columns

    except oracledb.DatabaseError as e:
        print(f"Failed to fetch teachers: {e}")
        return [], []
 


def modify_teacher(teacher_id, user_id, first_name, last_name, date_of_birth, email, enrollment_date, department, courses_taught, password=None):
    """
    Modify an existing teacher record in the teachers table and update the corresponding user record in the users table.
    Returns:
        bool: True if the operation is successful, False otherwise.
    """
    connection = DatabaseConnection.get_connection()
    if not connection:
        print("Database connection could not be established.")
        return False

    try:
        with connection.cursor() as cursor:
            # Fetch the current email and password from the teachers table
            query = "SELECT email, password FROM teachers WHERE teacher_id = :teacher_id"
            cursor.execute(query, {"teacher_id": teacher_id})
            current_data = cursor.fetchone()

            if not current_data:
                print(f"No teacher found with ID {teacher_id}.")
                return False

            current_email, current_password = current_data

            # Use the provided password or keep the current one
            password = password if password else current_password

            # Update the teachers table
            update_teacher_query = """
            UPDATE teachers
            SET first_name = :first_name, last_name = :last_name, date_of_birth = :date_of_birth,
                email = :email, enrollment_date = :enrollment_date, department = :department, 
                courses_taught = :courses_taught, password = :password
            WHERE teacher_id = :teacher_id
            """
            cursor.execute(update_teacher_query, {
                "first_name": first_name,
                "last_name": last_name,
                "date_of_birth": date_of_birth,
                "email": email,
                "enrollment_date": enrollment_date,
                "department": department,
                "courses_taught": courses_taught,
                "password": password,
                "teacher_id": teacher_id
            })

            # Update the users table if email or password has changed
            if email != current_email or (password and password != current_password):
                update_user_query = """
                UPDATE users
                SET email = :email, password = :password
                WHERE user_id = :user_id
                """
                cursor.execute(update_user_query, {
                    "email": email,
                    "password": password,
                    "user_id": user_id
                })

            connection.commit()
            print(f"Teacher with ID {teacher_id} and corresponding user updated successfully.")
            return True

    except oracledb.DatabaseError as e:
        print(f"Failed to modify teacher: {e}")
        connection.rollback()  # Rollback the transaction on failure
        return False



def delete_teacher(teacher_id, user_id_teacher, last_name_teacher):
    """
    Deletes a teacher and the corresponding user from the database.

    Args:
        teacher_id (int): The ID of the teacher to be deleted.
        user_id_teacher (int): The corresponding user ID for the teacher.
        last_name_teacher (str): The last name of the teacher for verification.

    Returns:
        bool: True if the operation is successful, False otherwise.
    """
    connection = DatabaseConnection.get_connection()
    if not connection:
        print("Failed to connect to the database.")
        return False

    try:
        with connection.cursor() as cursor:
            print("Starting deletion process...")

            # Delete teacher record
            delete_teacher_query = """
            DELETE FROM teachers
            WHERE teacher_id = :teacher_id AND last_name = :last_name_teacher
            """
            cursor.execute(delete_teacher_query, {
                "teacher_id": teacher_id,
                "last_name_teacher": last_name_teacher
            })

            # Check if any teacher rows were affected
            if cursor.rowcount == 0:
                print(f"No teacher found with ID {teacher_id} and last name {last_name_teacher}.")
                return False
            print(f"Teacher with ID {teacher_id} and last name {last_name_teacher} deleted successfully.")

            # Delete corresponding user record
            delete_user_query = """
            DELETE FROM users
            WHERE user_id = :user_id
            """
            cursor.execute(delete_user_query, {
                "user_id": user_id_teacher
            })

            # Check if the user was deleted
            if cursor.rowcount == 0:
                print(f"No user found with ID {user_id_teacher}. Rolling back transaction.")
                connection.rollback()
                return False
            print(f"User with ID {user_id_teacher} deleted successfully.")

            # Commit transaction
            connection.commit()
            print("Deletion process completed successfully.")
            return True

    except oracledb.DatabaseError as e:
        print(f"An error occurred while deleting the teacher: {e}")
        connection.rollback()  # Rollback the transaction on error
        return False

    
