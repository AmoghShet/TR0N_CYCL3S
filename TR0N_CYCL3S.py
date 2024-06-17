import curses
import time
import random
import heapq
import pygame
import os

# Constants
GRID_SIZE = 32
PLAYER_INITIAL_X, PLAYER_INITIAL_Y = GRID_SIZE // 2, GRID_SIZE - 2
RINZLER_INITIAL_X, RINZLER_INITIAL_Y = GRID_SIZE // 2, 1
PLAYER_TRAIL_LENGTH = 20
RINZLER_TRAIL_LENGTH = 30
OBSTACLE_COUNT = 10
INITIAL_SPEED = 0.3
MAX_SPEED = 0.07
SPEED_UP_DURATION = 3

MUSIC_FOLDER = "MUSIC"
MUSIC_FILES = ["1. Disc Wars.mp3", "2. Derezzed.mp3", "3. The Game Has Changed.mp3"]

def create_grid(size):
    return [['.' for _ in range(size)] for _ in range(size)]

def place_obstacles(grid, count):
    obstacles = []
    for _ in range(count):
        shape_type = random.choice(['HORIZONTAL', 'VERTICAL', 'L_SHAPE'])
        x, y = random.randint(1, GRID_SIZE - 5), random.randint(1, GRID_SIZE - 5)
        
        if shape_type == 'HORIZONTAL':
            for i in range(3):
                grid[y][x + i] = '▬'
                obstacles.append({'x': x + i, 'y': y, 'symbol': '▬'})
        elif shape_type == 'VERTICAL':
            for i in range(3):
                grid[y + i][x] = '▮'
                obstacles.append({'x': x, 'y': y + i, 'symbol': '▮'})
        elif shape_type == 'L_SHAPE':
            for i in range(2):
                grid[y][x + i] = '▬'
                obstacles.append({'x': x + i, 'y': y, 'symbol': '▬'})
            for i in range(2):
                grid[y + i][x] = '▮'
                obstacles.append({'x': x, 'y': y + i, 'symbol': '▮'})
    return obstacles

def add_boundary_walls(grid):
    for i in range(GRID_SIZE):
        grid[0][i] = '─'
        grid[GRID_SIZE - 1][i] = '─'
        grid[i][0] = '|'
        grid[i][GRID_SIZE - 1] = '|'

def print_grid(stdscr, grid, player, player_trail, rinzler, rinzler_trail, obstacles):
    stdscr.clear()
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            stdscr.addch(y, x * 2, cell)  # Multiply x by 2 for better spacing
    for t in player_trail:
        stdscr.addch(t['y'], t['x'] * 2, t['symbol'], curses.color_pair(2))
    for t in rinzler_trail:
        stdscr.addch(t['y'], t['x'] * 2, t['symbol'], curses.color_pair(5))
    for obs in obstacles:
        stdscr.addch(obs['y'], obs['x'] * 2, obs['symbol'], curses.color_pair(6))
    stdscr.addch(player['y'], player['x'] * 2, player['symbol'], curses.color_pair(1))
    stdscr.addch(rinzler['y'], rinzler['x'] * 2, rinzler['symbol'], curses.color_pair(4))
    stdscr.refresh()

def update_trail(trail, lightcycle, trail_length):
    trail.append({'x': lightcycle['x'], 'y': lightcycle['y'], 'symbol': lightcycle['trail_symbol']})
    if len(trail) > trail_length:
        trail.pop(0)

def check_collision(lightcycle, trails, obstacles):
    for trail in trails:
        for t in trail:
            if lightcycle['x'] == t['x'] and lightcycle['y'] == t['y']:
                return True
    for obs in obstacles:
        if lightcycle['x'] == obs['x'] and lightcycle['y'] == obs['y']:
            return True
    return False

