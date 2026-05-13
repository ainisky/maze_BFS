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
    
    last_enemy_move = time.time()

# handle input

def handle_input(event):
    global player, game_state

    if event.type != pygame.KEYDOWN:
        return

    if game_state in ["MENU", "WIN", "LOSE"]:
        if event.key == pygame.K_SPACE:
            reset_game()
            game_state = "PLAYING"
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

stars = []

for i in range(80):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    stars.append((x, y))

def draw():
    screen.fill((12, 18, 30))

    for x, y in stars:
        pygame.draw.circle(screen, (255, 255, 255), (x, y), 1)

    FLOOR_A = (90, 140, 200)  
    FLOOR_B = (100, 150, 210)  
    WALL_COLOR = (210, 210, 220)
    WALL_SHADOW = (170, 170, 180)
    WALL_HIGHLIGHT = (245, 245, 250)
    
    if game_state == "MENU":
        
        title = font.render("ALIEN ESCAPE", True, (120, 255, 180))

        story_lines = [
            "You are an alien stranded on Earth and captured!",
            "Escape the lab and find your spaceship",
            "before the scientist catches you again!"
        ]

        screen.blit(
            title,
            (WIDTH//2 - title.get_width()//2, 140)
        )

        small_font = pygame.font.SysFont(None, 32)

        for i, line in enumerate(story_lines):
            text = small_font.render(line, True, (230, 230, 230))

            screen.blit(
                text,
                (WIDTH//2 - text.get_width()//2, 250 + i * 40)
            )

        start_text = small_font.render(
            "Press SPACE to Start",
            True,
            (255, 255, 100)
        )

        screen.blit(
            start_text,
            (WIDTH//2 - start_text.get_width()//2, 420)
        )

        return

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

                    pygame.draw.line(screen, WALL_HIGHLIGHT, rect.topleft, rect.topright)
                    pygame.draw.line(screen, WALL_HIGHLIGHT, rect.topleft, rect.bottomleft)

                    pygame.draw.line(screen, WALL_SHADOW, rect.bottomleft, rect.bottomright)
                    pygame.draw.line(screen, WALL_SHADOW, rect.topright, rect.bottomright)

                else:
                    color = FLOOR_A if (x + y) % 2 == 0 else FLOOR_B
                    pygame.draw.rect(screen, color, rect)

        screen.blit(
            ufo_img,
            (offset_x + exit_pos[0]*TILE,
            offset_y + exit_pos[1]*TILE)
        )

        screen.blit(
            enemy_img,
            (offset_x + enemy[0]*TILE,
            offset_y + enemy[1]*TILE)
        )

        screen.blit(
            alien_img,
            (offset_x + player[0]*TILE,
            offset_y + player[1]*TILE)
        )

    tint = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    tint.fill((100, 180, 255, 20))
    screen.blit(tint, (0, 0))

    if game_state == "WIN":
        msg = "YOU WIN! Press SPACE to restart"
        shadow = font.render(msg, True, (0, 0, 0))
        text = font.render(msg, True, (255, 255, 255))

        screen.blit(shadow, (WIDTH//2 - text.get_width()//2 + 2, HEIGHT//2 + 2))
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))
        return


    if game_state == "LOSE":
        msg = "YOU LOSE! Press SPACE to restart"
        shadow = font.render(msg, True, (0, 0, 0))
        text = font.render(msg, True, (255, 100, 100))

        screen.blit(shadow, (WIDTH//2 - text.get_width()//2 + 2, HEIGHT//2 + 2))
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))
        return

def handle_menu_input(event):
    global game_state

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            game_state = "PLAYING"
            reset_game()

# Game start
pygame.init()

TILE = min(WIDTH // MAZE_W, HEIGHT // MAZE_H)
offset_x = (WIDTH - MAZE_W * TILE) // 2
offset_y = (HEIGHT - MAZE_H * TILE) // 2

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 60)

alien_img = pygame.image.load("assets/alien.png")
enemy_img = pygame.image.load("assets/enemy.png")
ufo_img = pygame.image.load("assets/ufo.png")

alien_img = pygame.transform.scale(alien_img, (TILE, TILE))
enemy_img = pygame.transform.scale(enemy_img, (TILE, TILE))
ufo_img = pygame.transform.scale(ufo_img, (TILE, TILE))

game_state = "MENU"

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                pygame.quit()
                sys.exit()

        if game_state == "MENU":
            handle_menu_input(event)
        else:
            handle_input(event)
    if game_state == "PLAYING":
        update()
        
    draw()

    pygame.display.update()
    clock.tick(60)