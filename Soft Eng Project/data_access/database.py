import oracledb

class DatabaseConnection:
    _instance = None  # Static variable to hold the single instance

    @staticmethod
    def get_connection():
        """Static access method to get the database connection."""
        try:
            # Check if the connection exists and is still open
            if DatabaseConnection._instance is None or DatabaseConnection._instance.ping() is not None:
                # Create or reconnect the instance
                DatabaseConnection._instance = oracledb.connect(
                    user="login_user",
                    password="login_password",
                    dsn="localhost:1521/ORCLPDB1"
                )
        except oracledb.DatabaseError as e:
            print("Database connection failed:", e)
            DatabaseConnection._instance = None
        return DatabaseConnection._instance

    @staticmethod
    def close_connection():
        """Close the database connection."""
        if DatabaseConnection._instance is not None:
            try:
                DatabaseConnection._instance.close()
                DatabaseConnection._instance = None
                print("Database connection closed successfully.")
            except oracledb.DatabaseError as e:
                print("Failed to close the database connection:", e)



def authenticate_user(email, password):
    """Authenticate the user by checking their credentials."""
    connection = DatabaseConnection.get_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                query = """
                SELECT role, user_id FROM users 
                WHERE email = :email AND password = :password
                """
                cursor.execute(query, {"email": email, "password": password})
                result = cursor.fetchone()
                print(f"Query Result -> {result}")
                return (result[0], result[1]) if result else None  # Return the role and user_id if found
        except oracledb.DatabaseError as e:
            print("Error during authentication:", e)
            return None
    else:
        print("Database connection could not be established.")
        return None




