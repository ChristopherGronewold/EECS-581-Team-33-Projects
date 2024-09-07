import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((1000, 750))
font = pygame.font.Font(None, 36)

# Define color variables
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)  # for grayed out buttons and ships
LIGHT_BLUE = (100, 100, 255)
RED = (255, 0, 0)  # for outlining ships
GRID_BLUE = (10, 150, 210)  # for grid background

# Global variables to store game state
num_ships = 0
player1_ships = None
player2_ships = None

def draw_button(text, x, y, w, h, color, action=None, enabled=True):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Draw the button in dark gray if it's disabled
    if enabled:
        pygame.draw.rect(screen, color, (x, y, w, h))
    else:
        pygame.draw.rect(screen, DARK_GRAY, (x, y, w, h))

    text_surf = font.render(text, True, BLACK)
    screen.blit(text_surf, (x + w // 2 - text_surf.get_width() // 2, y + h // 2 - text_surf.get_height() // 2))

    # Check if the button is clicked and execute the associated action
    if enabled and x < mouse[0] < x + w and y < mouse[1] < y + h:
        if click[0] == 1 and action is not None:
            action()

def start_screen():
    global num_ships
    while num_ships == 0:
        screen.fill(WHITE)
        text = font.render("Select number of ships to play with:", True, BLACK)
        screen.blit(text, (250, 200))

        # Draw buttons for selecting the number of ships (1 to 5)
        for i in range(1, 6):
            draw_button(str(i), 150 + 100 * i, 250, 80, 50, LIGHT_GRAY,
                        lambda i=i: setattr(sys.modules[__name__], 'num_ships', i))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()

def placement_screen(player):
    global player1_ships, player2_ships
    grid = [[0] * 10 for _ in range(10)]
    # Create ship rectangles of different sizes based on the number of ships
    ships = [pygame.Rect(600, 100 + i * 60, (i + 1) * 50, 50) for i in range(num_ships)]
    selected = None
    vertical = False
    finished = False

    def clear_ship(ship_num):
        # Remove a ship from the grid
        for y in range(10):
            for x in range(10):
                if grid[y][x] == ship_num:
                    grid[y][x] = 0

    def is_valid_placement(x, y, size, is_vertical, ship_num):
        # Check if a ship can be placed at the given position
        if is_vertical:
            if y + size > 10:
                return False
            return all(grid[y+i][x] == 0 or grid[y+i][x] == ship_num for i in range(size))
        else:
            if x + size > 10:
                return False
            return all(grid[y][x+i] == 0 or grid[y][x+i] == ship_num for i in range(size))

    while not finished:
        screen.fill(WHITE)
        text = font.render(f"Player {player} Ship Placement", True, BLACK)
        screen.blit(text, (350, 20))

        # Draw the grid and label it with letters and numbers
        for i in range(10):
            for j in range(10):
                pygame.draw.rect(screen, GRID_BLUE, (50 + i * 50, 100 + j * 50, 50, 50))
                pygame.draw.rect(screen, BLACK, (50 + i * 50, 100 + j * 50, 50, 50), 1)
                if grid[j][i] != 0:
                    pygame.draw.rect(screen, DARK_GRAY, (50 + i * 50, 100 + j * 50, 50, 50))
                screen.blit(font.render(chr(65 + i), True, BLACK), (65 + i * 50, 70))
                screen.blit(font.render(str(j + 1), True, BLACK), (20, 115 + j * 50))

        # Draw the ships in the sidebar
        for ship in ships:
            pygame.draw.rect(screen, DARK_GRAY, ship)
            if ships.index(ship) == selected:
                pygame.draw.rect(screen, RED, ship, 2)

        # Draw rotate and finish buttons
        rotate_text = "Rotate (V)" if vertical else "Rotate (H)"
        draw_button(rotate_text, 600, 600, 150, 50, LIGHT_GRAY, lambda: globals().update(vertical=not vertical))

        all_ships_placed = all(ship.left < 600 for ship in ships)
        draw_button("Finish", 800, 600, 150, 50, LIGHT_GRAY, lambda: globals().update(finished=True),
                    enabled=all_ships_placed)

        # Draw a red outline to show where the selected ship will be placed
        mouse_pos = pygame.mouse.get_pos()
        if selected is not None:
            size = max(ships[selected].width, ships[selected].height)
            if vertical:
                indicator = pygame.Rect(mouse_pos[0] - 25, mouse_pos[1] - 25, 50, size)
            else:
                indicator = pygame.Rect(mouse_pos[0] - 25, mouse_pos[1] - 25, size, 50)
            pygame.draw.rect(screen, RED, indicator, 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 600 <= event.pos[0] <= 750 and 600 <= event.pos[1] <= 650:
                    vertical = not vertical
                elif 800 <= event.pos[0] <= 950 and 600 <= event.pos[1] <= 650 and all_ships_placed:
                    finished = True
                else:
                    x, y = (event.pos[0] - 50) // 50, (event.pos[1] - 100) // 50
                    if 0 <= x < 10 and 0 <= y < 10:
                        if selected is not None:
                            size = max(ships[selected].width, ships[selected].height) // 50
                            if is_valid_placement(x, y, size, vertical, selected + 1):
                                # Place the ship on the grid
                                clear_ship(selected + 1)
                                if vertical:
                                    ships[selected] = pygame.Rect(50 + x * 50, 100 + y * 50, 50, size * 50)
                                else:
                                    ships[selected] = pygame.Rect(50 + x * 50, 100 + y * 50, size * 50, 50)
                                for i in range(size):
                                    if vertical:
                                        grid[y+i][x] = selected + 1
                                    else:
                                        grid[y][x+i] = selected + 1
                            selected = None
                        else:
                            # Select a ship that's already on the grid
                            for i, ship in enumerate(ships):
                                if ship.collidepoint(event.pos):
                                    selected = i
                                    break
                    else:
                        # Select a ship from the sidebar or pick up a placed ship
                        for i, ship in enumerate(ships):
                            if ship.collidepoint(event.pos):
                                if ship.left < 600:  # If ship is on the grid
                                    selected = i
                                else:  # If ship is in the sidebar
                                    selected = i
                                    clear_ship(i + 1)
                                break

        pygame.display.flip()

    # Store the completed ship placement for each player
    if player == 1:
        player1_ships = grid
    else:
        player2_ships = grid

# Main game flow
start_screen()
placement_screen(1)
placement_screen(2)

print("Player 1 ships:", player1_ships)
print("Player 2 ships:", player2_ships)
