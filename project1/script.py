"""
script.py

Description:
This program implements a two-player Battleship game using Pygame. Players can place ships on a grid and take turns attacking each other's ships.

Inputs:
- Mouse clicks for ship placement and attacks
- Keyboard input for rotating ships during placement

Output:
- Graphical display of the game board, ship placements, and attack results

Other sources:
- Pygame documentation for GUI implementation
- Claude 3.5 Sonnet for debugging and optimization suggestions
- Various Stack Overflow and GeeksforGeeks pages

Authors: Ethan Dirkes, Chase Entwistle, Christopher Gronewold, Tommy Lam, Zonaid Prithu
Creation date: 9/6/2024
"""

import pygame
import sys

# Initialize Pygame and set up the display
pygame.init()
screen = pygame.display.set_mode((1000, 750))  # Create a 1000x750 pixel window
font = pygame.font.Font(None, 36)  # Set up a default font for text rendering

# Define color constants for easy reference throughout the game
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)
LIGHT_BLUE = (100, 100, 255)
RED = (255, 0, 0)
GRID_BLUE = (10, 150, 210)

# Global variables to store game state
num_ships = 0  # Number of ships each player will have
player1_ships = None  # Stores Player 1's ship placements
player2_ships = None  # Stores Player 2's ship placements

# Grids to track attacks for each player (10x10 grid)
player1_attack_grid = [[None for _ in range(10)] for _ in range(10)]
player2_attack_grid = [[None for _ in range(10)] for _ in range(10)]

# Variables to store hit information for each player
player1_hits = None  # Will be initialized as a 10x10 grid
player2_hits = None  # Will be initialized as a 10x10 grid

# Lists to store sunk ships for each player
player1_sunk_ships = []
player2_sunk_ships = []


