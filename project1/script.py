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
from player import Player

# Initialize Pygame and set up the display
pygame.init()
screen = pygame.display.set_mode((1000, 750))  # Create a 1000x750 pixel window
font = pygame.font.Font(None, 36)  # Set up a default font for text rendering

# Game Parameters
gameParams = {
    "finished": False,
    "num_ships": 0,
    "player1" : Player(1),
    "player2" : Player(2),
}




# Define color constants for easy reference throughout the game
colorDict = {
    "WHITE" : (255, 255, 255),
    "BLACK" : (0, 0, 0),
    "LIGHT_GRAY" : (200, 200, 200),
    "DARK_GRAY" : (150, 150, 150),
    "LIGHT_BLUE" : (100, 100, 255),
    "RED" : (255, 0, 0),
    "GRID_BLUE" : (10, 150, 210),
}

#Initializing Player information

# Global variables to store game state
num_ships = 0  # Number of ships each player will have
#player1_ships = None  # Stores Player 1's ship placements
#player2_ships = None  # Stores Player 2's ship placements

# Grids to track attacks for each player (10x10 grid)
#player1_attack_grid = [[None for _ in range(10)] for _ in range(10)]
#player2_attack_grid = [[None for _ in range(10)] for _ in range(10)]

# Variables to store hit information for each player
#player1_hits = None  # Will be initialized as a 10x10 grid
#player2_hits = None  # Will be initialized as a 10x10 grid

# Lists to store sunk ships for each player

#finished = False  # Global flag to indicate when a screen is finished

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