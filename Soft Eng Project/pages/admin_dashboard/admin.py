import streamlit as st
import pandas as pd
from datetime import date

from business.admin_S_T_controller import ctrl_add_student,ctrl_delete_student,ctrl_modify_student,ctrl_view_students
from business.admin_S_T_controller import ctrl_add_teacher,ctrl_delete_teacher,ctrl_modify_teacher,ctrl_view_teachers

from business.admin_Classes_controllers import ctrl_view_courses, ctrl_create_course_in_db,ctrl_add_student_to_course,ctrl_get_students_in_course
from business.admin_viewReports import generate_attendance_report,generate_course_enrollment_report,generate_grade_report, generate_enrollment_pie_charts, generate_top_students_report

from business.message_Ctrl import fetch_messages,create_message

def admin_page():
    """Admin dashboard with sidebar menu."""
    st.sidebar.title("Admin Menu")
    menu_option = st.sidebar.radio(
        "Navigation",
        options=["Manage Students & Teachers","Manage Admin & Users","Manage Classes", "View Reports","Manage Messages" ,"Settings"]
    )

    st.title("🔑 Admin Dashboard")
    
    if menu_option == "Manage Students & Teachers":
        st.header("Manage Students & Teachers")
        st.write("Here you can manage student and teacher accounts and information.")

        # Tabs for adding student and teacher
        tab1, tab2, tab3, tab4 = st.tabs(["Add Student", "View and Modify Students", "Add Teacher", "View and Modify Teachers"])

        with tab1:
            st.subheader("Add Student")
            # Form to add a student
            with st.form(key="add_student_form"):
                first_name = st.text_input("First Name")
                last_name = st.text_input("Last Name")
                date_of_birth = st.date_input("Date of Birth", min_value=date(1900, 1, 1))
                year = st.number_input("Academic Year", min_value=1, max_value=12, step=1)
                email = st.text_input("Email")
                major = st.text_input("Major")
                enrollment_date = st.date_input("Enrollment Date", min_value=date(2000, 1, 1))
                password = st.text_input("Password", type="password")  # Add password field
                submit_button = st.form_submit_button(label="Add Student")

                if submit_button:
                    try:
                        success = ctrl_add_student(
                            first_name, last_name, date_of_birth,
                            year, email, major, enrollment_date, password
                        )
                        st.success(f"Student {first_name} {last_name} added successfully!")
                    except ValueError as e:
                        st.error(str(e))
                    except Exception:
                        st.error("Failed to add student. Please check the details and try again.")


        with tab2:
            st.subheader("View and Modify Students")
            placeholder = st.empty()  # Placeholder for the table

            # Function to render the student table
            def render_student_table():
                try:
                    rows, columns = ctrl_view_students()
                    if rows:
                        df = pd.DataFrame(rows, columns=columns)
                        placeholder.dataframe(df)  # Update the placeholder with the DataFrame
                    else:
                        placeholder.write("No students found in the database.")
                except Exception as e:
                    st.error(f"Error fetching student data: {str(e)}")

            if st.button("Show Students Table"):
                render_student_table()

            # State for showing the modification form
            if "show_form_modif_student" not in st.session_state:
                st.session_state.show_form_modif_student = False

            # Button to show the modification form
            if st.button("Modify Student Record"):
                st.session_state.show_form_modif_student = True

            if st.session_state.show_form_modif_student:
                with st.form(key="modify_student_form"):
                    st.write("Modify a Student Record")
                    student_id_to_modify = st.number_input("Enter Student ID to modify", min_value=1, step=1)
                    user_id = st.number_input("Enter User ID to modify", min_value=1, step=1)
                    first_name = st.text_input("First Name")
                    last_name = st.text_input("Last Name")
                    date_of_birth = st.date_input("Date of Birth")
                    current_academic_year = st.number_input("Academic Year", min_value=1, max_value=12, step=1)
                    email = st.text_input("Email")
                    major = st.text_input("Major")
                    enrollment_date = st.date_input("Enrollment Date")
                    password = st.text_input("Password ", type="password")  # Modify password field
                    modify_button = st.form_submit_button("Modify Student")

                if modify_button:
                    try:
                        success = ctrl_modify_student(
                            student_id_to_modify, user_id, first_name, last_name, date_of_birth,
                            current_academic_year, email, major, enrollment_date,
                            password.strip() if password else None
                        )
                        if success:
                            st.success(f"Student with ID {student_id_to_modify} modified successfully!")
                            render_student_table()  # Refresh the table
                        else:
                            st.error(f"Failed to modify student with ID {student_id_to_modify}.")
                    except ValueError as e:
                        st.error(str(e))
                    except Exception as e:
                        st.error(f"Unexpected error: {str(e)}")

            if "show_form_del_student" not in st.session_state:
                st.session_state.show_form_del_student = False

            # Button to show the delete form
            if st.button("Delete Student Record"):
                st.session_state.show_form_del_student = True

            if st.session_state.show_form_del_student:
                with st.form(key="delete_student_form"):
                    st.write("Delete a Student Record")
                    student_id_to_delete = st.number_input("Enter Student ID to delete", min_value=1, step=1)
                    user_id_delete = st.number_input("Enter User ID to delete", min_value=1, step=1)
                    last_name_delete = st.text_input("Last Name")
                    delete_button = st.form_submit_button("Delete Student")

                    if delete_button:
                        try:
                            delete_success = ctrl_delete_student(student_id_to_delete, user_id_delete, last_name_delete)
                            if delete_success:
                                st.success(f"Student with ID {student_id_to_delete} deleted successfully!")
                                render_student_table()  # Refresh the table
                            else:
                                st.error(f"Failed to delete student with ID {student_id_to_delete}.")
                        except ValueError as e:
                            st.error(str(e))
                        except Exception as e:
                            st.error(f"Unexpected error: {str(e)}")
      
        with tab3:
            st.subheader("Add Teacher")
        
            # Form to add a teacher
            with st.form(key="add_teacher_form"):
                first_name = st.text_input("First Name")
                last_name = st.text_input("Last Name")
                date_of_birth = st.date_input("Date of Birth", min_value=date(1900, 1, 1))
                email = st.text_input("Email")
                enrollment_date = st.date_input("Enrollment Date", min_value=date(2000, 1, 1))
                department = st.text_input("Department")
                courses_taught = st.text_area("Courses Taught (comma-separated)")
                password = st.text_input("Password", type="password")
                submit_button = st.form_submit_button(label="Add Teacher")
            
                if submit_button:
                    try:
                        success = ctrl_add_teacher(
                            first_name, last_name, date_of_birth, email,
                            enrollment_date, department, courses_taught, password
                        )
                        if success:
                            st.success(f"Teacher {first_name} {last_name} added successfully!")
                        else:
                            st.error("Failed to add teacher. Please check the details and try again.")
                    except ValueError as e:
                        st.error(str(e))
                    except Exception as e:
                        st.error(f"Unexpected error occurred: {str(e)}")

             
        with tab4:
            st.subheader("View and Modify Teachers")
            placeholder = st.empty()  # Placeholder for the table

            # Function to render the teacher table
            def render_teacher_table():
                try:
                    rows, columns = ctrl_view_teachers()
                    if rows:
                        df = pd.DataFrame(rows, columns=columns)
                        placeholder.dataframe(df)  # Update the placeholder with the DataFrame
                    else:
                        placeholder.write("No teachers found in the database.")
                except Exception as e:
                    st.error(f"Failed to load teacher data: {str(e)}")

            if st.button("Show Teachers Table"):
                render_teacher_table()

            # State for showing the modification form
            if "show_form2" not in st.session_state:
                st.session_state.show_form2 = False

            # Button to show the modification form
            if st.button("Modify Teacher Record"):
                st.session_state.show_form2 = True

            if st.session_state.show_form2:
                with st.form(key="modify_teacher_form"):
                    teacher_id_to_modify = st.number_input("Enter Teacher ID to modify", min_value=1, step=1)
                    user_id = st.number_input("Enter User ID to modify", min_value=1, step=1)
                    first_name = st.text_input("First Name")
                    last_name = st.text_input("Last Name")
                    date_of_birth = st.date_input("Date of Birth")
                    email = st.text_input("Email")
                    enrollment_date = st.date_input("Enrollment Date")
                    department = st.text_input("Department")
                    courses_taught = st.text_area("Courses Taught (comma-separated)")
                    password = st.text_input("Password (Leave empty to keep unchanged)", type="password")
                    modify_button = st.form_submit_button("Modify Teacher")

                if modify_button:
                    try:
                        success = ctrl_modify_teacher(
                            teacher_id_to_modify, user_id, first_name, last_name, date_of_birth,
                            email, enrollment_date, department, courses_taught, password.strip() if password else None
                        )
                        if success:
                            st.success(f"Teacher with ID {teacher_id_to_modify} modified successfully!")
                            render_teacher_table()  # Refresh the table
                        else:
                            st.error(f"Failed to modify teacher with ID {teacher_id_to_modify}.")
                    except ValueError as e:
                        st.error(str(e))
                    except Exception as e:
                        st.error(f"Unexpected error occurred: {str(e)}")

            # State for showing the delete form
            if "show_form_del_teacher" not in st.session_state:
                st.session_state.show_form_del_teacher = False

            # Button to show the delete form
            if st.button("Delete Teacher Record"):
                st.session_state.show_form_del_teacher = True

            if st.session_state.show_form_del_teacher:
                with st.form(key="delete_teacher_form"):
                    st.write("Delete a Teacher Record")
                    teacher_id_to_delete = st.number_input("Enter Teacher ID to delete", min_value=1, step=1)
                    teacher_user_id_delete = st.number_input("Enter User ID to delete", min_value=1, step=1)
                    teacher_last_name_delete = st.text_input("Last Name")
                    teacher_delete_button = st.form_submit_button("Delete Teacher")

                if teacher_delete_button:
                    try:
                        delete_success_teacher = ctrl_delete_teacher(
                            teacher_id_to_delete, teacher_user_id_delete, teacher_last_name_delete
                        )
                        if delete_success_teacher:
                            st.success(f"Teacher with ID {teacher_id_to_delete} deleted successfully!")
                            render_teacher_table()  # Refresh the table
                        else:
                            st.error(f"Failed to delete teacher with ID {teacher_id_to_delete}.")
                    except ValueError as e:
                        st.error(str(e))
                    except Exception as e:
                        st.error(f"Unexpected error occurred: {str(e)}")


    elif menu_option == "Manage Admin & Users":
        st.header("Manage Admin & Users")
        st.write("Here you can manage Admins & LogInUsers.")
        

    elif menu_option == "Manage Classes":

        st.header("Manage Classes")
        tab1, tab2, tab3, tab4 = st.tabs([ "Create Course","View and Modify Courses", "Assign Students to Course", "View and Modify Students by Course"])

        with tab1:
            st.header("Create a New Course")
            with st.form(key="create_course_form"):
                course_name = st.text_input("Course Name")
                description = st.text_area("Description")
                credit_hours = st.number_input("Credit Hours", min_value=1, max_value=10, step=1)
                department = st.text_input("Department")
                teacher_id = st.number_input("Teacher ID ", min_value=0, step=1, value=0)
                day_of_week = st.selectbox("Day of the Week", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
                start_time = st.time_input("Start Time")
                end_time = st.time_input("End Time")
                semester = st.text_input("Semester ")
                max_students = st.number_input("Max Students", min_value=1, step=1)

                submit_button = st.form_submit_button("Create Course")

                if submit_button:
                    # Convert teacher_id to None if not provided
                    teacher_id = teacher_id if teacher_id > 0 else None

                    # Call the function to create the course
                    try:
                        success = ctrl_create_course_in_db(
                            course_name, description, credit_hours, department, teacher_id,
                            day_of_week, start_time, end_time, semester, max_students
                        )

                        if success:
                            st.success(f"The course '{course_name}' was created successfully!")
                        else:
                            st.error("Failed to create the course. Please check the details and try again.")
                    except ValueError as e:
                        st.error(str(e))
                    except Exception as e:
                        st.error(f"Unexpected error occurred: {str(e)}")

        with tab2:
            st.subheader("View and Modify Courses")
            placeholder = st.empty()  # Placeholder to display courses

            # Function to render the courses data in a table
            def render_courses_table():
                try:
                    rows, columns = ctrl_view_courses()
                    if rows and columns:
                        # Create DataFrame and fill NaN values
                        df = pd.DataFrame(rows, columns=columns).fillna("N/A")
                        # Update placeholder with the DataFrame
                        placeholder.dataframe(df)
                    else:
                        placeholder.write("No courses found in the database.")
                except Exception as e:
                    st.error(f"Failed to load courses: {str(e)}")

            if st.button("Show Courses"):
                    render_courses_table()

    
        with tab3:
            st.header("Add Student to Course")

            # Input fields
            student_id = st.number_input("Enter Student ID", min_value=1, step=1)
            course_id = st.number_input("Enter Course ID", min_value=1, step=1)

            # Submit button
            if st.button("Add Student to Course"):
                try:
                    # Call the business logic
                    success = ctrl_add_student_to_course(student_id, course_id)

                    # Display appropriate message
                    if success:
                        st.success(f"Student ID {student_id} has been successfully added to Course ID {course_id}.")
                    else:
                        st.error(f"Failed to add Student ID {student_id} to Course ID {course_id}. Please check the details and try again.")
                except ValueError as e:
                    st.error(str(e))
                except Exception as e:
                    st.error(f"Unexpected error occurred: {str(e)}")

        
        with tab4:
            """
            Streamlit interface to display all students enrolled in a specific course.
            """
            st.header("View Students Enrolled in a Course")

            # Input to choose a course_id
            course_id = st.number_input("Enter Course ID", min_value=1, step=1, key='course_id_input')

            # Button to fetch data
            if st.button("Get Enrolled Students"):
                try:
                    # Fetch data using the business layer
                    rows, columns = ctrl_get_students_in_course(course_id)

                    if rows and columns:
                        # Convert to Pandas DataFrame
                        df = pd.DataFrame(rows, columns=columns)
                        st.subheader(f"Students Enrolled in Course ID: {course_id}")
                        st.dataframe(df)  # Display the DataFrame
                    else:
                        st.warning(f"No students found for Course ID: {course_id}.")
                except ValueError as e:
                    st.error(str(e))
                except Exception as e:
                    st.error(f"Unexpected error occurred: {str(e)}")



    elif menu_option == "View Reports":
        st.header("View Reports")
        st.write("Here you can view detailed reports on students, courses, attendance, and grades.")

        # Admin Reports Menu
        report_type = st.selectbox(
            "Select Report Type",
            ["Attendance Report", "Grade Report", "Course Enrollment Report","Enrollment Pie Charts","Find Top Students per Course"]
        )

        if report_type == "Attendance Report":
            generate_attendance_report()

        elif report_type == "Grade Report":
            generate_grade_report()

        elif report_type == "Course Enrollment Report":
            generate_course_enrollment_report()
        
        elif report_type == "Enrollment Pie Charts":
            generate_enrollment_pie_charts()
        
        elif report_type == "Find Top Students per Course":
            generate_top_students_report()

    
    elif menu_option == "Manage Messages":
        st.header("Manage Messages")
        tab1, tab2 = st.tabs(["Create Message", "View Messages"])

        # Create Message Tab
        with tab1:
            st.subheader("Create a New Message")

            with st.form(key="create_message_form"):
                course_id = st.number_input("Course ID", min_value=1, step=1)
                only_prof = st.checkbox("Only for Professors")
                if only_prof==False:
                    only_prof1=0
                else:
                    only_prof1=1
                content = st.text_area("Message Content", max_chars=100)
                submit_button = st.form_submit_button("Create Message")

                if submit_button:
                    
                    # Call a controller function to insert the message into the database
                    try:
                        success = create_message(course_id, only_prof1, content)

                        if success:
                            st.success("Message created successfully!")
                        else:
                            st.error("Failed to create the message. Please try again.")
                    except ValueError as e:
                        st.error(str(e))
                    except Exception as e:
                        st.error(f"Unexpected error occurred: {str(e)}")

        # View Messages Tab
        with tab2:
            st.subheader("View All Messages")
            placeholder = st.empty()

            if st.button("Load Messages"):
                try:
                    rows, columns = fetch_messages()

                    if rows and columns:
                        df = pd.DataFrame(rows, columns=columns)
                        placeholder.dataframe(df)  # Display the messages in a table
                    else:
                        st.warning("No messages found in the database.")
                except Exception as e:
                    st.error(f"Failed to load messages: {str(e)}")





    elif menu_option == "Settings":
        st.header("Settings")
        st.write("Update application settings.")

if __name__ == "__main__":
    admin_page()