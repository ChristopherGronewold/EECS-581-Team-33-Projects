import pygame

class Button:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font

    def draw(self, text, x, y, w, h, color, action=None, enabled=True):
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
            pygame.draw.rect(self.screen, color, (x, y, w, h))
        else:
            pygame.draw.rect(self.screen, DARK_GRAY, (x, y, w, h))  # Use dark gray for disabled buttons

        #Render the button text
        text_surf = self.font.render(text, True, BLACK)
        # Calculate position to center the text on the button
        text_pos = (x + w // 2 - text_surf.get_width() // 2, y + h // 2 - text_surf.get_height() // 2)
        self.screen.blit(text_surf, text_pos)

        # Check if the mouse is over the button and it's clicked
        if enabled and x < mouse[0] < x + w and y < mouse[1] < y + h:
            if click[0] == 1 and action is not None:
                action()  # Execute the given action when clicked