def game_over(stdscr, winner):
    h, w = stdscr.getmaxyx()
    if winner == 'player':
        msg1 = "RINZLER: DE-REZOLUTION"
        msg2 = "USER WINS"
        color = curses.color_pair(1)  # Player's cyan
    else:
        msg1 = "USER: DE-REZOLUTION"
        msg2 = "RINZLER WINS"
        color = curses.color_pair(4)  # Rinzler's yellow

    box_width = max(len(msg1), len(msg2)) + 4
    box_height = 5
    box_x = (w - box_width) // 2
    box_y = (h - box_height) // 2

    # Draw box
    stdscr.attron(curses.color_pair(3))
    stdscr.addstr(box_y, box_x, "+" + "-" * (box_width - 2) + "+")
    for i in range(1, box_height - 1):
        stdscr.addstr(box_y + i, box_x, "|" + " " * (box_width - 2) + "|")
    stdscr.addstr(box_y + box_height - 1, box_x, "+" + "-" * (box_width - 2) + "+")
    stdscr.attroff(curses.color_pair(3))

    # Display messages
    stdscr.attron(color)
    stdscr.addstr(box_y + 1, box_x + 2, msg1)
    stdscr.addstr(box_y + 2, box_x + 2, msg2)
    stdscr.attroff(color)

    stdscr.refresh()
    time.sleep(2)

def a_star(start, goal, player_trail, rinzler_trail, obstacles):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_neighbors(node):
        neighbors = [
            (node[0] + 1, node[1]),
            (node[0] - 1, node[1]),
            (node[0], node[1] + 1),
            (node[0], node[1] - 1)
        ]
        valid_neighbors = []
        for x, y in neighbors:
            if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
                if not any(t['x'] == x and t['y'] == y for t in player_trail + rinzler_trail + obstacles):
                    valid_neighbors.append((x, y))
        return valid_neighbors

    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for neighbor in get_neighbors(current):
            tentative_g_score = g_score[current] + 1

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return []

def evaluate_future_moves(rinzler, player, player_trail, rinzler_trail, obstacles, depth=3):
    possible_moves = {
        'UP': (0, -1),
        'DOWN': (0, 1),
        'LEFT': (-1, 0),
        'RIGHT': (1, 0)
    }

    best_move = None
    best_score = float('inf')

    for move, (dx, dy) in possible_moves.items():
        future_rinzler = {'x': rinzler['x'] + dx, 'y': rinzler['y'] + dy}
        if check_collision(future_rinzler, [player_trail, rinzler_trail], obstacles):
            continue

        path = a_star((future_rinzler['x'], future_rinzler['y']), (player['x'], player['y']), player_trail, rinzler_trail, obstacles)
        if not path:
            continue

        future_score = 0
        for future_step in path[:depth]:
            future_score += abs(future_step[0] - player['x']) + abs(future_step[1] - player['y'])

        if future_score < best_score:
            best_score = future_score
            best_move = move

    return best_move if best_move else 'DOWN'

def move_rinzler(rinzler, player, player_trail, rinzler_trail, obstacles):
    return evaluate_future_moves(rinzler, player, player_trail, rinzler_trail, obstacles)

def get_speed(elapsed_time):
    if elapsed_time < SPEED_UP_DURATION:
        return INITIAL_SPEED - (elapsed_time / SPEED_UP_DURATION) * (INITIAL_SPEED - MAX_SPEED)
    return MAX_SPEED

def play_music():
    pygame.mixer.init()
    music_files = [os.path.join(MUSIC_FOLDER, file) for file in MUSIC_FILES]
    pygame.mixer.music.load(music_files[0])
    for file in music_files[1:]:
        pygame.mixer.music.queue(file)
    pygame.mixer.music.set_endevent(pygame.USEREVENT)
    pygame.mixer.music.play(-1)  # Loop indefinitely

def show_menu(stdscr):
    menu_title = "TR0N: CYCL3S"
    menu_options = ["P - Play", "Q - Quit"]
    
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    
    title_x = w // 2 - len(menu_title) // 2
    title_y = h // 2 - 2
    stdscr.addstr(title_y, title_x, menu_title)
    
    for i, option in enumerate(menu_options):
        option_x = w // 2 - len(option) // 2
        option_y = h // 2 + i
        stdscr.addstr(option_y, option_x, option)
    
    stdscr.refresh()
    
    while True:
        key = stdscr.getch()
        if key == ord('p') or key == ord('P'):
            return 'play'
        elif key == ord('q') or key == ord('Q'):
            return 'quit'

