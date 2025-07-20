from fastapi import FastAPI, Form, Request, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from mako.template import Template
from mako.lookup import TemplateLookup
import csv
import os

# Local module imports
from student_signup import handle_student_signup
from faculty_signup import handle_faculty_signup
from login import handle_login
from new_student import save_student_details_logic
from new_faculty import save_faculty_details_logic
from add_project import add_new_project
from student_projects import get_projects
from session_store import set_session, get_session

app = FastAPI()

# Allow cross-origin requests (development use)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to frontend origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up Mako template directory
mako_lookup = TemplateLookup(directories=['.'])

# Define Pydantic model for a project
class Project(BaseModel):
    project_id: str
    project_title: str
    faculty_name: str
    faculty_id: str
    department: str
    skills: str
    overview: str
    month_proposed: str
    deadline: str
    status: str
    application_link: str

# ------------------ Auth & Signup Routes ------------------

@app.post("/signup")
def signup_faculty(email: str = Form(...), password: str = Form(...), confirm_password: str = Form(...)):
    return handle_faculty_signup(email, password, confirm_password)

@app.post("/student_signup")
def signup_student(email: str = Form(...), password: str = Form(...), confirm_password: str = Form(...)):
    return handle_student_signup(email, password, confirm_password)

@app.post("/login")
def authenticate_user(email: str = Form(...), password: str = Form(...), role: str = Form(...)):
    result = handle_login(email, password, role)
    if result.get("status") == "success":
        set_session(email, role)
        print(f"[DEBUG] Session set: email={email}, role={role}") 
    return result

@app.get("/current_user")
def get_current_user():
    session = get_session()
    print(f"[DEBUG] Session fetched: {session}")
    return session

# ------------------ Student & Faculty Detail Saving ------------------

@app.post("/student_signup_details")
async def save_student_details(
    student_id: str = Form(...),
    first_name: str = Form(...),
    middle_name: str = Form(""),
    last_name: str = Form(...),
    gender: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    department: str = Form(...),
    branch: str = Form(...),
    year_of_study: int = Form(...),
    skills: str = Form(...),
    cgpa: float = Form(...),
    birthday: str = Form(...),
    password: str = Form(...),
):
    return save_student_details_logic(
        student_id, first_name, middle_name, last_name, gender, email,
        phone, department, branch, year_of_study, skills, cgpa, birthday, password
    )

@app.post("/faculty_signup_details")
async def save_faculty_details(
    faculty_id: str = Form(...),
    first_name: str = Form(...),
    middle_name: str = Form(""),
    last_name: str = Form(...),
    email: str = Form(...),
    phone_number: str = Form(...),
    department: str = Form(...),
    role: str = Form(...),
    expertise: str = Form(...),
    password: str = Form(...),
):
    return save_faculty_details_logic(
        faculty_id, first_name, middle_name, last_name, email,
        phone_number, department, role, expertise, password
    )

# ------------------ Project Handling ------------------

@app.post("/add_project")
def add_project(project: Project):
    return add_new_project(project)

@app.get("/projects")
async def fetch_projects():
    return get_projects()

# Function to fetch student data by email
CSV_PATH = "data/students.csv"

@app.get("/api/student/details")
async def get_student_details(request: Request):
    email = request.headers.get("X-User-Email")
    role = request.headers.get("X-User-Role")

    if not email or not role:
        raise HTTPException(status_code=400, detail="Missing email or role in headers.")

    if role.lower() != "student":
        raise HTTPException(status_code=403, detail="Access denied. Only students allowed.")

    if not os.path.exists(CSV_PATH):
        raise HTTPException(status_code=500, detail="students.csv not found.")

    with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["email"].strip().lower() == email.strip().lower():
                return {
                    "student_id": row.get("student_id", ""),
                    "first_name": row.get("first_name", ""),
                    "middle_name": row.get("middle_name", ""),
                    "last_name": row.get("last_name", ""),
                    "gender": row.get("gender", ""),
                    "email": row.get("email", ""),
                    "phone": row.get("phone_number", ""),
                    "department": row.get("department", ""),
                    "branch": row.get("branch", ""),
                    "year_of_study": row.get("year_of_study", ""),
                    "skills": row.get("skills", ""),
                    "cgpa": row.get("cgpa", ""),
                    "birthday": row.get("birthday", ""),
                    "password": row.get("password", ""),
                }

    raise HTTPException(status_code=404, detail="Student not found.")