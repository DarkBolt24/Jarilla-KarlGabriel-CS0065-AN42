import agentpy as ap
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import collections

# -------- Get user input from console --------
print("--- Random Walk Simulation (Laboratory Tasks) ---")
num_agents = int(input("Enter number of agents: "))
grid_size = int(input("Enter grid size (e.g., 10 for 10x10): "))
num_steps = int(input("Enter number of steps: "))

print("\n--- Select Movement Rule (Laboratory Task 2 & 4) ---")
print("1. Standard Random Walk")
print("2. Biased Walk (Prefers moving Right)")
print("3. Avoidance (Agents avoid stepping on occupied cells)")
rule_choice = input("Enter rule number (1-3): ")

movement_rule = 'random'
if rule_choice == '2':
    movement_rule = 'biased'
elif rule_choice == '3':
    movement_rule = 'avoid'

# -------- Agent Definition -----------
class RandomWalker(ap.Agent):
    def setup(self):
        # Laboratory Task 1: Initialize path tracking
        self.history_x = []
        self.history_y = []

    def record_position(self):
        # Laboratory Task 1: Save current position to path
        self.history_x.append(self.position[0])
        self.history_y.append(self.position[1])

    def step(self):
        x, y = self.position

        # Laboratory Task 2: Change movement rules
        if self.model.p.movement_rule == 'biased':
            # Bias direction: 40% right, 20% left, 20% up, 20% down
            direction = random.choices(
                [(1,0), (-1,0), (0,1), (0,-1)], 
                weights=[0.4, 0.2, 0.2, 0.2], 
                k=1
            )[0]
        else:
            # Standard random choice
            direction = random.choice([(1,0), (-1,0), (0,1), (0,-1)])

        # Keep agents inside grid
        new_x = max(0, min(self.model.p.grid_size[0]-1, x + direction[0]))
        new_y = max(0, min(self.model.p.grid_size[1]-1, y + direction[1]))

        # Laboratory Task 2: Avoidance Rule
        if self.model.p.movement_rule == 'avoid':
            # Check if the target cell is already occupied by another agent
            occupied = any(a.position == (new_x, new_y) for a in self.model.agents if a != self)
            if not occupied:
                self.position = (new_x, new_y)
            # If occupied, the agent simply waits in place for this step
        else:
            self.position = (new_x, new_y)

        self.record_position()

# -------- Model Definition -----------
class RandomWalkModel(ap.Model):
    def setup(self):
        self.agents = ap.AgentList(self, self.p.agents, RandomWalker)

        # Initialize random positions
        # For avoidance rule, ensure they don't spawn on the same cell if possible
        if self.p.movement_rule == 'avoid' and self.p.agents <= (self.p.grid_size[0] * self.p.grid_size[1]):
            all_cells = [(i, j) for i in range(self.p.grid_size[0]) for j in range(self.p.grid_size[1])]
            start_positions = random.sample(all_cells, self.p.agents)
            for agent, pos in zip(self.agents, start_positions):
                agent.position = pos
        else:
            for agent in self.agents:
                agent.position = (random.randint(0, self.p.grid_size[0]-1),
                                  random.randint(0, self.p.grid_size[1]-1))
        
        # Record the starting position for the path
        for agent in self.agents:
            agent.record_position()

    def step(self):
        # Shuffle agents to prevent turn-order bias when avoiding each other
        agents_shuffled = list(self.agents)
        random.shuffle(agents_shuffled)
        for agent in agents_shuffled:
            agent.step()

# -------- Parameters -----------
parameters = {
    'agents': num_agents,
    'grid_size': (grid_size, grid_size),
    'steps': num_steps,
    'movement_rule': movement_rule
}

# -------- Run Model -----------
model = RandomWalkModel(parameters)
model.setup()

# -------- Interactive Animation -----------
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-0.5, model.p.grid_size[0] - 0.5)
ax.set_ylim(-0.5, model.p.grid_size[1] - 0.5)
ax.set_xticks(range(model.p.grid_size[0]))
ax.set_yticks(range(model.p.grid_size[1]))
ax.grid(True, linestyle='--', alpha=0.5)
ax.set_title(f"Random Walk Simulation\nRule: {movement_rule.capitalize()}")

# Scatter plot for current positions
scat = ax.scatter([], [], s=150, zorder=5, color='red')

# Laboratory Task 1: Line objects for tracking paths
lines = [ax.plot([], [], '-', alpha=0.4, linewidth=2)[0] for _ in range(num_agents)]

def update(frame):
    model.step()
    
    # Update current positions
    x = [agent.position[0] for agent in model.agents]
    y = [agent.position[1] for agent in model.agents]
    scat.set_offsets(list(zip(x, y)))

    # Update path trails
    for i, agent in enumerate(model.agents):
        lines[i].set_data(agent.history_x, agent.history_y)

    return [scat] + lines

# Run animation
ani = animation.FuncAnimation(fig, update, frames=model.p.steps, blit=True, repeat=False)
plt.show()

# -------- Laboratory Task 3: Analyze Final Positions -----------
# Note: This executes in the console after the animation window is closed.
print("\n--- Final Analysis ---")
final_positions = [agent.position for agent in model.agents]
print("Final Agent Positions:", final_positions)

# Group and count distributions
distribution = collections.Counter(final_positions)
print("\nPosition Distribution (Cells with agents):")
for pos, count in distribution.items():
    print(f"Cell {pos}: {count} agent(s)")

# Analyze by Quadrant to observe clustering
mid_x, mid_y = grid_size / 2, grid_size / 2
quadrants = {'Top-Right': 0, 'Top-Left': 0, 'Bottom-Left': 0, 'Bottom-Right': 0}

for (x, y) in final_positions:
    if x >= mid_x and y >= mid_y: quadrants['Top-Right'] += 1
    elif x < mid_x and y >= mid_y: quadrants['Top-Left'] += 1
    elif x < mid_x and y < mid_y: quadrants['Bottom-Left'] += 1
    else: quadrants['Bottom-Right'] += 1

print("\nAgent Distribution by Quadrant:")
for quad, count in quadrants.items():
    print(f"{quad}: {count} agent(s)")