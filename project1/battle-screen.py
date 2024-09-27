from player import Player

import pygame

class BattleScreen:
    
    #global finished, player1_sunk_ships, player2_sunk_ships, player1_hits, player2_hits

    
    # Determine which player's sunk ships to update
    #player_sunk_ships = player1_sunk_ships if player == 1 else player2_sunk_ships
    #opponent_sunk_ships = player2_sunk_ships if player == 1 else player1_sunk_ships
    #opponent_hits = player2_hits if player == 1 else player1_hits
    
    def _init_(self, players, screen):
        self.screen = screen
        self.player1 = players[0]
        self.player2 = players[1]
        self.finished = False
        self.shot_result = None  # Stores the result of the latest attack
        self.attack_made = False  # Flag to track if an attack has been made this turn
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
    

    def get_ship(opponent, x, y):
        """Find the ship at the given coordinates."""
        for ship in opponent.ships:
            if (y, x) in ship['coords']:
                return ship
        return None

    def check_ship_sunk(self, ship):
        """Check if all coordinates of a ship have been hit."""
        return all(hits_grid[y][x] == 'H' for y, x in ship['coords'])


    def display(self, player, opponent, hits_grid, player_ships):
        while not finished:
            self.screen.fill(WHITE)  # Clear screen
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