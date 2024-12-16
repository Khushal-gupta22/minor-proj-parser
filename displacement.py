import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def calculate_displacement(original_prefs, matched_pairs):
    """
    Calculate displacement for each entity based on their original preferences
    
    Parameters:
    - original_prefs: List of original preference lists
    - matched_pairs: List of matched pairs in the current round
    
    Returns:
    - List of displacements
    """
    displacements = []
    
    for entity_idx, entity_prefs in enumerate(original_prefs, 1):
        # Find the matched partner for this entity
        matched_partner = None
        for pair in matched_pairs:
            if pair[0] == entity_idx:
                matched_partner = pair[1]
                break
            elif pair[1] == entity_idx:
                matched_partner = pair[0]
                break
        
        if matched_partner is not None:
            # If partner is in preferences, calculate displacement
            try:
                displacement = entity_prefs.index(matched_partner)
                displacements.append(displacement)
            except ValueError:
                # If matched partner not in original preferences
                displacements.append(len(entity_prefs))
        else:
            # If no match found
            displacements.append(len(entity_prefs))
    
    return displacements

def analyze_displacements(candidates_file, jobs_file, original_candidate_prefs, original_job_prefs, k):
    """
    Analyze displacements across all rounds up to k
    """
    def read_flexible_csv(filename):
        matches = []
        with open(filename, 'r') as f:
            for line in f:
                # Split by comma and remove any whitespace
                row = [x.strip() for x in line.strip().split(',')]
                # Filter out empty strings
                row = [x for x in row if x]
                matches.append(row)
        return matches
    
    candidate_matches = read_flexible_csv(candidates_file)
    job_matches = read_flexible_csv(jobs_file)
    
    # Limit rounds to k
    max_rounds = min(len(candidate_matches), len(job_matches), k)
    candidate_round_displacements = []
    job_round_displacements = []
    
    # Process each round of matches up to k
    for round_idx in range(max_rounds):
        current_candidate_matches = []
        current_job_matches = []
        
        # Process candidate matches
        for candidate_idx, match in enumerate(candidate_matches[round_idx], 1):
            for job in map(int, match.split(',') if ',' in match else [match]):
                current_candidate_matches.append((candidate_idx, job))
        
        # Process job matches
        for job_idx, match in enumerate(job_matches[round_idx], 1):
            for candidate in map(int, match.split(',') if ',' in match else [match]):
                current_job_matches.append((job_idx, candidate))
        
        # Calculate displacements
        candidate_displacements = calculate_displacement(original_candidate_prefs, current_candidate_matches)
        job_displacements = calculate_displacement(original_job_prefs, current_job_matches)
        
        candidate_round_displacements.append(candidate_displacements)
        job_round_displacements.append(job_displacements)
    
    # Calculate average displacements per round
    candidate_avg_displacements = [np.mean(round_disp) for round_disp in candidate_round_displacements]
    job_avg_displacements = [np.mean(round_disp) for round_disp in job_round_displacements]
    
    return candidate_avg_displacements, job_avg_displacements, max_rounds

def plot_displacement_graph(candidate_displacements, job_displacements, num_rounds):
    """
    Plot displacement graph
    """
    plt.figure(figsize=(10, 6))
    rounds = range(1, num_rounds + 1)
    
    plt.plot(rounds, candidate_displacements[:num_rounds], marker='o', label='Candidates')
    plt.plot(rounds, job_displacements[:num_rounds], marker='s', label='Employers')
    
    plt.title('Average Displacement per Round')
    plt.xlabel('Round')
    plt.ylabel('Average Displacement')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('displacement_graph.png')
    plt.close()

# Load original preferences
def load_original_preferences(filename):
    prefs = []
    with open(filename, 'r') as f:
        for line in f:
            # Convert to list of integers, filtering out empty strings
            pref_list = [int(x) for x in line.strip().split(',') if x]
            prefs.append(pref_list)
    return prefs

# Main analysis
original_candidate_prefs = load_original_preferences('candidate_preferences.csv')
original_job_prefs = load_original_preferences('job_preferences.csv')
k = 10  # Set the desired number of rounds

candidate_displacements, job_displacements, num_rounds = analyze_displacements(
    'candidate_pairs.csv', 
    'job_pairs.csv', 
    original_candidate_prefs, 
    original_job_prefs,
    k
)

# Print average displacements
print("Candidate Average Displacements per Round:", candidate_displacements[:num_rounds])
print("Job Average Displacements per Round:", job_displacements[:num_rounds])

# Plot the graph
plot_displacement_graph(candidate_displacements, job_displacements, num_rounds)

print(f"Graph saved as displacement_graph.png (showing {num_rounds} rounds)")
