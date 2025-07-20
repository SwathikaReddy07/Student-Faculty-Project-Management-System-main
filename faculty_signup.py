import csv
import os
from utils import check_user_exists

def handle_faculty_signup(email: str, password: str, confirm_password: str):
    file_name = "faculty.csv"
    email_field = "email"

    if password != confirm_password:
        return {"success": False, "message": "Passwords do not match"}

    if check_user_exists(email, file_name, email_field):
        return {"success": False, "message": "Email already registered"}

    return {"success": True, "message": "Faculty sign-up successful."}
