# Rock-Paper-Scissors-Dynamics-in-a-2-Dimensional-Cellular-Automata
This repository contains a collection of Python-based simulations investigating the dynamics of biodiversity and pattern formation in cyclic competition games. By utilizing Two-Dimensional Cellular Automata (CA) and stochastic models, the repository explores how local microscopic rules lead to macroscopic self-organization.
# Overview
These scripts simulate non-hierarchical evolutionary game dynamics where species compete in a "predator-prey" cycle. In a spatial grid, these interactions prevent a single species from dominating, often resulting in the formation of entangled spiral waves that maintain biodiversity.
# Core Functionality
Each script implements a $200 \times 200$ grid with periodic (toroidal) boundary conditions and follows these general mechanics: 

-Neighbor Detection: Uses a Moore Neighborhood (8 immediate neighbors) to count the number of predators surrounding a cell.\\
-Threshold Rule: A cell transitions to its predator state only if the number of surrounding predators meets or exceeds a fixed threshold (default is 3).\\
-Simultaneous Updates: The entire grid is updated at each generation to observe self-organizing spatial patterns.\\
# Script Details
-1. rps.py (3-Species Classic)Logic: Rock (0) $\rightarrow$ Paper (1) $\rightarrow$ Scissors (2) $\rightarrow$ Rock (0). Visuals: Includes a Phase Space plot (Rock vs. Paper population) to visualize how the system oscillates around a statistical equilibrium.\\
-2. rps4.py (4-Species Cyclic)Logic: $0 \rightarrow 1 \rightarrow 2 \rightarrow 3 \rightarrow 0$.Dynamics: Demonstrates the effect of "non-interactions." Because each species has only one specific predator in a four-state cycle, "draws" occur between non-neighboring states, often leading to slower propagation or "oasis" formations.\\
-3. rpsls.py (5-Species RPSLS)Logic: Based on the game popularized by Sam Kass and The Big Bang Theory. Conflict Resolution: Unlike the other models, each species has two predators. If both predators meet the threshold in a cell's neighborhood, the code implements a random choice to decide which species takes over the cell.\\
# Requirements
numpy and matplotlibKey 

