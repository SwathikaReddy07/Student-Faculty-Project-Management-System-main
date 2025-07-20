# new_student.py
import csv

def save_student_details_logic(
    student_id, first_name, middle_name, last_name, gender, email,
    phone, department, branch, year_of_study, skills, cgpa, birthday, password
):
    with open("students.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            student_id,
            first_name,
            middle_name,
            last_name,
            gender,
            email,
            phone,
            department,
            branch,
            year_of_study,
            skills,
            cgpa,
            birthday,
            "",
            "",
            password
        ])
    return {"status": "success", "message": "Student registered successfully"}
