import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# Load the data
candidate_df = pd.read_csv('candidate_mock_data.csv')
job_df = pd.read_csv('job_mock_data.csv')

def clean_salary(salary):
    """Clean salary values by removing commas and converting to float"""
    if isinstance(salary, str):
        return float(salary.replace(',', ''))
    return float(salary)

def calculate_skill_match(candidate_skills, job_skills):
    """Calculate the percentage of job skills that match with candidate skills"""
    candidate_skills_list = [skill.strip() for skill in candidate_skills.split(',')]
    job_skills_list = [skill.strip() for skill in job_skills.split(',')]
    
    matches = sum(1 for skill in job_skills_list if any(s in skill or skill in s for s in candidate_skills_list))
    return (matches / len(job_skills_list)) * 100 if job_skills_list else 0

def calculate_degree_match(candidate_degree, required_degree):
    """Calculate degree match based on hierarchy"""
    degree_hierarchy = {
        'High School': 1,
        'Bachelor\'s': 2,
        'Master\'s': 3,
        'PhD': 4
    }
    
    candidate_level = degree_hierarchy.get(candidate_degree, 0)
    required_level = degree_hierarchy.get(required_degree, 0)
    
    # If candidate has higher or equal degree level, it's a match
    return 100 if candidate_level >= required_level else 0

def prepare_matching_data():
    """Prepare cross-product of candidates and jobs with feature engineering"""
    # Clean salary columns
    candidate_df['Expected_Salary_Clean'] = candidate_df['Expected Salary'].apply(clean_salary)
    job_df['Salary_Offered_Clean'] = job_df['Salary Offered (In INR)'].apply(clean_salary)
    
    # Create cross product
    matches = []
    
    for _, candidate in candidate_df.iterrows():
        for _, job in job_df.iterrows():
            # Calculate features
            skill_match = calculate_skill_match(candidate['Skills'], job['Required Skills'])
            
            experience_match = 100 if candidate['Experience (Years)'] >= job['Min Experience (Years)'] else \
                             (candidate['Experience (Years)'] / job['Min Experience (Years)'] * 100 if job['Min Experience (Years)'] > 0 else 100)
            
            degree_match = calculate_degree_match(candidate['Degree'], job['Degree Requirement'])
            
            salary_match = 100 if candidate['Expected_Salary_Clean'] <= job['Salary_Offered_Clean'] else \
                          (job['Salary_Offered_Clean'] / candidate['Expected_Salary_Clean'] * 100)
            
            location_match = 100 if candidate['Location'] == job['Location'] else 0
            
            remote_match = 100 if (job['Remote Allowed'] == 'Yes' and candidate['Remote'] == 'Yes') or \
                                 (job['Remote Allowed'] == 'No' and candidate['Remote'] == 'No') else 0
            
            # Calculate weighted match score
            weighted_match = (
                skill_match * 0.70 +      # 70% weight for skills
                experience_match * 0.05 +  # 5% weight for experience
                degree_match * 0.10 +      # 10% weight for degree
                salary_match * 0.10 +      # 10% weight for salary
                remote_match * 0.025 +     # 2.5% weight for remote preference
                location_match * 0.025     # 2.5% weight for location
            )
            
            matches.append({
                'CandidateID': candidate['CandidateID'],
                'JobID': job['JobID'],
                'Skill_Match': skill_match,
                'Experience_Match': experience_match,
                'Degree_Match': degree_match,
                'Salary_Match': salary_match,
                'Location_Match': location_match,
                'Remote_Match': remote_match,
                'Total_Match_Score': weighted_match,
                'Is_Match': weighted_match >= 60  # Consider it a match if total weighted score is >= 70%
            })
    
    return pd.DataFrame(matches)

def get_top_matches(match_df, n=5):
    """Get top N matches for each candidate"""
    return match_df.sort_values('Total_Match_Score', ascending=False) \
                  .groupby('CandidateID') \
                  .head(n)

def main():
    # Generate all matches
    print("Generating matches...")
    matches_df = prepare_matching_data()
    
    # Get top 5 matches for each candidate
    top_matches = get_top_matches(matches_df, n=5)
    
    # Save results
    matches_df.to_csv('all_matches.csv', index=False)
    
    # Print summary statistics
    print("\nMatching Summary:")
    print(f"Total possible combinations: {len(matches_df)}")
    print(f"Number of successful matches (>= 60% match score): {len(matches_df[matches_df['Is_Match']])}")
    print(f"Average match score: {matches_df['Total_Match_Score'].mean():.2f}%")

if __name__ == "__main__":
    main()