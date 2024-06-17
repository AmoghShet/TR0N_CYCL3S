import curses
import time
import random
import heapq

# Initialize grid size and lightcycle positions
GRID_SIZE = 32
PLAYER_INITIAL_X, PLAYER_INITIAL_Y = GRID_SIZE // 2, GRID_SIZE - 2
RINZLER_INITIAL_X, RINZLER_INITIAL_Y = GRID_SIZE // 2, 1
PLAYER_TRAIL_LENGTH = 20
RINZLER_TRAIL_LENGTH = 25
OBSTACLE_COUNT = 10  # Number of obstacle groups

def create_grid(size):
    grid = [['.' for _ in range(size)] for _ in range(size)]
    return grid

def place_obstacles(grid, count):
    obstacles = []
    for _ in range(count):
        shape_type = random.choice(['HORIZONTAL', 'VERTICAL', 'L_SHAPE'])
        x, y = random.randint(1, GRID_SIZE-5), random.randint(1, GRID_SIZE-5)
        
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

def game_over(stdscr):
    h, w = stdscr.getmaxyx()
    msg = "Game Over"
    x = w // 2 - len(msg) // 2
    y = h // 2
    stdscr.addstr(y, x, msg, curses.color_pair(3))
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

def move_rinzler(rinzler, player, player_trail, rinzler_trail, obstacles):
    path = a_star((rinzler['x'], rinzler['y']), (player['x'], player['y']), player_trail, rinzler_trail, obstacles)
    if path:
        next_step = path[0]
        if next_step[0] > rinzler['x']:
            return 'RIGHT'
        elif next_step[0] < rinzler['x']:
            return 'LEFT'
        elif next_step[1] > rinzler['y']:
            return 'DOWN'
        elif next_step[1] < rinzler['y']:
            return 'UP'
    return 'DOWN'  # Default move if no path found

def main(stdscr):
    curses.curs_set(0)  # Hide the cursor
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)   # Player color
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)   # Player trail color
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)    # Game over message color
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK) # Rinzler color
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK) # Rinzler trail color
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Obstacle color

    grid = create_grid(GRID_SIZE)
    add_boundary_walls(grid)
    obstacles = place_obstacles(grid, OBSTACLE_COUNT)
    player = {'x': PLAYER_INITIAL_X, 'y': PLAYER_INITIAL_Y, 'symbol': '▮', 'trail_symbol': '║'}
    player_trail = []
    rinzler = {'x': RINZLER_INITIAL_X, 'y': RINZLER_INITIAL_Y, 'symbol': '▮', 'trail_symbol': '║'}
    rinzler_trail = []

    player_direction = None
    rinzler_direction = 'DOWN'

    reverse_direction = {
        'UP': 'DOWN',
        'DOWN': 'UP',
        'LEFT': 'RIGHT',
        'RIGHT': 'LEFT'
    }

    while True:
        print_grid(stdscr, grid, player, player_trail, rinzler, rinzler_trail, obstacles)
        key = stdscr.getch()

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
        if (player['x'] < 1 or player['x'] >= GRID_SIZE-1 or player['y'] < 1 or player['y'] >= GRID_SIZE-1 or
            rinzler['x'] < 1 or rinzler['x'] >= GRID_SIZE-1 or rinzler['y'] < 1 or rinzler['y'] >= GRID_SIZE-1):
            game_over(stdscr)
            break

        # Check for trail and obstacle collision
        if (check_collision(player, [player_trail, rinzler_trail], obstacles) or
            check_collision(rinzler, [player_trail, rinzler_trail], obstacles)):
            game_over(stdscr)
            break

        update_trail(player_trail, player, PLAYER_TRAIL_LENGTH)
        update_trail(rinzler_trail, rinzler, RINZLER_TRAIL_LENGTH)

if __name__ == "__main__":
    curses.wrapper(main)
