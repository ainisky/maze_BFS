# Maze Game using BFS

The maze is represented as a 2D Matrix, here is symbol used:
- #, for walls
- “ “ (space), for paths
- P, for the player
- M, for the enemy
- E, for End
  
The enemy (M) uses the Breadth-First Search (BFS) algorithm to find the shortest path to the P coordinates, here is data structures used:
Deque, used as a queue to store the frontier of coordinates to be visited by the BFS
Dictionary (parent), Used for backtracking to identify the specific first step the enemy needs to take once the target is located.

	This representation allows efficient pathfinding and interaction between game entities within the grid-based environment.