def main(stdscr):
    curses.curs_set(0)  # Hide the cursor
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)   # Player color
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)   # Player trail color
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)    # Game over message color
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK) # Rinzler color
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK) # Rinzler trail color
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Obstacle color

    play_music()

    while True:
        action = show_menu(stdscr)
        if action == 'quit':
            pygame.mixer.music.stop()
            break

        grid = create_grid(GRID_SIZE)
        add_boundary_walls(grid)
        obstacles = place_obstacles(grid, OBSTACLE_COUNT)
        player = {'x': PLAYER_INITIAL_X, 'y': PLAYER_INITIAL_Y, 'symbol': '▮', 'trail_symbol': '║'}
        player_trail = []
        rinzler = {'x': RINZLER_INITIAL_X, 'y': RINZLER_INITIAL_Y, 'symbol': '▮', 'trail_symbol': '║'}
        rinzler_trail = []

        player_direction = 'UP'
        rinzler_direction = 'DOWN'

        stdscr.nodelay(1)  # Make getch() non-blocking
        key = -1
        start_time = time.time()

        while True:
            frame_start_time = time.time()

            # Check terminal size
            height, width = stdscr.getmaxyx()
            required_height = GRID_SIZE
            required_width = GRID_SIZE * 2  # Because x is multiplied by 2 for better spacing

            if height < required_height or width < required_width:
                stdscr.clear()
                stdscr.addstr(0, 0, "Terminal window is too small. Please resize the window.")
                stdscr.refresh()
                time.sleep(1)
                continue

            # Handle player input
            new_key = stdscr.getch()
            if new_key != -1:
                key = new_key

            if key == curses.KEY_UP and player_direction != 'DOWN':
                player['symbol'] = '▮'
                player['trail_symbol'] = '║'
                player_direction = 'UP'
            elif key == curses.KEY_DOWN and player_direction != 'UP':
                player['symbol'] = '▮'
                player['trail_symbol'] = '║'
                player_direction = 'DOWN'
            elif key == curses.KEY_LEFT and player_direction != 'RIGHT':
                player['symbol'] = '▬'
                player['trail_symbol'] = '═'
                player_direction = 'LEFT'
            elif key == curses.KEY_RIGHT and player_direction != 'LEFT':
                player['symbol'] = '▬'
                player['trail_symbol'] = '═'
                player_direction = 'RIGHT'

            # Update player position
            if player_direction == 'UP':
                player['y'] -= 1
            elif player_direction == 'DOWN':
                player['y'] += 1
            elif player_direction == 'LEFT':
                player['x'] -= 1
            elif player_direction == 'RIGHT':
                player['x'] += 1

            # Update Rinzler's direction and position
            rinzler_direction = move_rinzler(rinzler, player, player_trail, rinzler_trail, obstacles)

            if rinzler_direction == 'UP':
                rinzler['symbol'] = '▮'
                rinzler['trail_symbol'] = '║'
                rinzler['y'] -= 1
            elif rinzler_direction == 'DOWN':
                rinzler['symbol'] = '▮'
                rinzler['trail_symbol'] = '║'
                rinzler['y'] += 1
            elif rinzler_direction == 'LEFT':
                rinzler['symbol'] = '▬'
                rinzler['trail_symbol'] = '═'
                rinzler['x'] -= 1
            elif rinzler_direction == 'RIGHT':
                rinzler['symbol'] = '▬'
                rinzler['trail_symbol'] = '═'
                rinzler['x'] += 1

            # Check for boundary collision
            if (player['x'] < 1 or player['x'] >= GRID_SIZE - 1 or player['y'] < 1 or player['y'] >= GRID_SIZE - 1):
                game_over(stdscr, 'rinzler')
                break
            if (rinzler['x'] < 1 or rinzler['x'] >= GRID_SIZE - 1 or rinzler['y'] < 1 or rinzler['y'] >= GRID_SIZE - 1):
                game_over(stdscr, 'player')
                break

            # Check for trail and obstacle collision
            if check_collision(player, [player_trail, rinzler_trail], obstacles):
                game_over(stdscr, 'rinzler')
                break
            if check_collision(rinzler, [player_trail, rinzler_trail], obstacles):
                game_over(stdscr, 'player')
                break

            update_trail(player_trail, player, PLAYER_TRAIL_LENGTH)
            update_trail(rinzler_trail, rinzler, RINZLER_TRAIL_LENGTH)

            print_grid(stdscr, grid, player, player_trail, rinzler, rinzler_trail, obstacles)
            
            # Ensure consistent frame rate
            elapsed_time = time.time() - start_time
            speed = get_speed(elapsed_time)
            frame_elapsed_time = time.time() - frame_start_time
            time.sleep(max(speed - frame_elapsed_time, 0))

if __name__ == "__main__":
    curses.wrapper(main)
