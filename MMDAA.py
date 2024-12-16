import pandas as pd

def read_csv_file(filename):
    """Read CSV file and return its content as a string"""
    try:
        df = pd.read_csv(filename, header=None)
        return df.values.tolist()
    except Exception as e:
        print(f"Error reading {filename}: {str(e)}")
        return []

def load_preferences(candidates_file, employers_file):
    """Load and format preference data from CSV files"""
    candidates_data = read_csv_file(candidates_file)
    employers_data = read_csv_file(employers_file)
    
    # Process preferences - remove zeros and -1s
    def process_preferences(data):
        prefs = []
        for row in data:
            # Filter out zeros, -1s, and empty strings, keep 1-based indexing
            pref_list = [int(x) for x in row if str(x).strip() and int(x) > 0]
            prefs.append(pref_list)
        return prefs
    
    candidates_prefs = process_preferences(candidates_data)
    employers_prefs = process_preferences(employers_data)
    
    return candidates_prefs, employers_prefs

def run_daa(candidates_prefs, employers_prefs):
    """Single round of Deferred Acceptance Algorithm"""
    n_candidates = len(candidates_prefs)
    matches = {}  # employer -> candidate
    candidate_matches = {}  # candidate -> employer
    
    # Keep track of proposals
    proposals = {i: set() for i in range(n_candidates)}
    
    while True:
        # Find an unmatched candidate who hasn't proposed to everyone
        proposing_candidate = None
        for c in range(n_candidates):
            if (c not in candidate_matches and 
                len(proposals[c]) < len(candidates_prefs[c])):
                proposing_candidate = c
                break
        
        if proposing_candidate is None:
            break
            
        # Get next employer to propose to
        remaining_prefs = [e for e in candidates_prefs[proposing_candidate] 
                         if e not in proposals[proposing_candidate]]
        
        if not remaining_prefs:
            continue
            
        employer = remaining_prefs[0] - 1  # Convert to 0-based indexing
        proposals[proposing_candidate].add(employer + 1)
        
        # If employer has no preferences, reject the proposal
        if employer >= len(employers_prefs) or not employers_prefs[employer]:
            continue
            
        # Get employer's preferences (convert to 0-based indexing)
        employer_prefs = [c - 1 for c in employers_prefs[employer]]
        
        # If employer is unmatched
        if employer not in matches:
            if proposing_candidate in employer_prefs:
                matches[employer] = proposing_candidate
                candidate_matches[proposing_candidate] = employer
        else:
            current_match = matches[employer]
            # If employer prefers new candidate
            if (proposing_candidate in employer_prefs and 
                (current_match not in employer_prefs or 
                 employer_prefs.index(proposing_candidate) < employer_prefs.index(current_match))):
                # Remove old match
                del candidate_matches[current_match]
                # Add new match
                matches[employer] = proposing_candidate
                candidate_matches[proposing_candidate] = employer
    
    # Convert back to 1-based indexing
    return [(c + 1, e + 1) for e, c in matches.items()]

def multi_match_daa(candidates_prefs, employers_prefs, k):
    """Multi-Match Deferred Acceptance Algorithm"""
    all_matches = []
    match_number = 0
    
    # Make copies of original preferences
    current_candidates_prefs = [prefs.copy() for prefs in candidates_prefs]
    current_employers_prefs = [prefs.copy() for prefs in employers_prefs]
    
    while match_number < k:
        # Run DAA with current preferences
        matches = run_daa(current_candidates_prefs, current_employers_prefs)
        
        if not matches:
            break
            
        # Add matches to results
        all_matches.append(matches)
        match_number += 1
        
        # Remove matched pairs from preference lists
        for candidate, employer in matches:
            # Remove employer from candidate's preferences (1-based indexing)
            if candidate <= len(current_candidates_prefs):
                if employer in current_candidates_prefs[candidate-1]:
                    current_candidates_prefs[candidate-1].remove(employer)
            
            # Remove candidate from employer's preferences (1-based indexing)
            if employer <= len(current_employers_prefs):
                if candidate in current_employers_prefs[employer-1]:
                    current_employers_prefs[employer-1].remove(candidate)
    
    return all_matches

def write_results(all_matches, n_candidates, n_employers, candidate_file, job_file):
    """Write matching results to CSV files"""
    # Initialize empty dictionaries for both perspectives
    candidate_matches = {i: [] for i in range(1, n_candidates + 1)}
    employer_matches = {i: [] for i in range(1, n_employers + 1)}
    
    # Process all matches
    for round_matches in all_matches:
        for candidate, employer in round_matches:
            candidate_matches[candidate].append(employer)
            employer_matches[employer].append(candidate)
    
    # Write candidate matches
    with open(candidate_file, 'w') as f:
        for candidate in range(1, n_candidates + 1):
            matches = candidate_matches.get(candidate, [])
            f.write(','.join(map(str, matches)) + '\n')
    
    # Write employer matches
    with open(job_file, 'w') as f:
        for employer in range(1, n_employers + 1):
            matches = employer_matches.get(employer, [])
            f.write(','.join(map(str, matches)) + '\n')

def main():
    try:
        # File paths
        candidates_file = "candidate_preferences.csv"
        employers_file = "job_preferences.csv"
        candidate_output_file = "candidate_pairs.csv"
        job_output_file = "job_pairs.csv"
        
        # Load preferences
        candidates_prefs, employers_prefs = load_preferences(candidates_file, employers_file)
        
        print(f"Loaded {len(candidates_prefs)} candidates and {len(employers_prefs)} employers")
        
        # Set maximum number of matches to find
        k = 10
        
        # Run MMDAA
        all_matches = multi_match_daa(candidates_prefs, employers_prefs, k)
        
        # Write results
        write_results(all_matches, 
                     len(candidates_prefs), 
                     len(employers_prefs),
                     candidate_output_file, 
                     job_output_file)
        
        print(f"Matching completed successfully.")
        print(f"Found {len(all_matches)} stable matchings.")
        print(f"Results written to {candidate_output_file} and {job_output_file}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()