import pygame
import sys
import time
import random
from collections import deque

# Game configs
WIDTH, HEIGHT = 800, 600
MAZE_W, MAZE_H = 21, 17

PLAYER_COLOR = (0, 255, 0)
ENEMY_COLOR = (255, 0, 0)
EXIT_COLOR = (255, 255, 0)
WALL_COLOR = (0, 0, 255)

MOVE_DELAY = 0.3


#Generate Maze

def generate_maze(w, h):
    maze = [[" " for _ in range(w)] for _ in range(h)]

    for y in range(h):
        for x in range(w):
            if x == 0 or y == 0 or x == w-1 or y == h-1:
                maze[y][x] = "#"
            elif random.random() < 0.2:
                maze[y][x] = "#"

    return maze

# Enemy AI (BFS Implementation)

def get_next_bfs(maze, start, target):
    queue = deque([start])
    visited = {start}
    parent = {start: None}

    found = False

    while queue:
        x, y = queue.popleft()

        if (x, y) == target:
            found = True
            break

        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            nx, ny = x + dx, y + dy

            if 0 <= nx < MAZE_W and 0 <= ny < MAZE_H:
                if maze[ny][nx] != "#" and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    parent[(nx, ny)] = (x, y)
                    queue.append((nx, ny))

    if not found:
        return start

    # backtrack
    curr = target
    while parent[curr] != start:
        curr = parent[curr]

        if curr is None:
            return start

    return curr


# game state

def get_random_open_cell(maze):
    while True:
        x = random.randint(1, MAZE_W - 2)
        y = random.randint(1, MAZE_H - 2)

        if maze[y][x] == " ":
            return [x, y]
        

def reset_game():
    global player, enemy, game_state, maze, last_enemy_move,exit_pos

    maze = generate_maze(MAZE_W, MAZE_H)    

    player = get_random_open_cell(maze)
    enemy = get_random_open_cell(maze)

    exit_pos = get_random_open_cell(maze)
    maze[exit_pos[1]][exit_pos[0]] = "E"
    
    game_state = "PLAYING"
    last_enemy_move = time.time()


game_state = "PLAYING"

# handle input

def handle_input(event):
    global player, game_state

    if event.type != pygame.KEYDOWN:
        return

    if game_state != "PLAYING":
        if event.key == pygame.K_r:
            reset_game()
        return

    new_x, new_y = player

    if event.key == pygame.K_UP:
        new_y -= 1
    elif event.key == pygame.K_DOWN:
        new_y += 1
    elif event.key == pygame.K_LEFT:
        new_x -= 1
    elif event.key == pygame.K_RIGHT:
        new_x += 1

    if 0 <= new_x < MAZE_W and 0 <= new_y < MAZE_H:
        if maze[new_y][new_x] != "#":
            player = [new_x, new_y]

    if player == exit_pos:
        game_state = "WIN"

# Enemy movement

def update():
    global enemy, game_state, last_enemy_move

    if game_state != "PLAYING":
        return

    if time.time() - last_enemy_move > MOVE_DELAY:
        enemy = list(get_next_bfs(maze, tuple(enemy), tuple(player)))
        last_enemy_move = time.time()

    if enemy == player:
        game_state = "LOSE"

# UI

def draw():
    screen.fill((30, 30, 30))

    if game_state == "PLAYING":
        for y, row in enumerate(maze):
            for x, char in enumerate(row):

                rect = pygame.Rect(
                    offset_x + x * TILE,
                    offset_y + y * TILE,
                    TILE,
                    TILE
                )

                if char == "#":
                    pygame.draw.rect(screen, WALL_COLOR, rect)

                elif char == "E":
                    pygame.draw.rect(screen, EXIT_COLOR, rect)

        pygame.draw.rect(screen, ENEMY_COLOR,
            (offset_x + enemy[0]*TILE, offset_y + enemy[1]*TILE, TILE, TILE))

        pygame.draw.rect(screen, PLAYER_COLOR,
            (offset_x + player[0]*TILE, offset_y + player[1]*TILE, TILE, TILE))

    else:
        text = font.render(f"{game_state} (Press R)", True, (255, 255, 255))
        screen.blit(text, (WIDTH//2 - 150, HEIGHT//2))


# Game start
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 60)

TILE = min(WIDTH // MAZE_W, HEIGHT // MAZE_H)
offset_x = (WIDTH - MAZE_W * TILE) // 2
offset_y = (HEIGHT - MAZE_H * TILE) // 2

reset_game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        handle_input(event)

    update()
    draw()

    pygame.display.update()
    clock.tick(60)