def draw_button(text, x, y, w, h, color, action=None, enabled=True):
    """
    Draw an interactive button on the screen.

    Args:
    text (str): Text to display on the button
    x, y (int): Top-left coordinates of the button
    w, h (int): Width and height of the button
    color (tuple): RGB color of the button
    action (function): Function to call when the button is clicked
    enabled (bool): Whether the button is clickable
    """
    mouse = pygame.mouse.get_pos()  # Get current mouse position
    click = pygame.mouse.get_pressed()  # Check if mouse buttons are pressed

    # Draw the button rectangle
    if enabled:
        pygame.draw.rect(screen, color, (x, y, w, h))
    else:
        pygame.draw.rect(screen, DARK_GRAY, (x, y, w, h))  # Use dark gray for disabled buttons

    # Render the button text
    text_surf = font.render(text, True, BLACK)
    # Calculate position to center the text on the button
    text_pos = (x + w // 2 - text_surf.get_width() // 2, y + h // 2 - text_surf.get_height() // 2)
    screen.blit(text_surf, text_pos)

    # Check if the mouse is over the button and it's clicked
    if enabled and x < mouse[0] < x + w and y < mouse[1] < y + h:
        if click[0] == 1 and action is not None:
            action()  # Execute the given action when clicked


def start_screen():
    """
    Display the start screen where players select the number of ships.
    """
    global num_ships
    while num_ships == 0:  # Loop until a number of ships is selected
        screen.fill(WHITE)  # Clear the screen using white background
        text = font.render("Select number of ships to play with:", True, BLACK)
        screen.blit(text, (250, 200))

        # Create buttons for ship selection (1 to 5 ships)
        for i in range(1, 6):
            # Lambda function to set num_ships when a button is clicked
            draw_button(str(i), 150 + 100 * i, 250, 80, 50, LIGHT_GRAY,
                        lambda i=i: setattr(sys.modules[__name__], 'num_ships', i))

        # Handle quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()  # Update the display


finished = False  # Global flag to indicate when a screen is finished


def placement_screen(player):
    """
    Display the ship placement screen for a player.

    Args:
    player (int): The player number (1 or 2)
    """
    global player1_ships, player2_ships, finished
    grid = [[None] * 10 for _ in range(10)]  # Initialize empty grid for ship placement
    # Create ship rectangles for each size
    ships = [pygame.Rect(600, 100 + i * 60, (i + 1) * 50, 50) for i in range(num_ships)]
    selected = None  # Currently selected ship
    vertical = False  # Ship orientation (horizontal by default)
    finished = False  # Reset finished flag

    def clear_ship(ship_num):
        """Remove a ship from the grid."""
        for y in range(10):
            for x in range(10):
                if grid[y][x] == ship_num:
                    grid[y][x] = None

    def is_valid_placement(x, y, size, is_vertical, ship_num):
        """Check if a ship placement is valid."""
        # Check if ship is within grid bounds
        if is_vertical and y + size > 10:
            return False
        if not is_vertical and x + size > 10:
            return False

        # Check for overlap with other ships
        for i in range(size):
            check_x = x + (0 if is_vertical else i)
            check_y = y + (i if is_vertical else 0)

            if grid[check_y][check_x] is not None and grid[check_y][check_x] != ship_num:
                return False

        return True

    while not finished:
        screen.fill(WHITE)  # Clear screen
        # Display player instruction
        text = font.render(f"Player {player} Ship Placement", True, BLACK)
        screen.blit(text, (350, 20))

        # Draw the placement grid
        for i in range(10):
            for j in range(10):
                pygame.draw.rect(screen, GRID_BLUE, (50 + i * 50, 100 + j * 50, 50, 50))
                pygame.draw.rect(screen, BLACK, (50 + i * 50, 100 + j * 50, 50, 50), 1)
                if grid[j][i] is not None:
                    pygame.draw.rect(screen, DARK_GRAY, (50 + i * 50, 100 + j * 50, 50, 50))
                # Draw grid labels (A-J, 1-10)
                screen.blit(font.render(chr(65 + i), True, BLACK), (65 + i * 50, 70))
                screen.blit(font.render(str(j + 1), True, BLACK), (20, 115 + j * 50))

        # Draw the ships
        for ship in ships:
            pygame.draw.rect(screen, DARK_GRAY, ship)
            if ships.index(ship) == selected:
                pygame.draw.rect(screen, RED, ship, 2)  # Highlight selected ship

        # Draw rotate and finish buttons
        rotate_text = "Rotate (V)" if vertical else "Rotate (H)"
        draw_button(rotate_text, 600, 600, 150, 50, LIGHT_GRAY, lambda: globals().update(vertical=not vertical))

        all_ships_placed = all(ship.left < 600 for ship in ships)
        draw_button("Finish", 800, 600, 150, 50, LIGHT_GRAY, lambda: globals().update(finished=True),
                    enabled=all_ships_placed)

        # Draw placement indicator
        mouse_pos = pygame.mouse.get_pos()
        if selected is not None:
            size = max(ships[selected].width, ships[selected].height) // 50
            if vertical:
                indicator = pygame.Rect(mouse_pos[0] - 25, mouse_pos[1] - 25, 50, size * 50)
            else:
                indicator = pygame.Rect(mouse_pos[0] - 25, mouse_pos[1] - 25, size * 50, 50)
            pygame.draw.rect(screen, RED, indicator, 2)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    vertical = False
                elif event.key == pygame.K_v:
                    vertical = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 600 <= event.pos[0] <= 750 and 600 <= event.pos[1] <= 650:
                    vertical = not vertical  # Rotate button clicked
                elif 800 <= event.pos[0] <= 950 and 600 <= event.pos[1] <= 650 and all_ships_placed:
                    finished = True  # Finish button clicked
                else:
                    x, y = (event.pos[0] - 50) // 50, (event.pos[1] - 100) // 50
                    if 0 <= x < 10 and 0 <= y < 10:
                        if selected is not None:
                            # Place selected ship
                            size = max(ships[selected].width, ships[selected].height) // 50
                            if is_valid_placement(x, y, size, vertical, selected + 1):
                                clear_ship(selected + 1)
                                for i in range(size):
                                    if vertical:
                                        grid[y + i][x] = selected + 1
                                    else:
                                        grid[y][x + i] = selected + 1
                                ships[selected] = pygame.Rect(50 + x * 50, 100 + y * 50, 50 if vertical else size * 50,
                                                              size * 50 if vertical else 50)
                                selected = None
                        else:
                            # Select a ship
                            for i, ship in enumerate(ships):
                                if ship.collidepoint(event.pos):
                                    selected = i
                                    clear_ship(i + 1)
                                    break
                    else:
                        # Select a ship from the side panel
                        for i, ship in enumerate(ships):
                            if ship.collidepoint(event.pos):
                                selected = i
                                clear_ship(i + 1)
                                break

        pygame.display.flip()  # Update the display

    # Store the placed ships for each player
    if player == 1:
        player1_ships = [
            {'coords': set((y, x) for y in range(10) for x in range(10) if grid[y][x] == i + 1), 'size': i + 1} for i in
            range(num_ships)]
    else:
        player2_ships = [
            {'coords': set((y, x) for y in range(10) for x in range(10) if grid[y][x] == i + 1), 'size': i + 1} for i in
            range(num_ships)]


def pass_screen(player):
    """
    Display a screen to pass control to the next player.

    Args:
    player (int): The player number to pass control to
    """
    global finished
    finished = False
    while not finished:
        screen.fill(WHITE)  # Clear screen
        # Display pass instruction
        text = font.render(f"Pass to player {player}", True, BLACK)
        screen.blit(text, (350, 20))
        # Draw finish button
        draw_button("Finish", 400, 600, 150, 50, LIGHT_GRAY, lambda: globals().update(finished=True))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 400 <= event.pos[0] <= 550 and 600 <= event.pos[1] <= 650:
                    finished = True  # Finish button clicked
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()  # Update the display


def battle_screen(player, opponent_ships, hits_grid, player_ships):
    """
    Display the battle screen where players make attacks.

    Args:
    player (int): The current player
    opponent_ships (list): List of opponent's ships
    hits_grid (list): Grid to track hits and misses
    player_ships (list): List of current player's ships

    Returns:
    int: 0 if no winner, or the winning player number
    """
    global finished, player1_sunk_ships, player2_sunk_ships, player1_hits, player2_hits
    finished = False
    shot_result = None  # Stores the result of the latest attack
    attack_made = False  # Flag to track if an attack has been made this turn
    # Determine which player's sunk ships to update
    player_sunk_ships = player1_sunk_ships if player == 1 else player2_sunk_ships
    opponent_sunk_ships = player2_sunk_ships if player == 1 else player1_sunk_ships
    opponent_hits = player2_hits if player == 1 else player1_hits

    def get_ship(x, y):
        """Find the ship at the given coordinates."""
        for ship in opponent_ships:
            if (y, x) in ship['coords']:
                return ship
        return None

    def check_ship_sunk(ship):
        """Check if all coordinates of a ship have been hit."""
        return all(hits_grid[y][x] == 'H' for y, x in ship['coords'])

    while not finished:
        screen.fill(WHITE)  # Clear screen
        # Display player instruction
        text = font.render(f"Player {player}: Select a cell to attack", True, BLACK)
        screen.blit(text, (300, 20))

        # Draw opponent's grid (for attacks)
        for i in range(10):
            for j in range(10):
                pygame.draw.rect(screen, GRID_BLUE, (50 + i * 50, 100 + j * 50, 50, 50))
                pygame.draw.rect(screen, BLACK, (50 + i * 50, 100 + j * 50, 50, 50), 1)
                screen.blit(font.render(chr(65 + i), True, BLACK), (65 + i * 50, 70))
                screen.blit(font.render(str(j + 1), True, BLACK), (20, 115 + j * 50))

                # Draw hit and miss markers
                if hits_grid[j][i] == 'M':
                    pygame.draw.circle(screen, WHITE, (75 + i * 50, 125 + j * 50), 20, 2)
                elif hits_grid[j][i] == 'H':
                    ship = get_ship(i, j)
                    if ship and ship['coords'] in opponent_sunk_ships:
                        pygame.draw.rect(screen, RED, (50 + i * 50, 100 + j * 50, 50, 50))
                    else:
                        pygame.draw.line(screen, RED, (60 + i * 50, 110 + j * 50), (90 + i * 50, 140 + j * 50), 3)
                        pygame.draw.line(screen, RED, (90 + i * 50, 110 + j * 50), (60 + i * 50, 140 + j * 50), 3)

        # Draw player's own grid
        your_grid_text = font.render("Your Grid", True, BLACK)
        screen.blit(your_grid_text, (600, 70))
        for i in range(10):
            for j in range(10):
                pygame.draw.rect(screen, LIGHT_BLUE, (600 + i * 30, 130 + j * 30, 30, 30))
                pygame.draw.rect(screen, BLACK, (600 + i * 30, 130 + j * 30, 30, 30), 1)
                screen.blit(font.render(chr(65 + i), True, BLACK), (610 + i * 30, 100))
                screen.blit(font.render(str(j + 1), True, BLACK), (570, 135 + j * 30))

                # Draw player's ships and hit markers
                if any((j, i) in ship['coords'] for ship in player_ships):
                    pygame.draw.rect(screen, DARK_GRAY, (600 + i * 30, 130 + j * 30, 30, 30))
                if (j, i) in [(y, x) for ship in player_sunk_ships for y, x in ship]:
                    pygame.draw.rect(screen, RED, (600 + i * 30, 130 + j * 30, 30, 30))
                elif opponent_hits[j][i] == 'H':
                    pygame.draw.line(screen, RED, (605 + i * 30, 135 + j * 30), (625 + i * 30, 155 + j * 30), 2)
                    pygame.draw.line(screen, RED, (625 + i * 30, 135 + j * 30), (605 + i * 30, 155 + j * 30), 2)
                elif opponent_hits[j][i] == 'M':
                    pygame.draw.circle(screen, WHITE, (615 + i * 30, 145 + j * 30), 10, 2)

        if shot_result:
            result_text = font.render(shot_result, True, BLACK)
            screen.blit(result_text, (400, 650))

        # Draw finish turn button
        draw_button("Finish Turn", 800, 600, 150, 50, LIGHT_GRAY, lambda: globals().update(finished=True),
                    enabled=attack_made)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not attack_made:
                x, y = (event.pos[0] - 50) // 50, (event.pos[1] - 100) // 50
                if 0 <= x < 10 and 0 <= y < 10:
                    if hits_grid[y][x] is None:
                        ship = get_ship(x, y)
                        if ship:
                            hits_grid[y][x] = 'H'  # Mark as hit
                            if check_ship_sunk(ship):
                                opponent_sunk_ships.append(ship['coords'])
                                shot_result = "Sink!"
                            else:
                                shot_result = "Hit!"
                        else:
                            hits_grid[y][x] = 'M'  # Mark as miss
                            shot_result = "Miss!"
                        attack_made = True
                    else:
                        shot_result = "Already Attacked!"

        pygame.display.flip()  # Update the display

    # Update sunk ships for the correct player
    if player == 1:
        player2_sunk_ships = opponent_sunk_ships
    else:
        player1_sunk_ships = opponent_sunk_ships

    def all_ships_sunk(player_ships):
        """Check if all ships of a player have been sunk."""
        return all(check_ship_sunk(ship) for ship in player_ships)

    # Check for a winner
    if all_ships_sunk(opponent_ships):
        finished = True
        winner = player
        return winner
    else:
        return 0


def winner_screen(player):
    """
    Display the winner screen and options for a new game or to end the game.

    Args:
    player (int): The winning player number
    """
    global game_running, restart_game
    screen.fill(WHITE)  # Clear screen
    # Display winner text
    text = font.render(f"Player {player} Wins!", True, BLACK)
    screen.blit(text, (350, 200))

    def new_game():
        global restart_game
        restart_game = True

    def end_game():
        global game_running
        game_running = False

    # Draw new game and end game buttons
    draw_button("New Game", 300, 400, 150, 50, LIGHT_GRAY, action=new_game)
    draw_button("End Game", 500, 400, 150, 50, LIGHT_GRAY, action=end_game)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 300 <= mouse_pos[0] <= 450 and 400 <= mouse_pos[1] <= 450:
                    new_game()
                    return
                elif 500 <= mouse_pos[0] <= 650 and 400 <= mouse_pos[1] <= 450:
                    end_game()
                    return

        pygame.display.flip()  # Update the display


def main():
    """
    Main game loop that controls the flow of the game.
    """
    global num_ships, player1_ships, player2_ships, player1_sunk_ships, player2_sunk_ships
    global game_running, restart_game, player1_hits, player2_hits

    game_running = True
    restart_game = False

    while game_running:
        if restart_game:
            # Reset all game variables for a new game
            num_ships = 0
            player1_ships = None
            player2_ships = None
            player1_sunk_ships = []
            player2_sunk_ships = []
            player1_hits = None
            player2_hits = None
            restart_game = False
            continue

        # Start screen to select number of ships
        start_screen()
        # Initialize hit grids for both players
        player1_hits = [[None] * 10 for _ in range(10)]
        player2_hits = [[None] * 10 for _ in range(10)]

        # Ship placement for both players
        placement_screen(1)
        pass_screen(2)

        placement_screen(2)
        pass_screen(1)

        # Main game loop
        winner = 0
        while winner == 0:
            # Player 1's turn
            winner = battle_screen(1, player2_ships, player1_hits, player1_ships)
            if winner:
                break
            pass_screen(2)

            # Player 2's turn
            winner = battle_screen(2, player1_ships, player2_hits, player2_ships)
            if winner:
                break
            pass_screen(1)

        # Display winner and handle game end or restart
        winner_screen(winner)

        if not game_running:
            break


if __name__ == "__main__":
    main()