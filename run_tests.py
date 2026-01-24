import csv
import sys

# Add src to path just in case
sys.path.append("src")

from guard import CoherenceGuard

def run_validation():
    guard = CoherenceGuard()
    print("\n--- STARTING VALIDATION RUN (N=4) ---\n")
    
    results = []
    
    # FIX: use encoding="utf-8-sig" to handle Windows PowerShell BOM
    with open("src/validation/validation.csv", "r", encoding="utf-8-sig") as f:
        # strip() removes accidental whitespace around headers
        reader = csv.DictReader(f, skipinitialspace=True)
        
        # Debug: Print headers found if key error persists
        if 'id' not in reader.fieldnames:
            print(f"ERROR: Could not find 'id' column. Found: {reader.fieldnames}")
            return

        for row in reader:
            scan = guard.scan_abstract(row["abstract"])
            
            # Formatted Output
            print(f"ID {row['id']}: [k={scan['kappa_coherence']} t={scan['tau_temporal']} s={scan['sigma_risk']}] -> {scan['verdict']}")
            
            results.append(scan)
            
    # Calculate Average Sigma
    if results:
        avg_sigma = sum(r['sigma_risk'] for r in results) / len(results)
        print(f"\nGlobal System Stability (Avg Σ): {avg_sigma:.4f}")
    else:
        print("\nNo results found. Check CSV format.")

if __name__ == "__main__":
    run_validation()
