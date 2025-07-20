import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
import uuid

fake = Faker()

# === CONFIGURATION === #
num_faculty = 30
num_projects = 60
num_students = 100
num_applications = 50
num_meetings = 50

# === PRESETS === #
departments = [
    "Computer Science", "Electrical Engineering", "Mechanical Engineering", 
    "Civil Engineering", "Artificial Intelligence", "Computational Biology", 
    "Computational Mathematics", "Electronics and Communication", 
    "Electronics and Computation", "Bio Technology"
]

dept_to_branch = {
    "Artificial Intelligence": "ari",
    "Computational Biology": "cab",
    "Computational Mathematics": "cam",
    "Computer Science": "cse",
    "Electronics and Computation": "ecm",
    "Electronics and Communication": "ece",
    "Mechanical Engineering": "mec",
    "Civil Engineering": "civ",
    "Bio Technology": "bit",
    "Electrical Engineering": "eee"
}

roles = ["Professor", "Associate Professor", "Assistant Professor"]
expertise_pool = ["AI", "Machine Learning", "Data Science", "Embedded Systems", "Cybersecurity", "Networking"]
skills_pool = ["Python", "Machine Learning", "Data Analysis", "Web Development", "Embedded Systems", "Networking"]

branch_counters = {branch: 1 for branch in dept_to_branch.values()}
faculty_list = []
projects_list = []
students_list = []

# === FACULTY === #
faculty_ids = []
faculty_projects_map = {}
for _ in range(num_faculty):
    first_name = fake.first_name()
    middle_name = fake.first_name() if random.random() > 0.7 else ""
    last_name = fake.last_name()
    department = random.choice(departments)
    branch_code = dept_to_branch[department]
    initials = first_name[0] + (middle_name[0] if middle_name else "") + last_name[0]
    faculty_id = f"{initials.lower()}_{branch_code}"
    
    faculty_ids.append(faculty_id)
    email = f"{first_name.lower()}.{last_name.lower()}@mahindrauniversity.edu.in"
    phone_number = f"(+91) {random.choice([6, 7, 8, 9])}{random.randint(100000000, 999999999)}"
    role = random.choice(roles)
    expertise = random.sample(expertise_pool, k=random.randint(1, 3))
    password = ''.join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890", k=10))
    faculty_projects_map[faculty_id] = []

    faculty_list.append([faculty_id, first_name, middle_name, last_name, email, phone_number,
                         department, role, expertise, [], password])

# === PROJECTS === #
for _ in range(num_projects):
    faculty_idx = random.randint(0, num_faculty - 1)
    faculty = faculty_list[faculty_idx]
    faculty_id = faculty[0]
    first_name = faculty[1]
    last_name = faculty[3]
    department = faculty[6]
    prof_initials = (first_name[0] + last_name[0]).lower()
    field_initial = department.split()[0].lower()
    project_number = len(faculty_projects_map[faculty_id]) + 1
    project_id = f"{prof_initials}_{field_initial}_{project_number:02d}"

    title = fake.sentence(nb_words=4)
    skills_required = random.sample(skills_pool, k=random.randint(2, 4))
    overview = fake.paragraph(nb_sentences=3)
    created_at = fake.date_between(start_date="-1y", end_date="today")
    deadline = created_at + pd.Timedelta(days=random.randint(30, 120))
    status = "Open"
    application_link = random.choice(["https://forms.google.com/", "https://forms.microsoft.com/"]) + str(project_id)

    faculty_projects_map[faculty_id].append(project_id)

    projects_list.append([project_id, title, f"{first_name} {last_name}", faculty_id, department, skills_required,
                          overview, created_at, deadline, status, [], application_link])

# === STUDENTS === #
project_ids = [p[0] for p in projects_list]
for _ in range(num_students):
    department = random.choice(departments)
    branch = dept_to_branch[department]
    counter = branch_counters[branch]
    branch_counters[branch] += 1

    year_of_study = random.randint(1, 4)
    student_id = f"se{datetime.now().year - year_of_study - 2000}u{branch}{counter:03d}"
    email = f"{student_id}@mahindrauniversity.edu.in"

    first_name = fake.first_name()
    middle_name = fake.first_name() if random.random() > 0.7 else ""
    last_name = fake.last_name()
    gender = random.choice(["Male", "Female", "Other"])
    phone_number = f"(+91) {random.choice([6, 7, 8, 9])}{random.randint(100000000, 999999999)}"
    skills = random.sample(skills_pool, k=random.randint(2, 5))
    cgpa = round(random.uniform(6.0, 10.0), 2)
    password = f"{student_id}@{first_name}"
    
    # Generate birthday (between 18-24 years ago)
    birth_year = datetime.now().year - random.randint(18, 24)
    birthday = fake.date_of_birth(tzinfo=None, minimum_age=18, maximum_age=24)

    applied_projects = random.sample(project_ids, k=random.randint(1, 5))
    application_ids = [f"{pid}@{student_id}" for pid in applied_projects]

    for pid in applied_projects:
        for project in projects_list:
            if project[0] == pid:
                project[10].append(student_id)

    students_list.append([student_id, first_name, middle_name, last_name, gender, email,
                         phone_number, department, branch, year_of_study, skills, cgpa,
                         birthday, applied_projects, application_ids, password])

