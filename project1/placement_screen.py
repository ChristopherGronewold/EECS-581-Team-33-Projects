import pygame
import sys
from player import Player
from button import Button

class PlacementScreen:
    def __init__(self, colors, gameParams):
        self.colors = colors
        self.gameParams = gameParams

    def display(self, player):
        """
        Display the ship placement screen for a player.

        Args:
        player (int): The player number (1 or 2)
        """
        #global player1_ships, player2_ships, finished
        grid = [[None] * 10 for _ in range(10)]  # Initialize empty grid for ship placement
        # Create ship rectangles for each size
        ships = [pygame.Rect(600, 100 + i * 60, (i + 1) * 50, 50) for i in range(self.gameParams["num_ships"])]
        selected = None  # Currently selected ship
        vertical = False  # Ship orientation (horizontal by default)
        finished = False  # Reset finished flag
        while not finished:
            self.gameParams["screen"].fill(self.colors["WHITE"])  # Clear screen
            # Display player instruction
            text = self.gameParams["font"].render(f"Player {player} Ship Placement", True, self.colors["BLACK"])
            self.gameParams["screen"].blit(text, (350, 20))

            # Draw the placement grid
            for i in range(10):
                for j in range(10):
                    pygame.draw.rect(self.gameParams["screen"], self.colors["GRID_BLUE"], (50 + i * 50, 100 + j * 50, 50, 50))
                    pygame.draw.rect(self.gameParams["screen"], self.colors["BLACK"], (50 + i * 50, 100 + j * 50, 50, 50), 1)
                    if grid[j][i] is not None:
                        pygame.draw.rect(self.gameParams["screen"], self.colors["DARK_GRAY"], (50 + i * 50, 100 + j * 50, 50, 50))
                    # Draw grid labels (A-J, 1-10)
                    self.gameParams["screen"].blit(self.gameParams["font"].render(chr(65 + i), True, self.colors["BLACK"]), (65 + i * 50, 70))
                    self.gameParams["screen"].blit(self.gameParams["font"].render(str(j + 1), True, self.colors["BLACK"]), (20, 115 + j * 50))

        # Draw the ships
            for ship in ships:
                pygame.draw.rect(self.gameParams["screen"], self.colors["DARK_GRAY"], ship)
                if ships.index(ship) == selected:
                    pygame.draw.rect(self.gameParams["screen"], self.colors["RED"], ship, 2)  # Highlight selected ship


        # Create Rotate/Finish buttons
            rotateButton = Button("Rotate (V)" if vertical else "Rotate (H)",
                                   600, 600, 150, 50,
                                   self.colors["LIGHT_GRAY"], 
                                   lambda: locals().update(vertical=not vertical))
            finishButton = Button("Finish",
                                   800, 600, 150, 50, 
                                   self.colors["LIGHT_GRAY"], 
                                   lambda: locals().update(finished=True),
                                   enabled=all_ships_placed)
        # Draw rotate and finish buttons
            rotateButton.draw()
            finishButton.draw()
        #Enable 'Finish' button when all ships are placed
            all_ships_placed = all(ship.left < 600 for ship in ships)
            # Draw placement indicator
            mouse_pos = pygame.mouse.get_pos()
            if selected is not None:
                size = max(ships[selected].width, ships[selected].height) // 50
                if vertical:
                    indicator = pygame.Rect(mouse_pos[0] - 25, mouse_pos[1] - 25, 50, size * 50)
                else:
                    indicator = pygame.Rect(mouse_pos[0] - 25, mouse_pos[1] - 25, size * 50, 50)
                pygame.draw.rect(self.gameParams["screen"], self.colors["RED"], indicator, 2)

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

        