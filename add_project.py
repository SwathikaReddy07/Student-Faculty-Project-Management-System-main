# add_project.py
import csv

def add_new_project(project):
    # Add project to projects.csv
    with open("projects.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([  
            project.project_id,
            project.project_title,
            project.faculty_name,
            project.faculty_id,
            project.department,
            project.skills,
            project.overview,
            project.month_proposed,
            project.deadline,
            project.status,
            project.application_link
        ])

    # Update the faculty's record in faculty.csv with the project ID in 'projects_posted'
    faculty_updated = False
    with open("faculty.csv", mode="r", newline="") as file:
        rows = list(csv.reader(file))

    with open("faculty.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        for row in rows:
            # Find the faculty row by faculty_id
            if row[0] == project.faculty_id:
                # Check if the 'projects_posted' column already has projects
                if row[9]:  # Assuming column index 9 is 'projects_posted'
                    row[9] += f', {project.project_id}'  # Append project ID to the existing list
                else:
                    row[9] = project.project_id  # If no projects, add the project ID as the first entry
                faculty_updated = True
            writer.writerow(row)

    if faculty_updated:
        return {"message": "Project added successfully and faculty updated."}
    else:
        return {"message": "Faculty not found. Project added, but faculty not updated."}
