# session_store.py

session_data = {
    "email": None,
    "role": None
}

def set_session(email: str, role: str):
    session_data["email"] = email
    session_data["role"] = role

def get_session():
    return session_data
