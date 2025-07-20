import csv
from fastapi.responses import JSONResponse

def load_projects():
    projects = []
    with open('projects.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            projects.append({
                "project_id": row["project_id"],
                "title": row["title"],
                "professor": row["professor"],
                "faculty_id": row["faculty_id"],
                "department": row["department"],
                "skills_required": row["skills_required"],
                "overview": row["overview"],
                "created_at": row["created_at"],
                "deadline": row["deadline"],
                "status": row["status"],
                "applied_students": row["applied_students"],
                "application_link": row["application_link"]
            })
    return projects

def get_projects():
    projects = load_projects()
    return JSONResponse(content={"projects": projects})
