import numpy as np
import pandas as pd
import traceback

def read_csv_file(filename):
    """Read CSV file and return its content as a string"""
    with open(filename, 'r') as f:
        return f.read()

def load_preferences(candidates_file, employers_file):
    """Load and format preference data from CSV files"""
    # Read the CSV files
    candidates_data = read_csv_file(candidates_file)
    employers_data = read_csv_file(employers_file)
    
    # Convert to preference lists, handling variable lengths
    candidates_prefs = []
    for row in candidates_data.strip().split('\n'):
        # Convert to integers, remove zeros, and adjust to 0-based indexing
        pref_list = [int(x) - 1 for x in row.split(',') if int(x) != 0]
        candidates_prefs.append(pref_list)
    
    employers_prefs = []
    for row in employers_data.strip().split('\n'):
        # Convert to integers, remove zeros, and adjust to 0-based indexing
        pref_list = [int(x) - 1 for x in row.split(',') if int(x) != 0]
        employers_prefs.append(pref_list)
    
    return candidates_prefs, employers_prefs

def create_preference_rankings(prefs):
    """Create ranking dictionaries for quick lookup"""
    rankings = []
    for pref_list in prefs:
        ranking = {employer: rank for rank, employer in enumerate(pref_list)}
        rankings.append(ranking)
    return rankings

def deferred_acceptance(candidates_prefs, employers_prefs):
    """
    Implement the deferred acceptance algorithm
    Returns: matches, history of proposals
    """
    n_candidates = len(candidates_prefs)
    n_employers = len(employers_prefs)
    
    # Create preference rankings for quick lookup
    employer_rankings = create_preference_rankings(employers_prefs)
    
    # Initialize variables
    matches = [-1] * n_employers  # employer -> candidate
    candidate_matches = [-1] * n_candidates  # candidate -> employer
    next_proposal = [0] * n_candidates  # next employer to propose to for each candidate
    unmatched_candidates = list(range(n_candidates))
    proposal_history = []  # track all proposals for analysis
    
    # Main loop
    while unmatched_candidates:
        candidate = unmatched_candidates[0]
        
        # If candidate has no more employers to propose to
        if next_proposal[candidate] >= len(candidates_prefs[candidate]):
            unmatched_candidates.pop(0)
            continue
            
        # Get next employer for this candidate to propose to
        employer = candidates_prefs[candidate][next_proposal[candidate]]
        next_proposal[candidate] += 1
        
        # Record the proposal
        proposal_history.append((candidate, employer))
        
        # If employer is unmatched
        if matches[employer] == -1:
            matches[employer] = candidate
            candidate_matches[candidate] = employer
            unmatched_candidates.pop(0)
        else:
            current_match = matches[employer]
            # If employer prefers this candidate to current match
            if employer_rankings[employer].get(candidate, float('inf')) < employer_rankings[employer].get(current_match, float('inf')):
                matches[employer] = candidate
                candidate_matches[candidate] = employer
                candidate_matches[current_match] = -1
                unmatched_candidates.pop(0)
                unmatched_candidates.append(current_match)
    
    return candidate_matches, proposal_history

def write_results(matches, proposal_history, output_file="matching_results.csv"):
    """Write matching results to CSV and print metrics to terminal"""
    # Convert to 1-based indexing for output
    matches_df = pd.DataFrame({
        'candidate': range(1, len(matches) + 1),
        'matched_employer': [m + 1 if m != -1 else 0 for m in matches]
    })
    
    # Calculate some basic metrics
    total_proposals = len(proposal_history)
    avg_proposals_per_candidate = total_proposals / len(matches)
    unmatched_count = sum(1 for m in matches if m == -1)
    
    # Print metrics to terminal
    print("\n# Matching Metrics:")
    print(f"Total Proposals: {total_proposals}")
    print(f"Average Proposals per Candidate: {avg_proposals_per_candidate:.2f}")
    print(f"Unmatched Candidates: {unmatched_count}")
    
    # Write matching results to CSV (without metrics)
    with open(output_file, 'w') as f:
        f.write("# Matching Results\n")
        matches_df.to_csv(f, index=False)
        
    print(f"\nMatching results written to {output_file}")


def main():
    # File paths
    candidates_file = "candidate_preferences.csv"
    employers_file = "job_preferences.csv"
    output_file = "matching_results.csv"
    
    try:
        # Load and process preferences
        candidates_prefs, employers_prefs = load_preferences(candidates_file, employers_file)
        
        # Validate input data
        print(f"Number of candidates: {len(candidates_prefs)}")
        print(f"Number of employers: {len(employers_prefs)}")
        
        # Check for potential issues
        max_employer_id = max(max(pref) for pref in candidates_prefs)
        print(f"Maximum employer ID in candidates preferences: {max_employer_id}")
        
        # Run the algorithm
        matches, history = deferred_acceptance(candidates_prefs, employers_prefs)
        
        # Write results
        write_results(matches, history, output_file)
        
        print(f"Matching completed successfully. Results written to {output_file}")
        
        return matches, history
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Traceback:")
        traceback.print_exc()

if __name__ == "__main__":
    main()