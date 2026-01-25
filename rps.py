import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def update_rps(grid, threshold=3):
    new_grid = grid.copy()
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]
    predators = (grid + 1) % 3
    neighbor_wins = np.zeros_like(grid)
    
    for dx, dy in directions:
        shifted_grid = np.roll(np.roll(grid, dx, axis=0), dy, axis=1)
        neighbor_wins += (shifted_grid == predators)

    mask = neighbor_wins >= threshold
    new_grid[mask] = predators[mask]
    return new_grid

# --- Simulation Setup ---
size = 200 
grid = np.random.randint(0, 3, size=(size, size))

# Data storage for analysis
history_r = []
history_p = []
history_s = []

# --- Layout Setup ---
fig = plt.figure(figsize=(15, 7))
gs = fig.add_gridspec(2, 2)

# 1. The CA Simulation
ax_sim = fig.add_subplot(gs[:, 0])
img = ax_sim.imshow(grid, cmap='viridis', interpolation='nearest')
ax_sim.set_title("Cellular Automata Grid")
ax_sim.axis('off')

# 2. Frequency Time Series
ax_freq = fig.add_subplot(gs[0, 1])
line_r, = ax_freq.plot([], [], color='purple', label='Rock')
line_p, = ax_freq.plot([], [], color='teal', label='Paper')
line_s, = ax_freq.plot([], [], color='yellow', label='Scissors')
ax_freq.set_title("Species Population (Time Series)")
ax_freq.legend(loc='upper right', fontsize='small')
ax_freq.set_ylabel("Cell Count")

# 3. Phase Space (Rock vs Paper)
ax_phase = fig.add_subplot(gs[1, 1])
phase_line, = ax_phase.plot([], [], color='black', lw=0.5, alpha=0.6)
phase_dot, = ax_phase.plot([], [], 'ro') # Current state
ax_phase.set_title("Phase Space: Rock vs Paper")
ax_phase.set_xlabel("Rock Count")
ax_phase.set_ylabel("Paper Count")
ax_phase.plot(size*size/3, size*size/3, 'bo', label="Statistical equilibrium")
ax_phase.legend(loc='upper right', frameon=True)


def animate(i):
    global grid
    grid = update_rps(grid)
    
    # Calculate counts
    counts = np.bincount(grid.ravel(), minlength=3)
    history_r.append(counts[0])
    history_p.append(counts[1])
    history_s.append(counts[2])
    
    # Update Grid
    img.set_array(grid)
    
    # Update Time Series
    t = np.arange(len(history_r))
    line_r.set_data(t, history_r)
    line_p.set_data(t, history_p)
    line_s.set_data(t, history_s)
    
    ax_freq.set_xlim(0, max(100, len(t)))
    ax_freq.set_ylim(0, size*size)
    
    # Update Phase Space
    phase_line.set_data(history_r, history_p)
    phase_dot.set_data([history_r[-1]], [history_p[-1]])
    
    ax_phase.set_xlim(min(history_r)-100, max(history_r)+100)
    ax_phase.set_ylim(min(history_p)-100, max(history_p)+100)
    
    return img, line_r, line_p, line_s, phase_line, phase_dot

# Run the animation
ani = animation.FuncAnimation(fig, animate, frames=500, interval=20, blit=False, repeat=False)
plt.tight_layout()
plt.show()