# === Update Faculty Projects === #
for i in range(len(faculty_list)):
    fid = faculty_list[i][0]
    faculty_list[i][9] = faculty_projects_map[fid]

# === APPLICATIONS === #
applications = []
for _ in range(num_applications):
    student = random.choice(students_list)
    student_id = student[0]
    project_id = random.choice(project_ids)
    application_id = f"{project_id}@{student_id}"
    status = random.choice(["Pending", "Accepted", "Rejected"])
    date_applied = fake.date_between(start_date="-6m", end_date="today")
    updated_at = fake.date_between(start_date=date_applied, end_date="today")
    applications.append([application_id, student_id, project_id, status, date_applied, updated_at])

# === MEETINGS === #
room_numbers = {
    "Faculty Office": [1, 2, 3],
    "Tutorial Room": list(range(1, 8)),
    "Classroom": list(range(1, 19)),
    "Lecture Hall": list(range(1, 8))
}

def generate_venue_short_form(venue):
    venue_parts = venue.split(" ")
    if len(venue_parts) > 2:
        venue_type = " ".join(venue_parts[:-1])
        room = venue_parts[-1]
    else:
        venue_type, room = venue_parts
    if "Faculty Office" in venue_type:
        return f"FO{room}"
    elif "Tutorial Room" in venue_type:
        return f"TR{room}"
    elif "Classroom" in venue_type:
        return f"CR{room}"
    elif "Lecture Hall" in venue_type:
        return f"LH{room}"
    return "UNK"

def generate_meeting_time():
    start_time = datetime.strptime("14:00", "%H:%M")
    end_time = datetime.strptime("18:00", "%H:%M")
    random_time = start_time + (end_time - start_time) * random.random()
    return random_time.strftime("%H:%M")

def generate_meeting_venue():
    venues = [
        "Faculty Office", "Tutorial Room", "Classroom", "Lecture Hall"
    ]
    venue = random.choice(venues)
    room = random.choice(room_numbers[venue])
    return f"{venue} {room}"

meetings = []
for _ in range(num_meetings):
    project = random.choice(projects_list)
    project_id = project[0]
    faculty_id = project[3]
    student_id = random.choice(project[10]) if project[10] else random.choice([s[0] for s in students_list])
    meeting_date = fake.date_between(start_date="today", end_date="+3m")
    meeting_time = generate_meeting_time()
    meeting_venue = generate_meeting_venue()

    venue_short = generate_venue_short_form(meeting_venue)
    meeting_id = f"{project_id}@{meeting_date.strftime('%Y-%m-%d')}_{meeting_time}_{venue_short}"

    meetings.append([meeting_id, project_id, faculty_id, student_id, meeting_date, meeting_time, meeting_venue])

# === SAVE DATA === #
df_faculty = pd.DataFrame(faculty_list, columns=[
    "faculty_id", "first_name", "middle_name", "last_name", "email", "phone_number",
    "department", "role", "expertise", "projects_posted", "password"
])

df_projects = pd.DataFrame(projects_list, columns=[
    "project_id", "title", "professor", "faculty_id", "department", "skills_required", 
    "overview", "created_at", "deadline", "status", "applied_students", "application_link"
])

df_students = pd.DataFrame(students_list, columns=[
    "student_id", "first_name", "middle_name", "last_name", "gender", "email",
    "phone_number", "department", "branch", "year_of_study", "skills", "cgpa",
    "birthday", "projects", "applications", "password"
])

df_applications = pd.DataFrame(applications, columns=[
    "application_id", "student_id", "project_id", "status", "date_applied", "updated_at"
])

df_meetings = pd.DataFrame(meetings, columns=[
    "meeting_id", "project_id", "faculty_id", "student_id", "meeting_date", "meeting_time", "meeting_venue"
])

df_faculty.to_csv("faculty.csv", index=False)
df_projects.to_csv("projects.csv", index=False)
df_students.to_csv("students.csv", index=False)
df_applications.to_csv("applications.csv", index=False)
df_meetings.to_csv("meetings.csv", index=False)
