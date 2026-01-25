import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def update_rps_4(grid, threshold=3):
    new_grid = grid.copy()
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]
    
    # 4-Species Logic: 0->1->2->3->0
    # The predator of species 'n' is (n + 1) % 4
    predators = (grid + 1) % 4
    
    neighbor_wins = np.zeros_like(grid)
    for dx, dy in directions:
        shifted_grid = np.roll(np.roll(grid, dx, axis=0), dy, axis=1)
        neighbor_wins += (shifted_grid == predators)

    mask = neighbor_wins >= threshold
    new_grid[mask] = predators[mask]
    return new_grid

# --- Simulation Setup ---
size = 200
grid = np.random.randint(0, 4, size=(size, size)) 

# Data storage for 4 species
history = {0: [], 1: [], 2: [], 3: []}

# --- Visualization Setup ---
fig = plt.figure(figsize=(15, 7))
gs = fig.add_gridspec(2, 2)

ax_sim = fig.add_subplot(gs[:, 0])
img = ax_sim.imshow(grid, cmap='jet', interpolation='nearest')
ax_sim.set_title("4-Species Cyclic CA")

ax_freq = fig.add_subplot(gs[:, 1])
colors = ['red', 'blue', 'green', 'orange']
lines = [ax_freq.plot([], [], color=colors[i], label=f'Species {i}')[0] for i in range(4)]
ax_freq.set_title("Population Dynamics")
ax_freq.legend()

def animate(i):
    global grid
    grid = update_rps_4(grid)
    
    img.set_array(grid)
    
    counts = np.bincount(grid.ravel(), minlength=4)
    t = np.arange(len(history[0]) + 1)
    
    for s in range(4):
        history[s].append(counts[s])
        lines[s].set_data(t, history[s])
    
    ax_freq.set_xlim(0, max(100, len(t)))
    ax_freq.set_ylim(0, size*size)
    
    return [img] + lines

ani = animation.FuncAnimation(fig, animate, frames=500, interval=20, blit=False)
plt.tight_layout()
plt.show()