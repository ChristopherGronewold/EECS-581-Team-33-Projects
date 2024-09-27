import pygame
import sys
from player import Player
from button import Button

class WinScreen:
    def __init__(self, players, screen, font, colors, gameParams):
        self.player1 = players[0]
        self.player2 = players[1]
        self.screen = screen
        self.font = font
        self.colors = colors
        self.gameParams = gameParams
    
    def new_game():
        global restart_game
        restart_game = True

    def end_game():
        global game_running
        game_running = False

    def winner_screen(self, player):
        """
        Display the winner screen and options for a new game or to end the game.

        Args:
        player (int): The winning player number
        """
        global game_running, restart_game
        self.screen.fill(self.colors["WHITE"])  # Clear screen
        # Display winner text
        text = self.font.render(f"Player {player} Wins!", True, self.colors["BLACK"])
        self.screen.blit(text, (350, 200))

    # Draw new game and end game buttons
        newGameButton = Button("New Game", 300, 400, 150, 50, self.colors["LIGHT_GRAY"], action=new_game)
        endGameButton = Button("End Game", 500, 400, 150, 50, self.colors["LIGHT_GRAY"], action=end_game)

        newGameButton.draw(self.screen, self.font)
        endGameButton.draw(self.screen, self.font)

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