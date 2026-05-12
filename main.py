import curses
import time
import random
from collections import deque

WIDTH, HEIGHT = 30, 15

def generate_maze():
    maze = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if i == 0 or i == HEIGHT - 1 or j == 0 or j == WIDTH - 1:
                maze[i][j] = "#"
            elif random.random() < 0.2:  # 20% peluang jadi tembok
                maze[i][j] = "#"
    return maze

def get_next_bfs(maze, start, target):
    """Mencari langkah pertama menuju target menggunakan BFS"""
    queue = deque([start])
    visited = {start}
    parent = {start: None}
    
    found = False
    while queue:
        curr = queue.popleft()
        if curr == target:
            found = True
            break
            
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            nx, ny = curr[0] + dx, curr[1] + dy
            if 0 <= nx < WIDTH and 0 <= ny < HEIGHT:
                if maze[ny][nx] != "#" and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    parent[(nx, ny)] = curr
                    queue.append((nx, ny))
    
    if not found or target == start:
        return start
        
    curr = target
    while parent[curr] != start:
        curr = parent[curr]
    return curr

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK) # Player
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)   # Enemy
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)# Exit

    maze = generate_maze()
    p_pos = [1, 1]
    e_pos = [WIDTH - 2, HEIGHT - 2]
    exit_pos = [WIDTH - 2, 1]
    
    maze[p_pos[1]][p_pos[0]] = " "
    maze[e_pos[1]][e_pos[0]] = " "
    maze[exit_pos[1]][exit_pos[0]] = "E"

    last_enemy_move = time.time()

    while True:
        stdscr.erase()
        
        for y, row in enumerate(maze):
            for x, char in enumerate(row):
                if [x, y] == p_pos:
                    stdscr.addstr(y, x, "P", curses.color_pair(1) | curses.A_BOLD)
                elif [x, y] == e_pos:
                    stdscr.addstr(y, x, "M", curses.color_pair(2) | curses.A_BOLD)
                elif char == "E":
                    stdscr.addstr(y, x, "E", curses.color_pair(3) | curses.A_BOLD)
                else:
                    stdscr.addstr(y, x, char)

        stdscr.addstr(HEIGHT + 1, 0, "Gunakan Panah (Arrow Keys) untuk kabur!")
        stdscr.refresh()

        if tuple(p_pos) == tuple(e_pos):
            stdscr.addstr(HEIGHT + 2, 0, "GAME OVER! Kamu ketangkep musuh!")
            stdscr.refresh()
            time.sleep(2)
            break
        if tuple(p_pos) == tuple(exit_pos):
            stdscr.addstr(HEIGHT + 2, 0, "MENANG! Kamu berhasil keluar!")
            stdscr.refresh()
            time.sleep(2)
            break

        # Handle Input User
        key = stdscr.getch()
        new_p = p_pos[:]
        if key == curses.KEY_UP:    new_p[1] -= 1
        elif key == curses.KEY_DOWN:  new_p[1] += 1
        elif key == curses.KEY_LEFT:  new_p[0] -= 1
        elif key == curses.KEY_RIGHT: new_p[0] += 1
        elif key == ord('q'): break
        
        if maze[new_p[1]][new_p[0]] != "#":
            p_pos = new_p

        # Pergerakan Musuh (Tiap 0.5 detik biar agak cepet)
        if time.time() - last_enemy_move > 0.5:
            next_step = get_next_bfs(maze, tuple(e_pos), tuple(p_pos))
            e_pos = list(next_step)
            last_enemy_move = time.time()

if __name__ == "__main__":
    curses.wrapper(main)