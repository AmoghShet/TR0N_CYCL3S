import curses
import time

# Initialize grid size and lightcycle position
GRID_SIZE = 32
INITIAL_X, INITIAL_Y = GRID_SIZE // 2, GRID_SIZE // 2
TRAIL_LENGTH = 20

def create_grid(size):
    grid = [['.' for _ in range(size)] for _ in range(size)]
    return grid

def print_grid(stdscr, grid, lightcycle, trail):
    stdscr.clear()
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            stdscr.addch(y, x * 2, cell)  # Multiply x by 2 for better spacing
    for t in trail:
        stdscr.addch(t['y'], t['x'] * 2, t['symbol'], curses.color_pair(2))
    stdscr.addch(lightcycle['y'], lightcycle['x'] * 2, lightcycle['symbol'], curses.color_pair(1))
    stdscr.refresh()

def update_trail(trail, lightcycle):
    trail.append({'x': lightcycle['x'], 'y': lightcycle['y'], 'symbol': lightcycle['trail_symbol']})
    if len(trail) > TRAIL_LENGTH:
        trail.pop(0)

def check_collision(lightcycle, trail):
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
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

    grid = create_grid(GRID_SIZE)
    lightcycle = {'x': INITIAL_X, 'y': INITIAL_Y, 'symbol': '▮', 'trail_symbol': '║'}
    trail = []

    direction = None

    while True:
        print_grid(stdscr, grid, lightcycle, trail)
        key = stdscr.getch()

        if key == curses.KEY_UP:
            lightcycle['symbol'] = '▮'
            lightcycle['trail_symbol'] = '║'
            direction = 'UP'
        elif key == curses.KEY_DOWN:
            lightcycle['symbol'] = '▮'
            lightcycle['trail_symbol'] = '║'
            direction = 'DOWN'
        elif key == curses.KEY_LEFT:
            lightcycle['symbol'] = '▬'
            lightcycle['trail_symbol'] = '═'
            direction = 'LEFT'
        elif key == curses.KEY_RIGHT:
            lightcycle['symbol'] = '▬'
            lightcycle['trail_symbol'] = '═'
            direction = 'RIGHT'

        if direction == 'UP':
            lightcycle['y'] -= 1
        elif direction == 'DOWN':
            lightcycle['y'] += 1
        elif direction == 'LEFT':
            lightcycle['x'] -= 1
        elif direction == 'RIGHT':
            lightcycle['x'] += 1

        # Check for boundary collision
        if lightcycle['x'] < 0 or lightcycle['x'] >= GRID_SIZE or lightcycle['y'] < 0 or lightcycle['y'] >= GRID_SIZE:
            game_over(stdscr)
            break

        # Check for trail collision
        if check_collision(lightcycle, trail):
            game_over(stdscr)
            break

        update_trail(trail, lightcycle)

if __name__ == "__main__":
    curses.wrapper(main)
