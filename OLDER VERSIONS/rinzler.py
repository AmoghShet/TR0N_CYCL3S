import curses
import time

# Initialize grid size and lightcycle positions
GRID_SIZE = 32
PLAYER_INITIAL_X, PLAYER_INITIAL_Y = GRID_SIZE // 2, GRID_SIZE - 1
RINZLER_INITIAL_X, RINZLER_INITIAL_Y = GRID_SIZE // 2, 0
TRAIL_LENGTH = 10

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

    while True:
        print_grid(stdscr, grid, player, player_trail, rinzler, rinzler_trail)
        key = stdscr.getch()

        if key == curses.KEY_UP:
            player['symbol'] = '▮'
            player['trail_symbol'] = '║'
            player_direction = 'UP'
        elif key == curses.KEY_DOWN:
            player['symbol'] = '▮'
            player['trail_symbol'] = '║'
            player_direction = 'DOWN'
        elif key == curses.KEY_LEFT:
            player['symbol'] = '▬'
            player['trail_symbol'] = '═'
            player_direction = 'LEFT'
        elif key == curses.KEY_RIGHT:
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
        if rinzler_direction == 'DOWN':
            rinzler['symbol'] = '▮'
            rinzler['trail_symbol'] = '║'
            rinzler['y'] += 1
        elif rinzler_direction == 'UP':
            rinzler['symbol'] = '▮'
            rinzler['trail_symbol'] = '║'
            rinzler['y'] -= 1
        elif rinzler_direction == 'LEFT':
            rinzler['symbol'] = '▬'
            rinzler['trail_symbol'] = '═'
            rinzler['x'] -= 1
        elif rinzler_direction == 'RIGHT':
            rinzler['symbol'] = '▬'
            rinzler['trail_symbol'] = '═'
            rinzler['x'] += 1

        # Change Rinzler's direction randomly for demonstration
        if rinzler['x'] <= 0 or rinzler['x'] >= GRID_SIZE - 1 or rinzler['y'] <= 0 or rinzler['y'] >= GRID_SIZE - 1:
            rinzler_direction = ['UP', 'DOWN', 'LEFT', 'RIGHT'][rinzler_direction != 'DOWN']

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
