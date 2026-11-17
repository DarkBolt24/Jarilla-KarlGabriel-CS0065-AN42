import random

class BonusRuleBasedAgent:
    """Agent that handles three rooms and visualizes movement."""
    
    def __init__(self, start_location='A'):
        self.location = start_location

    def display_grid(self, environment):
        """Visualizes the agent and room states using a text-based grid."""
        grid_elements = []
        for room in ['A', 'B', 'C']:
            if self.location == room:
                grid_elements.append(f"[{room}-Agent]")
            else:
                grid_elements.append(f"[{room}-{environment[room]}]")
        print(" ".join(grid_elements))

    def perceive_and_act(self, environment):
        """
        Perceives the environment and acts.
        Randomly chooses which dirty room to clean next if current is clean.
        """
        # Print initial state for this step
        self.display_grid(environment)
        
        # Check if all rooms are clean
        if all(state.lower() == 'clean' for state in environment.values()):
            print("All rooms are clean.\nAgent is idle.")
            self.display_grid(environment)
            return

        # Action: Clean or Move
        if environment[self.location].lower() == 'dirty':
            environment[self.location] = 'Clean'
            print(f"Room {self.location} has been cleaned.")
            self.display_grid(environment)
        else:
            # Find all dirty rooms
            dirty_rooms = [room for room, state in environment.items() if state.lower() == 'dirty']
            
            # Randomly select a dirty room and move
            if dirty_rooms:
                next_room = random.choice(dirty_rooms)
                print(f"Moving to room {next_room}")
                self.location = next_room
            self.display_grid(environment)

def main():
    # Initialize the three rooms
    # Room A is defaulted to 'Clean' based on the TA2 bonus sample output structure
    environment = {
        'A': 'Clean',
        'B': input("Is room B Dirty or Clean? ").strip().capitalize(),
        'C': input("Is room C Dirty or Clean? ").strip().capitalize()
    }
    
    try:
        steps = int(input("How many steps should the agent run? "))
    except ValueError:
        print("Invalid input. Defaulting to 5 steps.")
        steps = 5

    # Initialize the agent in Room A
    agent = BonusRuleBasedAgent(start_location='A')

    # Run the simulation
    for step in range(1, steps + 1):
        print(f"\nStep {step}:")
        agent.perceive_and_act(environment)

if __name__ == "__main__":
    main()