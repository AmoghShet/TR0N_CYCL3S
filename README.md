# TR0N: CYCL3S Game - README

## Overview

TR0N: CYCL3S is a terminal-based lightcycle game inspired by the TRON franchise. The game features two characters: the Player and an AI opponent named Rinzler. Each character leaves a trail behind them as they move on a grid. The objective is to avoid colliding with the trails or obstacles while trying to outmaneuver the opponent.

## Game Mechanics

1. **Grid**: The game is played on a 32x32 grid.
2. **Characters**:
   - **Player**: Controlled by the user using the arrow keys.
   - **Rinzler**: Controlled by an AI using A* pathfinding and predictive logic.
3. **Trails**: Both the Player and Rinzler leave a trail as they move. Colliding with any trail results in a game over.
4. **Obstacles**: Randomly placed obstacles add complexity to the game.
5. **Boundaries**: The grid has boundary walls that the characters cannot pass through.
6. **Music**: Background music plays during the game, enhancing the gameplay experience.

## Controls

- **Up Arrow**: Move up
- **Down Arrow**: Move down
- **Left Arrow**: Move left
- **Right Arrow**: Move right
- **P**: Play the game from the main menu
- **Q**: Quit the game from the main menu

## Game Logic

### Initialization

#### Constants

- **GRID_SIZE**: Defines the size of the grid (32x32).
- **PLAYER_INITIAL_X, PLAYER_INITIAL_Y**: Initial coordinates for the Player.
- **RINZLER_INITIAL_X, RINZLER_INITIAL_Y**: Initial coordinates for Rinzler.
- **PLAYER_TRAIL_LENGTH**: Maximum length of the Player's trail.
- **RINZLER_TRAIL_LENGTH**: Maximum length of Rinzler's trail.
- **OBSTACLE_COUNT**: Number of obstacles to be placed on the grid.
- **INITIAL_SPEED, MAX_SPEED, SPEED_UP_DURATION**: Parameters for controlling the game's speed dynamics.
- **MUSIC_FOLDER, MUSIC_FILES**: Paths to music files for background music.

#### Functions

1. **create_grid(size)**: Initializes the game grid with '.' representing empty cells.
2. **place_obstacles(grid, count)**: Places a specified number of obstacles on the grid in different shapes (horizontal, vertical, L-shaped).
3. **add_boundary_walls(grid)**: Adds boundary walls around the grid.
4. **print_grid(stdscr, grid, player, player_trail, rinzler, rinzler_trail, obstacles)**: Renders the grid and all game elements on the screen.
5. **update_trail(trail, lightcycle, trail_length)**: Updates the trail for a given lightcycle, maintaining a maximum trail length.
6. **check_collision(lightcycle, trails, obstacles)**: Checks for collisions between a lightcycle and trails or obstacles.
7. **game_over(stdscr, winner)**: Displays the game over message indicating the winner.
8. **a_star(start, goal, player_trail, rinzler_trail, obstacles)**: Implements the A* pathfinding algorithm to find a path from start to goal.
9. **evaluate_future_moves(rinzler, player, player_trail, rinzler_trail, obstacles, depth=3)**: Predicts the best move for Rinzler based on future possible positions.
10. **move_rinzler(rinzler, player, player_trail, rinzler_trail, obstacles)**: Determines and returns Rinzler's next move using predictive logic.
11. **get_speed(elapsed_time)**: Adjusts the game speed dynamically based on elapsed time.
12. **play_music()**: Plays background music using pygame.
13. **show_menu(stdscr)**: Displays the main menu with options to play or quit the game.
14. **main(stdscr)**: Main function to run the game using curses.

### Game Loop

1. **Menu Display**: Shows the main menu with options to play or quit.
2. **Game Start**: Initializes the Player and Rinzler positions and directions.
3. **Input Handling**: Captures player input for movement.
4. **Movement Update**:
   - Updates the Player's position based on input.
   - Determines Rinzler's next move using the `evaluate_future_moves` function, which predicts the best move to get closer to the Player while avoiding collisions.
