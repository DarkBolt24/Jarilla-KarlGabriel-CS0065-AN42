# Task 1A: Create a Knowledge Base
# Use Case: PC Gaming & Network Performance
knowledge_base = {
    "categories": ["network_status", "hardware_status", "game_performance"],
    "facts": {
        "ping_ms": 135,
        "fps": 45,
        "packet_loss": True,
        "cpu_temp_c": 86,
        "gpu_temp_c": 75
    }
}

# Task 2A: Create at least 3 IF THEN rules
def rule_high_ping(facts):
    # Rule 1: Triggers if network latency is high or unstable
    if facts["ping_ms"] > 100 or facts["packet_loss"]:
        return "Restart your router and check the ethernet cable."
    return None

def rule_low_fps(facts):
    # Rule 2: Triggers if frame rate is below competitive standards
    if facts["fps"] < 60:
        return "Lower Valorant graphics settings and disable background apps."
    return None

def rule_overheating(facts):
    # Rule 3: Triggers if hardware temperatures are dangerous
    if facts["cpu_temp_c"] > 80 or facts["gpu_temp_c"] > 80:
        return "Check PC cooling and clean dust from fans."
    return None

rules = [rule_high_ping, rule_low_fps, rule_overheating]

# Task 2B: Implement an Inference Engine
def inference_engine(kb, rule_list):
    actions = []
    facts = kb["facts"]
    # Reads the knowledge base and checks each rule
    for rule in rule_list:
        action = rule(facts)
        if action:
            actions.append(action) # Returns all actions inferred
    return actions

# Task 2C: Display Output
print("--- RBR System Output ---")
print("Rule-Based Reasoning Actions:")
rbr_actions = inference_engine(knowledge_base, rules)
for action in rbr_actions:
    print(f"- {action}")
print("\n")

# Task 3A: Build a Case Base
# Use Case: Vehicle Maintenance 
case_base = [
    {
        "problem": {"engine_wont_start": True, "headlights_dim": True, "clicking_noise": True},
        "solution": "Replace or jump-start the vehicle battery."
    },
    {
        "problem": {"engine_wont_start": True, "headlights_dim": False, "clicking_noise": False},
        "solution": "Check the starter motor or fuel pump."
    },
    {
        "problem": {"engine_wont_start": False, "steering_vibrates": True, "check_engine": False},
        "solution": "Check tire alignment and wheel balance."
    }
]

# Similarity function to support the Retrieve step
def calculate_similarity(new_case, past_case):
    matches = 0
    total = len(new_case)
    for key in new_case:
        if key in past_case and new_case[key] == past_case[key]:
            matches += 1
    return matches / total if total > 0 else 0

# Task 3C: Reuse Step (Includes Retrieve logic)
def retrieve_and_reuse(new_problem, cb):
    best_match = None
    highest_score = -1

    for case in cb:
        score = calculate_similarity(new_problem, case["problem"])
        if score > highest_score:
            highest_score = score
            best_match = case

    print(f"[Retrieve] Highest similarity score: {highest_score * 100:.2f}%")
    print(f"[Reuse] Suggested Solution: {best_match['solution']}")
    return best_match['solution'] # Returns the solution of the most similar case

# Task 3D: Revise Step
def revise(suggested_solution):
    # Simulating a user prompt adjusting the solution manually
    print("[Revise] Evaluating solution...")
    user_override = "" # If a user typed a string here, it would override the solution
    if user_override:
        print(f"Solution revised to: {user_override}")
        return user_override
    print("Solution accepted unchanged.")
    return suggested_solution

# Task 3E: Retain Step
def retain(new_problem, final_solution, cb):
    new_case = {"problem": new_problem, "solution": final_solution}
    cb.append(new_case) # Adds the new case to the case base
    print("[Retain] New case successfully added to the Case Base.")

# CBR Execution
print("--- CBR System Output ---")
# Simulating a new unstructured problem (e.g., Honda BR-V battery issue)
new_vehicle_problem = {"engine_wont_start": True, "headlights_dim": True, "clicking_noise": False}
suggested = retrieve_and_reuse(new_vehicle_problem, case_base)
final = revise(suggested)
retain(new_vehicle_problem, final, case_base)