import pandas as pd
import random

# Define the number of rows in the dataset
num_rows = 100

# Predefined lists for generating mock data
job_titles_skills = {
    "Software Engineer": ["Java", "Python", "SQL", "React", "Node.js", "Docker", "Kubernetes"],
    "Data Scientist": ["Python", "R", "SQL", "Machine Learning", "Deep Learning", "Pandas", "Scikit-learn"],
    "Product Manager": ["Agile", "Scrum", "Project Management", "Communication", "Market Research", "Roadmapping", "Stakeholder Management"],
    "Graphic Designer": ["Adobe Photoshop", "Illustrator", "UI/UX Design", "Typography", "Sketch", "InVision", "Figma"],
    "Accountant": ["Excel", "QuickBooks", "Tax Filing", "Financial Analysis", "Payroll Management", "Auditing", "SAP"],
    "Marketing Manager": ["SEO", "Content Marketing", "Google Analytics", "Social Media", "Email Marketing", "PPC", "Market Research"],
    "Sales Executive": ["CRM", "Cold Calling", "Lead Generation", "Negotiation", "Presentation Skills", "Customer Service", "Salesforce"],
    "HR Specialist": ["Recruitment", "Employee Relations", "HR Policies", "Payroll", "Training", "Onboarding", "Compliance"]
}
degree_requirements = ["High School", "Bachelor's", "Master's", "PhD"]
locations = ["Gurgaon", "Mumbai", "Chennai", "Bangalore", "Noida", "Hyderabad"]
salary_ranges = [(300000, 500000), (500000, 700000), (700000, 1000000), (1000000, 1500000)]
remote_allowed_options = ["Yes", "No"]

# Helper functions to generate random data
def generate_skills(job_title):
    """Generate a random set of skills based on the job title."""
    possible_skills = job_titles_skills.get(job_title, [])
    return ", ".join(random.sample(possible_skills, random.randint(3, 4)))

def round_salary(salary):
    """Round the salary to the nearest lakh (100,000) and format it."""
    return f"{round(salary / 100000) * 100000:,}"

def generate_salary():
    """Generate a random salary from predefined ranges, then round it to the nearest lakh."""
    salary_range = random.choice(salary_ranges)
    salary = random.randint(salary_range[0], salary_range[1])
    return round_salary(salary)

def generate_min_experience():
    """Generate random minimum experience in years (0 to 15)."""
    return random.randint(0, 15)

# Generate the dataset
data = {
    "JobID": list(range(1, num_rows + 1)),
    "Title": [random.choice(list(job_titles_skills.keys())) for _ in range(num_rows)],
    "Required Skills": [],
    "Min Experience (Years)": [generate_min_experience() for _ in range(num_rows)],
    "Location": [random.choice(locations) for _ in range(num_rows)],
    "Degree Requirement": [random.choice(degree_requirements) for _ in range(num_rows)],
    "Salary Offered (In INR)": [],
    "Remote Allowed": [random.choice(remote_allowed_options) for _ in range(num_rows)],
}

# Populate the "Required Skills" field and "Salary Offered" field based on job title
for i in range(num_rows):
    job_title = data["Title"][i]
    data["Required Skills"].append(generate_skills(job_title))
    data["Salary Offered (In INR)"].append(generate_salary())

# Create a DataFrame
job_dataset_df = pd.DataFrame(data)

# Save the dataset to a CSV file
job_dataset_df.to_csv("job_mock_data.csv", index=False)

# Display the first few rows
print(job_dataset_df.head())
