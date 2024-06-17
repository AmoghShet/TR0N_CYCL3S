def create_grid(size):
    grid = [['.' for _ in range(size)] for _ in range(size)]
    return grid

def print_grid(grid):
    for row in grid:
        print(' '.join(row))

def main():
    size = 32
    grid = create_grid(size)
    print_grid(grid)

if __name__ == "__main__":
    main()
