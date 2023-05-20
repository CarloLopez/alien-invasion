class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self):
        """Initialise the game's static settings."""

        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (20, 20, 20)

        # Difficulty flag
        self.hardmode_on = False

        # Bullet settings
        self.ship_bullet_color = (245, 99, 66)
        self.alien_bullet_color = (137, 222, 120)
        self.alien_bullet_width = 8
        self.alien_bullet_height = 10

        # Alien settings
        self.fleet_drop_speed = 10

        # Powerup settings
        self.powerup_drop_speed = 2.5
        
        self.initialise_difficulty_settings()
        self.initialise_dynamic_settings()

    def initialise_difficulty_settings(self):
        """Set base settings depending on difficulty flag"""

        if self.hardmode_on == False:
            # Ship lives remaining
            self.ship_limit = 3
            # Speed of alien bullets
            self.alien_bullet_speed = 2.5
            # How quickly the alien ships speed up after each wave
            self.speedup_scale = 1.1
            # How quickly the alien point values increase
            self.score_scale = 1.5
            # Multiplier to determine maximum alien bullets raining down
            self.max_alien_bullet_factor = 8
            # Interval timer for frequency of aliens shooting bullets at player (ms)
            self.alien_bullet_interval = 2500
        else:
            self.ship_limit = 1
            self.alien_bullet_speed = 5
            self.speedup_scale = 1.25
            self.score_scale = 2
            self.max_alien_bullet_factor = 4
            self.alien_bullet_interval = 1250

    def initialise_dynamic_settings(self):
        """Initialise settings that change throughout the game"""
        self.ship_speed = 5
        self.alien_speed = 1.5

        # Dynamic bullet settings
        self.bullet_speed = 5
        self.ship_bullet_width = 4
        self.ship_bullet_height = 12
        self.bullets_allowed = 3

        # fleet direction of 1 represents right; -1 represents left
        self.fleet_direction = 1

        # Scoring settings
        self.alien_points = 50
    
    def increase_difficulty(self):
        """Increase alien speed settings, bullet frequency and alien point values."""
        self.alien_speed *= self.speedup_scale
        self.alien_bullet_interval /= self.speedup_scale
        
        self.alien_points = int(self.alien_points * self.score_scale)