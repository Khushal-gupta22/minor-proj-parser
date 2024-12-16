import pandas as pd

def create_preference_csv_files(top_n):
    """
    Create simple preference CSV files for employers and candidates without headers
    Replace missing preferences with 0
    
    Parameters:
    top_n: Number of top preferences to consider for each candidate/job
    """
    # Read the input file
    df = pd.read_csv(r'C:\Users\kritv\Downloads\BTECH PROJECT\predictions_total_match_best.csv')
    
    # Initialize lists for preferences
    job_pref_rows = []
    candidate_pref_rows = []
    
    # Create job preferences
    for job in sorted(df['JobID'].unique()):
        job_data = df[df['JobID'] == job]
        sorted_candidates = job_data.sort_values('Predicted', ascending=False)
        top_candidates = sorted_candidates['CandidateID'].head(top_n).tolist()
        
        # Fill with 0 if fewer candidates than top_n
        while len(top_candidates) < top_n:
            top_candidates.append(0)
        
        # Create row for CSV (just the preferences)
        job_pref_rows.append(top_candidates)
    
    # Create candidate preferences
    for candidate in sorted(df['CandidateID'].unique()):
        candidate_data = df[df['CandidateID'] == candidate]
        sorted_jobs = candidate_data.sort_values('Predicted', ascending=False)
        top_jobs = sorted_jobs['JobID'].head(top_n).tolist()
        
        # Fill with 0 if fewer jobs than top_n
        while len(top_jobs) < top_n:
            top_jobs.append(0)
        
        # Create row for CSV (just the preferences)
        candidate_pref_rows.append(top_jobs)
    
    # Convert to DataFrames
    job_pref_df = pd.DataFrame(job_pref_rows)
    candidate_pref_df = pd.DataFrame(candidate_pref_rows)
    
    # Save to CSV files without headers
    job_pref_df.to_csv('job_preferences.csv', index=False, header=False)
    candidate_pref_df.to_csv('candidate_preferences.csv', index=False, header=False)
    
    print("\nPreference files created:")
    print("1. job_preferences.csv")
    print("2. candidate_preferences.csv")

if __name__ == "__main__":
    create_preference_csv_files(top_n=10)
