import streamlit as st
from data_access.database import authenticate_user
from pages.admin_dashboard.admin import admin_page  # Import the admin page
from pages.teacher_dashboard.teacher import teacher_page  # Import the teacher page
from pages.student_dashboard.student import student_page  # Import the student page

import atexit
from data_access.database import DatabaseConnection
import pandas as pd

def on_session_end():
    """Close the database connection when the session ends."""
    DatabaseConnection.close_connection()

# Call on_session_end explicitly when session ends
st.session_state.on_session_end = on_session_end


# Set up the main app interface
st.set_page_config(page_title="School Management System", page_icon="📚", layout="wide")

# Define login state
if "role" not in st.session_state:
    st.session_state["role"] = None
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None

def login():
    """Login page for the application."""
    st.title("📚 School Management System")
    st.subheader("Login to your account")

    # Input fields
    email = st.text_input("Email", placeholder="Enter your email", key="email")
    password = st.text_input("Password", placeholder="Enter your password", type="password", key="password")

    if st.button("Login"):
        if email and password:
            auth_result = authenticate_user(email, password)
            if auth_result:
                print(f"Authentication result: {auth_result}")
                role, user_id = auth_result
                st.session_state["role"] = role
                st.session_state["user_id"] = user_id
                st.success(f"Logged in as {role}")
            else:
                st.error("Invalid email or password.")
        else:
            st.error("Please enter both email and password.")


from business.message_Ctrl import fetch_messages
def display_notifications():
    """
    Fetch and display relevant messages as notifications for the logged-in user.
    """
    user_id = st.session_state.get("user_id")
    user_role = st.session_state.get("role")  # Get the user's role (e.g., "teacher", "student")

    if user_id:
        try:
            # Fetch all messages
            rows, columns = fetch_messages()
            if rows and columns:
                # Convert to DataFrame
                df = pd.DataFrame(rows, columns=columns)

                # Filter messages based on user role
                if user_role == "teacher":
                    # Teachers can see all messages
                    filtered_df = df[(df["ONLYPROF"] == 1) | (df["ONLYPROF"] == 0)]
                else:
                    # Other roles can see only public messages
                    filtered_df = df[df["ONLYPROF"] == 0]

                # Display messages as notifications
                if not filtered_df.empty:
                    st.markdown("### 🔔 Notifications")
                    for _, row in filtered_df.iterrows():
                        st.info(f"**Course {row['COURSE_NAME']}**: {row['CONTENU']}")
                else:
                    st.markdown("### 🔔 No new notifications")
        except Exception as e:
            st.error(f"Error loading notifications: {str(e)}")
    else:
        st.error("You are not logged in.")


def main():
    """Main function to display the correct page."""
    role = st.session_state.get("role")
    if role == "student":
        display_notifications()
        student_page()  # Call the student page function
    elif role == "admin":
        admin_page()  # Call the admin page function
    elif role == "teacher":
        display_notifications()
        teacher_page()  # Call the teacher page function
    else:
        login()


if __name__ == "__main__":
    main()