5. **Collision Check**:
   - Checks for collisions with trails, obstacles, and boundary walls.
   - Ends the game if a collision is detected, declaring the winner.
6. **Trail Update**: Updates the trails for both the Player and Rinzler, maintaining a maximum trail length.
7. **Rendering**: Renders the grid, characters, and trails on the screen.
8. **Speed Control**: Adjusts the game speed dynamically based on elapsed time.

### Detailed Breakdown

#### Initialization

1. **Grid Creation**: The game initializes a 32x32 grid filled with '.' to represent empty cells.
2. **Obstacles Placement**: Randomly places a specified number of obstacles in different shapes (horizontal, vertical, L-shaped).
3. **Boundary Walls**: Adds boundary walls around the grid.

#### Game Loop

1. **Menu Display**:
   - Displays the game title and menu options.
   - Captures user input to start the game or quit.

2. **Game Start**:
   - Initializes the Player and Rinzler positions and directions.
   - Initializes trails and obstacles on the grid.
   - Sets the initial speed and start time.

3. **Input Handling**:
   - Captures player input using the arrow keys.
   - Updates the Player's direction based on input.
   - Ensures that the Player does not reverse direction instantly.

4. **Movement Update**:
   - Updates the Player's position based on the current direction.
   - Determines Rinzler's next move using the `evaluate_future_moves` function.
   - Updates Rinzler's position based on the determined move.

5. **Collision Check**:
   - Checks for collisions with trails, obstacles, and boundary walls for both the Player and Rinzler.
   - Ends the game if a collision is detected, displaying the appropriate game over message.

6. **Trail Update**:
   - Updates the trails for both the Player and Rinzler.
   - Ensures that the trails do not exceed the maximum length.

7. **Rendering**:
   - Renders the grid, characters, and trails on the screen.
   - Uses color pairs to differentiate between the Player, Rinzler, trails, and obstacles.

8. **Speed Control**:
   - Adjusts the game speed dynamically based on the elapsed time since the start of the game.
   - Gradually increases the game speed to a maximum limit over a specified duration.

#### Pathfinding and AI

- **A* Algorithm**:
  - Implements the A* pathfinding algorithm to find the shortest path from Rinzler's current position to the Player's position.
  - Uses a heuristic function to estimate the cost from the current position to the goal.
  - Considers valid neighboring positions that are not occupied by trails or obstacles.

- **Predictive Logic**:
  - Evaluates future possible moves for Rinzler based on the predicted positions of the Player.
  - Uses the A* algorithm to find paths for each possible move.
  - Chooses the move that minimizes the distance to the Player while avoiding collisions.

#### Dynamic Speed Adjustment

- **Speed Control**:
  - Uses the `get_speed` function to dynamically adjust the game speed based on the elapsed time.
  - Gradually decreases the frame delay to increase the game speed over time.
  - Ensures a consistent frame rate by accounting for the time taken to render each frame.

## Dependencies

- **curses**: For terminal-based user interface.
- **time**: For handling delays and game speed.
- **random**: For random obstacle placement.
- **heapq**: For priority queue in A* algorithm.
- **pygame**: For playing background music.
- **os**: For file handling.

## Running the Game

1. Ensure all dependencies are installed.
2. Run the script in a terminal that supports curses (e.g., Linux terminal, macOS Terminal, or Windows with WSL).
3. Use the arrow keys to control the Player and try to outmaneuver Rinzler.
4. Enjoy the game with background music!

```bash
python TR0N_CYCL3S.py
```

## Notes

- Make sure your terminal window is large enough to accommodate the grid. Resize the window if necessary.
- The game is designed for a grid of size 32x32, and changing the grid size might require adjustments to other parameters.
- Background music requires pygame and valid music files in the specified folder.

Enjoy the game and have fun in the digital world of TR0N: CYCL3S!
