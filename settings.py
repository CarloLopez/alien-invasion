class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self):
        """Initialise the game's settings."""

        # Screen settings
        self.fullscreen = False
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (46, 23, 82)

        # Ship settings
        self.ship_speed = 1.5