import curses

# Initialize grid size and lightcycle position
GRID_SIZE = 32
INITIAL_X, INITIAL_Y = GRID_SIZE // 2, GRID_SIZE // 2

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
    if len(trail) == 10:
        trail.pop(0)
    trail.append({'x': lightcycle['x'], 'y': lightcycle['y'], 'symbol': lightcycle['trail_symbol']})

def main(stdscr):
    curses.curs_set(0)  # Hide the cursor
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)

    grid = create_grid(GRID_SIZE)
    lightcycle = {'x': INITIAL_X, 'y': INITIAL_Y, 'symbol': '▮', 'trail_symbol': '║'}
    trail = []

    direction = None

    while True:
        print_grid(stdscr, grid, lightcycle, trail)
        key = stdscr.getch()

        if key == curses.KEY_UP and lightcycle['y'] > 0:
            lightcycle['symbol'] = '▮'
            lightcycle['trail_symbol'] = '║'
            direction = 'UP'
        elif key == curses.KEY_DOWN and lightcycle['y'] < GRID_SIZE - 1:
            lightcycle['symbol'] = '▮'
            lightcycle['trail_symbol'] = '║'
            direction = 'DOWN'
        elif key == curses.KEY_LEFT and lightcycle['x'] > 0:
            lightcycle['symbol'] = '▬'
            lightcycle['trail_symbol'] = '═'
            direction = 'LEFT'
        elif key == curses.KEY_RIGHT and lightcycle['x'] < GRID_SIZE - 1:
            lightcycle['symbol'] = '▬'
            lightcycle['trail_symbol'] = '═'
            direction = 'RIGHT'

        if direction == 'UP':
            update_trail(trail, lightcycle)
            lightcycle['y'] -= 1
        elif direction == 'DOWN':
            update_trail(trail, lightcycle)
            lightcycle['y'] += 1
        elif direction == 'LEFT':
            update_trail(trail, lightcycle)
            lightcycle['x'] -= 1
        elif direction == 'RIGHT':
            update_trail(trail, lightcycle)
            lightcycle['x'] += 1

if __name__ == "__main__":
    curses.wrapper(main)
