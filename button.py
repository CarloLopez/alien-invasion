import pygame.font

class Button:
    """A class to build buttons for the game."""

    def __init__(self, ai_game, msg):
        """Initialise button attributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button.
        self.width, self.height = 200, 50
        self.font = pygame.font.SysFont(None, 35)

        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Draw blank button and then draw message."""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

class NormalButton(Button):
    """Button to play in normal mode."""

    def __init__(self, ai_game, msg):

        super().__init__(ai_game, msg)

        # Set the dimensions and properties of the button.
        self.button_color = (18, 18, 18)
        self.text_color = (255, 255, 255)

        # Align y-axis
        self.rect.y -= 50 

        self._prep_msg(msg)

class HardModeButton(Button):
    """Button to play in hard mode."""

    def __init__(self, ai_game, msg):

        super().__init__(ai_game, msg)

        # Set the dimensions and properties of the button.
        self.button_color = (18, 18, 18)
        self.text_color = (255, 255, 255)

        # Align y-axis
        self.rect.y += 50 

        self._prep_msg(msg)