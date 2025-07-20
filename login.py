import csv

# Dictionary to simulate session storage
sessions = {}

def handle_login(email: str, password: str, role: str):
    def check_login(email, password, file_name, email_field, password_field):
        try:
            with open(file_name, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row[email_field].strip().lower() == email.strip().lower():
                        if row[password_field] == password:
                            return row  # Return the full row (user's details)
                        else:
                            return "wrong_password"
            return "not_found"
        except Exception as e:
            print(f"Error during login: {e}")
            return "error"

    if role == "faculty":
        user_details = check_login(email, password, 'faculty.csv', 'email', 'password')
    elif role == "student":
        user_details = check_login(email, password, 'students.csv', 'email', 'password')
    else:
        return {"success": False, "message": "Invalid role selected."}

    if isinstance(user_details, dict):  # Successful login
        # Store session locally (using email as key, and user details as value)
        session_id = f"{email}_{role}"
        sessions[session_id] = user_details

        return {
            "success": True,
            "message": "Login successful.",
            "role": role,
            "session_id": session_id
        }
    elif user_details == "wrong_password":
        return {"success": False, "message": "Incorrect password."}
    elif user_details == "not_found":
        return {"success": False, "message": "User not found. Please sign up first."}
    else:
        return {"success": False, "message": "Server error while reading CSV."}