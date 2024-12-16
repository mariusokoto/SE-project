import streamlit as st

from business.student_Ctrl import ctrl_layer_get_student_info, ctrl_layer_get_student_courses, business_layer_get_all_grades_for_course, ctrl_layer_get_attendance_for_course,business_layer_get_mean_grade_for_course

def student_page():
    """Student dashboard."""
    # Sidebar menu
    st.sidebar.title("Student Menu")
    menu_option = st.sidebar.radio(
        "Navigation",
        options=["Personal Information", "View Schedule", "View Grades","View Attendance" , "Settings"]
    )
    
    st.title("📘 Student Dashboard")
    st.write("Welcome to the Student Dashboard!")

    if menu_option == "Personal Information":
        st.header("Personal Information")
        st.write("Here you can view your personal information.")

        user_id = st.session_state.get("user_id")

        if user_id:
            try:
                # Fetch student personal information
                student_info = ctrl_layer_get_student_info(user_id)

                if student_info:
                    st.write(f"**Student ID:** {student_info['student_id']}")
                    st.write(f"**First Name:** {student_info['first_name']}")
                    st.write(f"**Last Name:** {student_info['last_name']}")
                    st.write(f"**Date of Birth:** {student_info['date_of_birth']}")
                    st.write(f"**Current Academic Year:** {student_info['current_academic_year']}")
                    st.write(f"**Email:** {student_info['email']}")
                    st.write(f"**Major:** {student_info['major']}")
                    st.write(f"**Enrollment Date:** {student_info['enrollment_date']}")
                    st.write(f"**Password:** {student_info['password']}")
                else:
                    st.info("No personal information found.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.error("You are not logged in. Please log in to view your personal information.")

    elif menu_option == "View Schedule":
        st.header("View Schedule")
        st.write("Here is your class schedule.")

        # Retrieve user_id from session state
        user_id = st.session_state.get("user_id")

        if user_id:
            try:
                courses = ctrl_layer_get_student_courses(user_id)

                if courses:
                    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

                    # Organize courses by day of the week
                    schedule_by_day = {day: [] for day in days_of_week}

                    for course in courses:
                        day = course["day_of_week"]
                        if day in schedule_by_day:
                            schedule_by_day[day].append(course)

                    # Sort courses within each day by start time
                    for day in days_of_week:
                        schedule_by_day[day].sort(key=lambda x: x["start_time"])

                    # Display schedule
                    for day in days_of_week:
                        st.subheader(day)

                        if schedule_by_day[day]:
                            for course in schedule_by_day[day]:
                                st.write(f"**Course Name:** {course['course_name']}")
                                st.write(f"**Description:** {course['description']}")
                                st.write(f"**Credits:** {course['credit_hours']}")
                                st.write(f"**Instructor:** {course['teacher_name']}")
                                st.write(f"**Time:** {course['start_time']} - {course['end_time']}")
                                st.write(f"**Semester:** {course['semester']}")
                                st.write("---")
                        else:
                            st.write("No classes scheduled.")
                else:
                    st.info("No courses found in your schedule.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.error("You are not logged in. Please log in to view your schedule.")


    elif menu_option == "View Grades":
        st.header("View Grades")
        st.write("Here you can view all your grades for a specific course.")

        # Retrieve user_id from session state
        user_id = st.session_state.get("user_id")

        if user_id:
            try:
                # Fetch all courses the student is enrolled in
                courses = ctrl_layer_get_student_courses(user_id)

                if courses:
                    # Prepare a list of class names for selection
                    class_names = [course["course_name"] for course in courses]
                    selected_class = st.selectbox("Select a Course", class_names)

                    if selected_class:
                        # Fetch all grades for the selected course
                        grades = business_layer_get_all_grades_for_course(user_id, selected_class)

                        if grades:
                            st.write(f"Your Grades for {selected_class}:")
                            grades_data = {
                                "Grade Type": [grade["grade_type"] for grade in grades],
                                "Grade": [grade["grade"] for grade in grades],
                                "Assigned At": [grade["assigned_at"] for grade in grades],
                            }
                            st.table(grades_data)

                            # Calculate and display the mean grade
                            mean_grade = business_layer_get_mean_grade_for_course(user_id, selected_class)
                            st.write(f"**Mean Grade for {selected_class}: {mean_grade:.2f}**")
                        else:
                            st.info(f"No grades available for {selected_class}.")
                else:
                    st.info("You are not enrolled in any courses.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.error("You are not logged in. Please log in to view your grades.")




    
    elif menu_option == "View Attendance":
        st.header("View Attendance")
        st.write("Here you can view your attendance for specific courses.")

        user_id = st.session_state.get("user_id")

        if user_id:
            try:
                # Fetch all courses the student is enrolled in
                courses = ctrl_layer_get_student_courses(user_id)

                if courses:
                    # Prepare a list of class names for selection
                    class_names = [course["course_name"] for course in courses]
                    selected_class = st.selectbox("Select a Course", class_names)

                    if selected_class:
                        # Fetch attendance for the selected course
                        attendance = ctrl_layer_get_attendance_for_course(user_id, selected_class)

                        if attendance:
                            st.write(f"**Course Name:** {selected_class}")
                            st.write(f"**Attendance Status:** {'Present' if attendance['is_present'] else 'Absent'}")
                            st.write(f"**Marked At:** {attendance['marked_at']}")
                        else:
                            st.info(f"No attendance record found for {selected_class}.")
                else:
                    st.info("You are not enrolled in any courses.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.error("You are not logged in. Please log in to view your attendance.")
