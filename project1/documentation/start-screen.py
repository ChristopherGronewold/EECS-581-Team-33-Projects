from player import Player

class StartScreen:
    def __init__(self, players, screen, font):
        self.player1 = players[0]
        self.player2 = players[1]
        self.num_ships = 0
    
    def display(self, screen, font):
        """
        Display the start screen where players select the number of ships.
        """
        while self.num_ships == 0:  # Loop until a number of ships is selected
            self.screen.fill(WHITE)  # Clear the screen using white background
            text = self.font.render("Select number of ships to play with:", True, BLACK)
            self.screen.blit(text, (250, 200))

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