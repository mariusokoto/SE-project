import streamlit as st

from data_access.adminReports import get_attendance_summary,get_course_enrollment_summary,get_course_mean_of_means, get_course_enrollment_data, get_top_students_per_course

def generate_attendance_report():
    st.subheader("Attendance Report")
    try:
        # Fetch attendance summary data
        attendance_data = get_attendance_summary()

        if attendance_data:
            st.write("Attendance Summary by Course:")
            st.table(attendance_data)
        else:
            st.info("No attendance data found.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")



def generate_grade_report():
    st.subheader("Grade Report")
    try:
        # Fetch grade summary data
        grade_report_data = get_course_mean_of_means()

        if grade_report_data:
            st.write("Grade Report - Mean of Mean Grades by Course:")
            grades_data = {
                "Course Name": [row["course_name"] for row in grade_report_data],
                "Mean of Mean Grades": [row["mean_of_means"] for row in grade_report_data],
                "Total Students": [row["total_students"] for row in grade_report_data],
            }
            st.table(grades_data)
        else:
            st.info("No grade data found.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")




def generate_course_enrollment_report():
    st.subheader("Course Enrollment Report")
    try:
        # Fetch enrollment summary data
        enrollment_data = get_course_enrollment_summary()

        if enrollment_data:
            st.write("Enrollment Summary by Course:")
            st.table(enrollment_data)
        else:
            st.info("No enrollment data found.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")




import matplotlib.pyplot as plt

def generate_pie_chart(enrolled, remaining, course_name):
    """
    Generate a pie chart showing enrolled vs. remaining capacity for a course.

    Args:
        enrolled (int): Number of students enrolled in the course.
        remaining (int): Remaining capacity in the course.
        course_name (str): Name of the course.

    Returns:
        matplotlib.figure.Figure: Pie chart figure.
    """
    labels = ["Enrolled", "Remaining Capacity"]
    sizes = [enrolled, remaining]
    colors = ["#ff9999", "#66b3ff"]
    explode = (0.1, 0)  # Explode the "Enrolled" slice

    # Adjust figure size to make it smaller
    fig, ax = plt.subplots(figsize=(3, 3))  # Smaller figure size
    ax.pie(sizes, explode=explode, labels=labels, autopct="%1.1f%%", colors=colors, startangle=90)
    ax.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.set_title(f"{course_name}", fontsize=10)

    return fig




def generate_enrollment_pie_charts():
    st.subheader("Enrollment Pie Charts")
    try:
        # Fetch enrollment data for all courses
        enrollment_data = get_course_enrollment_data()

        if enrollment_data:
            # Use columns to display multiple charts in a row
            col1, col2, col3 = st.columns(3)
            for index, course in enumerate(enrollment_data):
                course_name = course["course_name"]
                enrolled = course["enrolled"]
                capacity = course["capacity"]
                remaining = max(capacity - enrolled, 0)

                # Generate pie chart
                fig = generate_pie_chart(enrolled, remaining, course_name)

                # Display pie charts in columns
                if index % 3 == 0:
                    with col1:
                        st.pyplot(fig)
                elif index % 3 == 1:
                    with col2:
                        st.pyplot(fig)
                elif index % 3 == 2:
                    with col3:
                        st.pyplot(fig)
        else:
            st.info("No enrollment data found.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")


def generate_top_students_report():
    st.subheader("Top Students for Each Course")
    try:
        # Fetch top students for each course
        top_students = get_top_students_per_course()

        if top_students:
            st.write("Top Students by Course:")
            student_data = {
                "Course Name": [row["course_name"] for row in top_students],
                "Student Name": [row["student_name"] for row in top_students],
                "Mean Grade": [row["top_mean_grade"] for row in top_students],
            }
            st.table(student_data)
        else:
            st.info("No student data found.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
