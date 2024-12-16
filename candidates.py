import pandas as pd
import random

# Define the number of rows in the dataset
num_rows = 500

# Predefined skill pools for each job title
skills_by_job_title = {
    "Software Engineer": ["Java", "Python", "C++", "JavaScript", "React", "Node.js", "SQL"],
    "Data Scientist": ["Python", "R", "SQL", "Machine Learning", "Deep Learning", "Pandas", "Scikit-learn"],
    "Product Manager": ["Agile", "Scrum", "Project Management", "Communication", "Market Research", "Roadmapping", "Stakeholder Management"],
    "Graphic Designer": ["Adobe Photoshop", "Illustrator", "UI/UX Design", "Typography", "Sketch", "InVision", "Figma"],
    "Accountant": ["Excel", "QuickBooks", "Tax Filing", "Financial Analysis", "Payroll Management", "Auditing", "SAP"],
    "HR Specialist": ["Recruitment", "Employee Relations", "HR Policies", "Payroll", "Training", "Onboarding", "Compliance"]
}

job_titles = list(skills_by_job_title.keys())  # Job titles will be the keys of the skill pools
job_types = job_titles  # Each candidate's job type is one of these job titles

locations = ["Gurgaon", "Mumbai", "Chennai", "Bangalore", "Noida", "Hyderabad"]
degrees = ["High School", "Bachelor's", "Master's", "PhD"]

# Helper functions to generate random data
def generate_skills(job_title):
    """Generate a random set of skills based on the job title."""
    skills_pool = skills_by_job_title.get(job_title, [])
    # Candidate will have 3 to 5 skills from the specific pool
    return ", ".join(random.sample(skills_pool, random.randint(3, 5)))

def generate_salary():
    """Generate a random expected salary in dollars."""
    return round(random.uniform(30000, 150000), -3)

def generate_experience():
    """Generate random experience in years (0 to 20)."""
    return random.randint(0, 20)

def generate_remote():
    """Generate random remote work preference."""
    return random.choice(["Yes", "No"])

# Generate the dataset
data = {
    "CandidateID": list(range(1, num_rows + 1)),
    "Job Type": [random.choice(job_types) for _ in range(num_rows)],  # Assign job type randomly from the job_titles list
    "Skills": [],  # Skills will be generated based on Job Type
    "Experience (Years)": [generate_experience() for _ in range(num_rows)],
    "Location": [random.choice(locations) for _ in range(num_rows)],
    "Degree": [random.choice(degrees) for _ in range(num_rows)],
    "Expected Salary": [generate_salary() for _ in range(num_rows)],
    "Remote": [generate_remote() for _ in range(num_rows)],
}

# Populate the "Skills" field based on the job title (Job Type)
for job_title in data["Job Type"]:
    data["Skills"].append(generate_skills(job_title))

# Create a DataFrame
candidate_df = pd.DataFrame(data)

# Save the dataset to a CSV file
candidate_df.to_csv("candidate_mock_data.csv", index=False)

# Display the first few rows
print(candidate_df.head())
