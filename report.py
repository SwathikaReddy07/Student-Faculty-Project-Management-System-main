import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF
import os

def generate_report():
    # Load CSVs
    students = pd.read_csv('students.csv')
    projects = pd.read_csv('projects.csv')
    faculty = pd.read_csv('faculty.csv')
    applications = pd.read_csv('applications.csv')

    # Initialize report variable
    report = f"---- Project Statistics Report ----\n"

    # ===== PROJECT SECTION =====

    # 1. Ongoing projects
    ongoing_projects = projects[projects['status'].fillna('').str.lower().str.strip() == 'open']
    ongoing_count = len(ongoing_projects)

    # 2. Projects proposed by each faculty
    faculty_project_counts = projects.groupby('faculty_id').size().reset_index(name='project_count')
    faculty_project_counts = faculty_project_counts.merge(faculty[['faculty_id', 'first_name', 'last_name']], on='faculty_id')

    # 3. Projects per department
    department_project_counts = projects.groupby('department').size().sort_values(ascending=False)

    # 4. Projects proposed per month (current year)
    projects['created_at'] = pd.to_datetime(projects['created_at'], errors='coerce')
    current_year = datetime.now().year
    projects_this_year = projects[projects['created_at'].dt.year == current_year]
    projects_per_month = projects_this_year['created_at'].dt.month.value_counts().sort_index()

    # 5. Department excelling / needing push
    best_department = department_project_counts.idxmax()
    least_department = department_project_counts.idxmin()

    # Add project section to report
    report += f"\n1. Ongoing Projects: {ongoing_count}\n"
    report += "2. Projects Proposed by Faculty:\n"
    for _, row in faculty_project_counts.iterrows():
        report += f"   - {row['first_name']} {row['last_name']} (ID: {row['faculty_id']}): {row['project_count']}\n"
    report += "\n3. Projects Proposed by Department:\n"
    for dept, count in department_project_counts.items():
        report += f"   - {dept}: {count}\n"
    report += "\n4. Projects Proposed Each Month (Current Year):\n"
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    for month, count in projects_per_month.items():
        report += f"   - {month_names[month-1]}: {count}\n"
    report += f"\n5. Department Excelling in Projects: {best_department}\n"
    report += f"6. Department Needing More Project Initiatives: {least_department}\n"

    # ===== STUDENT SECTION =====

    total_students = len(students)

    # 1. Participation: Assigned & Applied
    accepted_applications = applications[applications['status'].str.lower() == 'accepted']
    assigned_students = accepted_applications['student_id'].nunique()
    applied_students = applications['student_id'].nunique()
    unassigned_students = total_students - assigned_students

    report += f"\n\n---- Student Participation ----\n"
    report += f"7. Students Participating in Projects (Accepted): {assigned_students}\n"
    report += f"8. Students Who Applied for Projects: {applied_students}\n"
    report += f"9. Students Without Any Accepted Projects: {unassigned_students}\n"

    # 4. Department-wise student participation
    student_dept_counts = students[students['student_id'].isin(accepted_applications['student_id'])] \
                                .groupby('department').size().sort_values(ascending=False)
    report += "\n10. Department-wise Student Participation:\n"
    for dept, count in student_dept_counts.items():
        report += f"   - {dept}: {count} students\n"

    # ===== CREATE PDF =====

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Project Statistics Report", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 10, report)

    def save_and_add_plot(fig, filename):
        fig.tight_layout()
        fig.savefig(filename)
        plt.close(fig)
        pdf.ln(10)
        pdf.image(filename, x=10, w=180)
        os.remove(filename)

    # Bar plot - Projects by faculty
    fig = plt.figure(figsize=(10, 6))
    sns.barplot(data=faculty_project_counts, x='first_name', y='project_count',
                hue='last_name', palette='viridis', errorbar=None, dodge=False)
    plt.title('Projects Proposed by Faculty')
    plt.ylabel('Number of Projects')
    plt.xticks(rotation=45, ha='right')
    save_and_add_plot(fig, 'faculty_projects.png')

    # Pie chart - Projects per department
    fig, ax = plt.subplots(figsize=(6, 6))
    wedges, texts, autotexts = ax.pie(department_project_counts, autopct='%1.1f%%', startangle=90)
    legend_labels = [f"{dept} ({auto.get_text()})" for dept, auto in zip(department_project_counts.index, autotexts)]
    ax.legend(wedges, legend_labels, title="Departments", loc="upper left", bbox_to_anchor=(1, 1))
    ax.set_title('Projects Distribution by Department')
    save_and_add_plot(fig, 'department_projects.png')

    # Line plot - Projects per month
    fig = plt.figure(figsize=(10, 6))
    plt.plot(projects_per_month.index, projects_per_month.values, marker='o', color='b')
    plt.title('Projects Proposed Per Month (Current Year)')
    plt.xlabel('Month')
    plt.ylabel('Number of Projects')
    plt.xticks(range(1, 13), month_names)
    save_and_add_plot(fig, 'monthly_projects.png')

    # Bar chart - Department-wise student participation
    fig = plt.figure(figsize=(8, 5))
    sns.barplot(x=student_dept_counts.index, y=student_dept_counts.values, palette='Set2')
    plt.title('Student Participation by Department')
    plt.ylabel('Number of Students')
    plt.xticks(rotation=45)
    save_and_add_plot(fig, 'student_participation.png')

    # Save final PDF
    output_pdf = 'project_statistics_report.pdf'
    pdf.output(output_pdf)
    print(f"✅ Report generated and saved as {output_pdf}")

if __name__ == "__main__":
    generate_report()
