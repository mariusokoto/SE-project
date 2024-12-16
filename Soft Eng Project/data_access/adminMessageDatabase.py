import oracledb
from data_access.database import DatabaseConnection

def insert_message(course_id, onlyprof, contenu):
    """
    Inserts a new message into the message table.
    """
    connection = DatabaseConnection.get_connection()
    if not connection:
        print("Database connection is not established.")
        return False

    try:
        with connection.cursor() as cursor:
            query = """
                INSERT INTO message (course_id, onlyprof, contenu)
                VALUES (:course_id, :onlyprof, :contenu)
            """
            cursor.execute(query, {"course_id": course_id, "onlyprof": onlyprof, "contenu": contenu})
            connection.commit()
            print(f"Message inserted for course_id {course_id}.")
            return True
    except oracledb.Error as e:
        print(f"Error inserting message: {e}")
        connection.rollback()
        return False

def retrieve_messages():
    """
    Retrieves all messages from the message table.
    """
    connection = DatabaseConnection.get_connection()
    if not connection:
        print("Database connection is not established.")
        return [], []

    try:
        with connection.cursor() as cursor:
            query = """
                SELECT 
                    m.message_id, 
                    m.course_id, 
                    c.course_name, 
                    m.onlyprof, 
                    m.contenu
                FROM 
                    message m
                INNER JOIN 
                    courses c ON m.course_id = c.course_id
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            print(f"Retrieved {len(rows)} messages.")
            return rows, columns
    except oracledb.Error as e:
        print(f"Error retrieving messages: {e}")
        return [], []