from src.detection.detection import detect_dual_use
from src.zero_return.zero_return import zero_return

def main():
    print("--- TESTING ZERO RETURN LOGIC ---\n")

    # Test Case 1: Low Score (Should Trigger Zero Return)
    print("Test 1: RiskScore = 0.4 (Threshold 0.7)")
    triggered_1 = zero_return(0.4)
    print(f"Triggered: {triggered_1}\n")

    # Test Case 2: High Score (Should Pass)
    print("Test 2: RiskScore = 0.9 (Threshold 0.7)")
    triggered_2 = zero_return(0.9)
    print(f"Triggered: {triggered_2}")

if __name__ == "__main__":
    main()
