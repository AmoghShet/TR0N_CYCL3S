import curses

# Constants for grid size and initial lightcycle position
GRID_SIZE = 64
START_X = GRID_SIZE // 2
START_Y = GRID_SIZE // 2

# Function to create an empty grid
def create_grid(size):
    return [['.' for _ in range(size)] for _ in range(size)]

# Function to print the grid
def print_grid(grid, stdscr):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            stdscr.addch(y, x * 2, cell)

# Main game loop
def main(stdscr):
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(1)   # Set getch() to be non-blocking
    stdscr.timeout(100) # Set a delay for screen updates

    grid = create_grid(GRID_SIZE)
    x, y = START_X, START_Y
    direction = 'right'
    grid[y][x] = '▬'

    while True:
        key = stdscr.getch()

        # Change direction based on arrow key input
        if key == curses.KEY_UP and direction != 'down':
            direction = 'up'
        elif key == curses.KEY_DOWN and direction != 'up':
            direction = 'down'
        elif key == curses.KEY_LEFT and direction != 'right':
            direction = 'left'
        elif key == curses.KEY_RIGHT and direction != 'left':
            direction = 'right'

        # Update position
        if direction == 'up':
            y -= 1
            grid[y][x] = '▮'
        elif direction == 'down':
            y += 1
            grid[y][x] = '▮'
        elif direction == 'left':
            x -= 1
            grid[y][x] = '▬'
        elif direction == 'right':
            x += 1
            grid[y][x] = '▬'

        # Clear the screen
        stdscr.clear()

        # Print the updated grid
        print_grid(grid, stdscr)

        # Refresh the screen
        stdscr.refresh()

        # Exit if the lightcycle goes out of bounds
        if x < 0 or x >= GRID_SIZE or y < 0 or y >= GRID_SIZE:
            break

curses.wrapper(main)
