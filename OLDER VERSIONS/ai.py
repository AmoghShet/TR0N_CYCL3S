import curses
import time
import random

# Initialize grid size and lightcycle positions
GRID_SIZE = 32
PLAYER_INITIAL_X, PLAYER_INITIAL_Y = GRID_SIZE // 2, GRID_SIZE - 1
RINZLER_INITIAL_X, RINZLER_INITIAL_Y = GRID_SIZE // 2, 0
TRAIL_LENGTH = 20

def create_grid(size):
    grid = [['.' for _ in range(size)] for _ in range(size)]
    return grid

def print_grid(stdscr, grid, player, player_trail, rinzler, rinzler_trail):
    stdscr.clear()
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            stdscr.addch(y, x * 2, cell)  # Multiply x by 2 for better spacing
    for t in player_trail:
        stdscr.addch(t['y'], t['x'] * 2, t['symbol'], curses.color_pair(2))
    for t in rinzler_trail:
        stdscr.addch(t['y'], t['x'] * 2, t['symbol'], curses.color_pair(5))
    stdscr.addch(player['y'], player['x'] * 2, player['symbol'], curses.color_pair(1))
    stdscr.addch(rinzler['y'], rinzler['x'] * 2, rinzler['symbol'], curses.color_pair(4))
    stdscr.refresh()

def update_trail(trail, lightcycle):
    trail.append({'x': lightcycle['x'], 'y': lightcycle['y'], 'symbol': lightcycle['trail_symbol']})
    if len(trail) > TRAIL_LENGTH:
        trail.pop(0)

def check_collision(lightcycle, trails):
    for trail in trails:
        for t in trail:
            if lightcycle['x'] == t['x'] and lightcycle['y'] == t['y']:
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

def move_rinzler(rinzler, player, player_trail, rinzler_trail, grid_size, rinzler_direction):
    possible_moves = {
        'UP': ('UP', 'LEFT', 'RIGHT'),
        'DOWN': ('DOWN', 'LEFT', 'RIGHT'),
        'LEFT': ('UP', 'DOWN', 'LEFT'),
        'RIGHT': ('UP', 'DOWN', 'RIGHT')
    }

    reverse_direction = {
        'UP': 'DOWN',
        'DOWN': 'UP',
        'LEFT': 'RIGHT',
        'RIGHT': 'LEFT'
    }

    safe_moves = []
    current_possible_moves = possible_moves[rinzler_direction]

    for move in current_possible_moves:
        next_x, next_y = rinzler['x'], rinzler['y']
        if move == 'UP':
            next_y -= 1
        elif move == 'DOWN':
            next_y += 1
        elif move == 'LEFT':
            next_x -= 1
        elif move == 'RIGHT':
            next_x += 1

        if 0 <= next_x < grid_size and 0 <= next_y < grid_size:
            if not any(t['x'] == next_x and t['y'] == next_y for t in player_trail + rinzler_trail):
                safe_moves.append((move, next_x, next_y))

    if not safe_moves:
        return random.choice(current_possible_moves)  # Default to random move if no safe move found

    best_move = safe_moves[0][0]
    best_distance = float('inf')

    for move, next_x, next_y in safe_moves:
        distance = abs(next_x - player['x']) + abs(next_y - player['y'])
        if distance < best_distance:
            best_move = move
            best_distance = distance

    return best_move

def main(stdscr):
    curses.curs_set(0)  # Hide the cursor
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)   # Player color
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)   # Player trail color
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)    # Game over message color
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK) # Rinzler color
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK) # Rinzler trail color

    grid = create_grid(GRID_SIZE)
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
        print_grid(stdscr, grid, player, player_trail, rinzler, rinzler_trail)
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
        rinzler_direction = move_rinzler(rinzler, player, player_trail, rinzler_trail, GRID_SIZE, rinzler_direction)

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
        if (player['x'] < 0 or player['x'] >= GRID_SIZE or player['y'] < 0 or player['y'] >= GRID_SIZE or
            rinzler['x'] < 0 or rinzler['x'] >= GRID_SIZE or rinzler['y'] < 0 or rinzler['y'] >= GRID_SIZE):
            game_over(stdscr)
            break

        # Check for trail collision
        if (check_collision(player, [player_trail, rinzler_trail]) or
            check_collision(rinzler, [player_trail, rinzler_trail])):
            game_over(stdscr)
            break

        update_trail(player_trail, player)
        update_trail(rinzler_trail, rinzler)

if __name__ == "__main__":
    curses.wrapper(main)
