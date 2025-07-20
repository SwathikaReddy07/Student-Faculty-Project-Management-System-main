# new_faculty.py
import csv

def save_faculty_details_logic(
    faculty_id, first_name, middle_name, last_name, email,
    phone_number, department, role, expertise, password
):
    with open("faculty.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            faculty_id,
            first_name,
            middle_name,
            last_name,
            email,
            phone_number,
            department,
            role,
            expertise,
            "",
            password
        ])
    return {"status": "success", "message": "Faculty registered successfully"}
