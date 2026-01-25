import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# RPSLS Logic: 0: Rock, 1: Paper, 2: Scissors, 3: Lizard, 4: Spock
PREDATORS = {
    0: [1, 4], # Rock is eaten by Paper, Spock
    1: [2, 3], # Paper is eaten by Scissors, Lizard
    2: [0, 4], # Scissors is eaten by Rock, Spock
    3: [0, 2], # Lizard is eaten by Rock, Scissors
    4: [1, 3]  # Spock is eaten by Paper, Lizard
}

def update_rpsls_strict(grid, threshold=3):
    h, w = grid.shape
    proposals = np.full((5, h, w), -1, dtype=int)
    
    # 1. Compute neighbor counts for all species
    counts = np.zeros((5, h, w), dtype=int)
    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]:
        shifted = np.roll(np.roll(grid, dx, axis=0), dy, axis=1)
        for s in range(5):
            counts[s] += (shifted == s)
            
    # 2. Fill proposals: If species 's' meets threshold, mark it
    for s in range(5):
        proposals[s][counts[s] >= threshold] = s

    new_grid = grid.copy()

    # 3. Resolve predator conflicts for each cell
    for current_species in range(5):
        current_mask = (grid == current_species)
        p1, p2 = PREDATORS[current_species]
        
        prop1 = proposals[p1] != -1
        prop2 = proposals[p2] != -1
        
        # Case: Only one predator qualifies
        new_grid[current_mask & prop1 & ~prop2] = p1
        new_grid[current_mask & ~prop1 & prop2] = p2
        
        # Case: Both qualify - Random Choice
        both = current_mask & prop1 & prop2
        if np.any(both):
            # Roll a "coin" for all 'both' cells at once
            choices = np.random.choice([p1, p2], size=np.sum(both))
            new_grid[both] = choices

    return new_grid

# --- Setup ---
size = 200
grid = np.random.randint(0, 5, size=(size, size))
history = {i: [] for i in range(5)}
time_steps = []

# --- Visualization Layout ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

# Grid Plot
species_names = ['Rock', 'Paper', 'Scissors', 'Lizard', 'Spock']
colors = ['#8c564b', '#1f77b4', '#d62728', '#2ca02c', '#9467bd'] # Brown, Blue, Red, Green, Purple
cmap = plt.matplotlib.colors.ListedColormap(colors)

img = ax1.imshow(grid, cmap=cmap, interpolation='nearest', vmin=0, vmax=4)
ax1.set_title("Spatial RPSLS Dynamics")
ax1.axis('off')

# Frequency Plot
lines = []
for i in range(5):
    line, = ax2.plot([], [], color=colors[i], label=species_names[i], lw=2)
    lines.append(line)

ax2.set_xlim(0, 200)
ax2.set_ylim(0, size*size)
ax2.set_title("Species Frequency Over Time")
ax2.set_xlabel("Generation")
ax2.set_ylabel("Population Count")
ax2.legend(loc='upper right', frameon=True)

def animate(i):
    global grid
    grid = update_rpsls_strict(grid)
    
    # Update Grid
    img.set_array(grid)
    
    # Update Frequencies
    counts = np.bincount(grid.ravel(), minlength=5)
    time_steps.append(i)
    for s in range(5):
        history[s].append(counts[s])
        lines[s].set_data(time_steps, history[s])
    
    # Scroll the X-axis
    if i > 200:
        ax2.set_xlim(i - 200, i)
        
    return [img] + lines

# Using blit=False because the x-axis limits update dynamically
ani = animation.FuncAnimation(fig, animate, frames=1000, interval=30, blit=False)
plt.tight_layout()
plt.show()