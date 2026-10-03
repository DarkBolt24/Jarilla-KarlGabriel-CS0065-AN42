class RuleBasedAgent:
    """Class representing the rule-based vacuum cleaner agent."""
    
    def __init__(self, start_location='A'):
        self.location = start_location

    def perceive_and_act(self, environment):
        """
        Perceives the environment and acts based on predefined rules.
        Rule 1: If current room is dirty, clean it.
        Rule 2: If current room is clean, move to the other room.
        """
        print(f"Agent is in room {self.location}")
        
        # Check if the room is dirty
        if environment[self.location].lower() == 'dirty':
            environment[self.location] = 'Clean'
            print(f"Room {self.location} has been cleaned.")
        else:
            self.move()

    def move(self):
        """Moves the agent to the other room."""
        next_location = 'B' if self.location == 'A' else 'A'
        print(f"Moving to room {next_location}")
        self.location = next_location


def main():
    # Task 1: Set Up the Environment
    # Initialize the two rooms using a dictionary based on user input
    environment = {
        'A': input("Is room A Dirty or Clean? ").strip().capitalize(),
        'B': input("Is room B Dirty or Clean? ").strip().capitalize()
    }
    
    # Task 3: Run the Simulation
    try:
        steps = int(input("How many steps should the agent run? "))
    except ValueError:
        print("Invalid input. Defaulting to 5 steps.")
        steps = 5

    # Initialize the agent in Room A
    agent = RuleBasedAgent(start_location='A')

    # Run the agent in a loop for the specified steps
    for step in range(1, steps + 1):
        print(f"Step {step}: ", end="")
        
        # Task 2: Implement the Rule-Based Agent
        agent.perceive_and_act(environment)
        
        # Print the current state of the environment
        print(f"Environment state: {environment}")

if __name__ == "__main__":
    main()