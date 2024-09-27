from button import Button
import pygame
import sys

class PassScreen:
    def __init__(self, player, screen, font, colors):
        self.colors = colors # Dictionary of colors
        self.nextPlayer = player # Player to pass control to
        self.screen = screen # Game screen
        self.font = font    # Font for text

    def display(self, player):
        """
        Display a screen to pass control to the next player.

        Args:
        player (int): The player number to pass control to
        """
        finished = False
        while not finished:
            button = Button(self.screen, self.font)

            self.screen.fill(self.colors["WHITE"])  # Clear screen
            # Display pass instruction
            text = self.font.render(f"Pass to player {player}", True, BLACK)
            self.screen.blit(text, (350, 20))
            # Draw finish button
            button.draw("Finish", 400, 600, 150, 50, LIGHT_GRAY, lambda: globals().update(finished=True))

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 400 <= event.pos[0] <= 550 and 600 <= event.pos[1] <= 650:
                        finished = True  # Finish button clicked
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()  # Update the display
        