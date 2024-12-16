import streamlit as st

from business.teacher_Ctrl import ctrl_retrieve_teacher_info,ctrl_layer_get_teacher_courses, ctrl_layer_get_students_in_class,ctrl_assign_grades_to_students, ctrl_layer_get_class_grades, ctrl_save_attendance

def teacher_page():
    """Teacher dashboard."""
    # Sidebar menu
    st.sidebar.title("Teacher Menu")
    menu_option = st.sidebar.radio(
        "Navigation",
        options=["Personal Information", "View Schedule", "View Classes & Assign Grades","View Grades","Mark Attendance", "Settings"]
    )
    
    st.title("📘 Teacher Dashboard")
    st.write("Welcome to the Teacher Dashboard!")

    if menu_option == "Personal Information":
        st.header("Personal Information")
        st.write("Here you can view your personal information.")
        # Add fields or logic for displaying and editing personal information
                # Retrieve user_id from session state
        user_id = st.session_state.get("user_id")
        if user_id:
            # Retrieve teacher information
            teacher_info = ctrl_retrieve_teacher_info(user_id)
            
            if teacher_info:
                # Display teacher information
                st.write(f"**Name:** {teacher_info['first_name']} {teacher_info['last_name']}")
                st.write(f"**Date of Birth:** {teacher_info['date_of_birth']}")
                st.write(f"**Email:** {teacher_info['email']}")
                st.write(f"**Enrollment Date:** {teacher_info['enrollment_date']}")
                st.write(f"**Department:** {teacher_info['department']}")
                st.write(f"**Courses Taught:** {teacher_info['courses_taught']}")
                st.write(f"**Password:** {teacher_info['password']}")
            else:
                st.error("No teacher information found.")
        else:
            st.error("You are not logged in. Please log in to view your personal information.")


    elif menu_option == "View Schedule":
        st.header("View Schedule")
        st.write("Here is your teaching schedule.")

        # Retrieve user_id from session state
        user_id = st.session_state.get("user_id")

        if user_id:
            try:
                # Get courses through the business layer
                courses = ctrl_layer_get_teacher_courses(user_id)

                if courses:
                    # Days of the week in desired order
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




    elif menu_option == "View Classes & Assign Grades":
        st.header("View Classes & Assign Grades")
        st.write("Here you can view your classes, the students enrolled in them, and assign multiple grades.")

        # Retrieve user_id from session state
        user_id = st.session_state.get("user_id")

        if user_id:
            try:
                # Fetch all classes taught by the teacher
                classes = ctrl_layer_get_teacher_courses(user_id)

                if classes:
                    # Prepare a list of class names for selection
                    class_names = [cls["course_name"] for cls in classes]
                    selected_class = st.selectbox("Select Class", class_names)

                    if selected_class:
                        # Fetch student data for the selected class
                        students = ctrl_layer_get_students_in_class(selected_class)

                        if students:
                            st.write(f"Students in {selected_class}:")
                            student_grades = {}

                            for student in students:
                                student_id = student["student_id"]
                                student_name = student["name"]

                                # Create input fields for multiple grades
                                student_grades[student_id] = []
                                grade_count = st.number_input(
                                    f"Number of grades to assign for {student_name} (ID: {student_id}):",
                                    min_value=1,
                                    step=1,
                                    key=f"grade_count_{student_id}"
                                )

                                for i in range(grade_count):
                                    grade_type = st.text_input(
                                        f"Grade Type {i+1} for {student_name} (ID: {student_id}):",
                                        key=f"grade_type_{student_id}_{i}"
                                    )
                                    grade = st.text_input(
                                        f"Grade {i+1} for {student_name} (ID: {student_id}):",
                                        key=f"grade_{student_id}_{i}"
                                    )

                                    if grade.strip() and grade_type.strip():
                                        student_grades[student_id].append({
                                            "grade_type": grade_type,
                                            "grade": grade
                                        })

                            # Submit button to assign grades
                            if st.button("Submit Grades"):
                                success = ctrl_assign_grades_to_students(user_id, selected_class, student_grades)

                                if success:
                                    st.success("Grades successfully assigned!")
                                else:
                                    st.error("Failed to assign grades. Please try again.")
                        else:
                            st.info(f"No students found in {selected_class}.")
                else:
                    st.info("You are not teaching any classes.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.error("You are not logged in. Please log in to view your classes.")




    elif menu_option == "View Grades":
        st.header("View Grades")
        st.write("Here you can view all the grades for your classes.")

        # Retrieve user_id from session state
        user_id = st.session_state.get("user_id")

        if user_id:
            try:
                # Fetch all classes taught by the teacher
                classes = ctrl_layer_get_teacher_courses(user_id)

                if classes:
                    # Prepare a list of class names for selection
                    class_names = [cls["course_name"] for cls in classes]
                    selected_class = st.selectbox("Select Class", class_names)

                    if selected_class:
                        # Fetch grades for the selected class
                        grades = ctrl_layer_get_class_grades(user_id, selected_class)

                        if grades:
                            st.write(f"Grades for {selected_class}:")
                            grades_data = {
                                "Student ID": [grade["student_id"] for grade in grades],
                                "First Name": [grade["first_name"] for grade in grades],
                                "Last Name": [grade["last_name"] for grade in grades],
                                "Grade": [grade["grade"] for grade in grades],
                            }
                            st.table(grades_data)
                        else:
                            st.info(f"No grades found for {selected_class}.")
                    else:
                        st.info("Please select a class.")
                else:
                    st.info("You are not teaching any classes.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.error("You are not logged in. Please log in to view grades.")

    elif menu_option == "Mark Attendance":
        st.header("Mark Attendance")
        st.write("Here you can mark students as present or absent for a specific class.")

        # Retrieve user_id from session state
        user_id = st.session_state.get("user_id")

        if user_id:
            try:
                # Fetch all classes taught by the teacher
                classes = ctrl_layer_get_teacher_courses(user_id)

                if classes:
                    # Prepare a list of class names for selection
                    class_names = [cls["course_name"] for cls in classes]
                    selected_class = st.selectbox("Select Class", class_names)

                    if selected_class:
                        # Fetch student data for the selected class
                        students = ctrl_layer_get_students_in_class(selected_class)

                        if students:
                            st.write(f"Mark attendance for {selected_class}:")
                            attendance_records = {}

                            for student in students:
                                student_id = student["student_id"]
                                student_name = student["name"]

                                # Create a checkbox for marking attendance
                                is_present = st.checkbox(
                                    f"{student_name} (ID: {student_id})", 
                                    key=f"attendance_{student_id}"
                                )
                                attendance_records[student_id] = is_present

                            # Submit button to save attendance
                            if st.button("Submit Attendance"):
                                success = ctrl_save_attendance(user_id, selected_class, attendance_records)

                                if success:
                                    st.success("Attendance successfully recorded!")
                                else:
                                    st.error("Failed to record attendance. Please try again.")
                        else:
                            st.info(f"No students found in {selected_class}.")
                else:
                    st.info("You are not teaching any classes.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.error("You are not logged in. Please log in to mark attendance.")



    elif menu_option == "Settings":
        st.header("Settings")
        st.write("Update your preferences and account settings.")
        
    
    

