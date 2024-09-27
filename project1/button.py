import pygame

class Button:
    def __init__(self, colors, gameParams, x, y, width, height, buttonColor, text):
        self.colors = colors #Color dictionary
        self.screen = gameParams["screen"]#Pull the screen info from the gameParams dictionary
        self.font = gameParams["font"]#Pull the font info from the gameParams dictionary
        self.color = buttonColor #The specified button color is called at object creation, this makes it easier to create buttons

        #X and Y coordinates of the button
        self.x = x
        self.y = y
        #Width and Height of the button
        self.width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height) #Create a rectangle on the screen:
                                                    #at coordinates: X and Y
                                                    #dimensions: width and height

        self.action = None
        self.text = text

    def draw(self, x, y, w, h, action=None, enabled=True):
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
            pygame.draw.rect(self.screen, self.buttonColor, (x, y, w, h))
        else:
            pygame.draw.rect(self.screen, self.colors["DARK_GRAY"], (x, y, w, h))  # Use dark gray for disabled buttons

        #Render the button text
        text_surf = self.font.render(self.text, True, self.colors["BLACK"])
        # Calculate position to center the text on the button
        text_pos = (x + w // 2 - text_surf.get_width() // 2, y + h // 2 - text_surf.get_height() // 2)
        self.screen.blit(text_surf, text_pos)

        # Check if the mouse is over the button and it's clicked
        if enabled and x < mouse[0] < x + w and y < mouse[1] < y + h:
            if click[0] == 1 and action is not None:
                action()  # Execute the given action when clicked

    def click(self, mouse_pos):
        return self.rect.collidepoint