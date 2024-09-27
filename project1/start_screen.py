import pygame
import sys

from button import Button
class StartScreen:

    def __init__(self, gameParams, colors):
            self.gameParams = gameParams
            self.colors = colors
        
    def display(self):
        """
        Display the start screen where players select the number of ships.
        """
        
        while self.gameParams["num_ships"] == 0:  # Loop until a number of ships is selected
            self.gameParams["screen"].fill(self.colors["WHITE"])  # Clear the screen using white background
            text = self.gameParams["font"].render("Select number of ships to play with:", True, self.colors["BLACK"])
            self.gameParams["screen"].blit(text, (250, 200))

        # Create buttons for ship selection (1 to 5 ships)
            for i in range(1, 6):
                # Lambda function to set num_ships when a button is clicked
                selectionButton = Button(str(i), 150 + 100 * i, 250, 80, 50, self.colors["LIGHT_GRAY"],
                            lambda i=i: self.gameParams.update({"num_ships" : i}))
                selectionButton.draw()

        # Handle quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()  # Update the display


        # Needs to be moved # finished = False  # Global flag to indicate when a screen is finished