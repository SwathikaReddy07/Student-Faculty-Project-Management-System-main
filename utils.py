import csv

def check_user_exists(email, file_name, email_field):
    try:
        if not email:
            return False

        with open(file_name, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row[email_field].strip().lower() == email.strip().lower():
                    return True
        return False
    except FileNotFoundError:
        return False
    except Exception as e:
        print(f"Error while checking user: {e}")
        return False
