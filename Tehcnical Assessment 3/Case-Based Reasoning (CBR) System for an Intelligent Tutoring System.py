# Case-Based Reasoning (CBR) System for an Intelligent Tutoring System
import json

# 1. Define the Case Base
# Storing past cases including student profiles, problems with repeated errors, successful solutions, and outcomes.
case_base = [
    {
        "id": 1,
        "student_profile": {"student_id": "S101", "grade_level": 9},
        "problem": {"error_type": "sign_error", "topic": "algebra", "difficulty": "medium", "repeated_errors": True},
        "solution": {"feedback": "Review the rules for multiplying negative numbers.", "module": "Basic Algebra Signs"},
        "outcome": "Success"
    },
    {
        "id": 2,
        "student_profile": {"student_id": "S102", "grade_level": 10},
        "problem": {"error_type": "formula_misuse", "topic": "geometry", "difficulty": "hard", "repeated_errors": True},
        "solution": {"feedback": "Double-check the specific formula for the shape's area before calculating.", "module": "Geometry Formulas"},
        "outcome": "Success"
    },
    {
        "id": 3,
        "student_profile": {"student_id": "S103", "grade_level": 8},
        "problem": {"error_type": "fraction_addition", "topic": "arithmetic", "difficulty": "easy", "repeated_errors": True},
        "solution": {"feedback": "Remember to find a common denominator first.", "module": "Fraction Fundamentals"},
        "outcome": "Success"
    }
]

# The new student profile and problem scenario
new_student_profile = {"student_id": "S104", "grade_level": 10}
new_problem = {"error_type": "formula_misuse", "topic": "trigonometry", "difficulty": "hard", "repeated_errors": True}

print("--- NEW PROBLEM SCENARIO ---")
print(json.dumps({"student_profile": new_student_profile, "problem": new_problem}, indent=2))

# 2. Similarity Assessment
def calculate_similarity(new_prob, past_prob):
    score = 0
    if new_prob["error_type"] == past_prob["error_type"]: score += 3 # High weight for error type
    if new_prob["topic"] == past_prob["topic"]: score += 1
    if new_prob["difficulty"] == past_prob["difficulty"]: score += 1
    return score

best_match = None
highest_score = -1

for case in case_base:
    score = calculate_similarity(new_problem, case["problem"])
    if score > highest_score:
        highest_score = score
        best_match = case

print(f"\n--- RETRIEVED SIMILAR CASE (Similarity Score: {highest_score}) ---")
print(json.dumps(best_match, indent=2))

# 3. Adapt the Solution
# Modifying the retrieved solution to fit the new problem's specific topic context.
adapted_solution = best_match["solution"].copy()
adapted_solution["feedback"] = f"Warning: Repeated {new_problem['error_type']} detected. Before solving for {new_problem['topic']}, ensure you are applying the correct theorems."
adapted_solution["module"] = f"Review: {new_problem['topic'].capitalize()} Fundamentals"

print("\n--- ADAPTED FINAL SOLUTION ---")
print(json.dumps(adapted_solution, indent=2))

# 4. Demonstrate Learning (Retention)
# Saving the newly solved case into the system's case base, retaining the new student profile and pending outcome.
new_case = {
    "id": len(case_base) + 1,
    "student_profile": new_student_profile,
    "problem": new_problem,
    "solution": adapted_solution,
    "outcome": "Pending Assessment"
}
case_base.append(new_case)

print("\n--- NEW CASE SAVED. UPDATED CASE BASE ---")
print(json.dumps(case_base, indent=2))