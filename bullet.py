import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage global bullet attributes."""

    def __init__(self, ai_game):
        """Create a bullet object with default parameters."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
    
    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)

class ShipBullet(Bullet):
    """A class to manage bullets fired from the player ship"""

    def __init__(self, ai_game):
        """Create the bullet at the ship's position"""

        super().__init__(ai_game)

        self.color = self.settings.ship_bullet_color

        # Sets the bullet's position to align with the top of the player ship
        self.rect = pygame.Rect(0, 0, self.settings.ship_bullet_width, self.settings.ship_bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Store the bullet's position as a float.
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet up the screen."""
        
        # Update the exact position of the bullet.
        self.y -= self.settings.bullet_speed
        
        # Update the rect position.
        self.rect.y = self.y

class AlienBullet(Bullet):
    """A class to manage bullets fired from the alien ships"""

    def __init__(self, ai_game, alien):
        """Create the bullet at the alien's position"""

        super().__init__(ai_game)

        self.color = self.settings.alien_bullet_color

        # Sets the bullet's position to align with the bottom of the alien ship
        self.rect = pygame.Rect(0, 0, self.settings.alien_bullet_width, self.settings.alien_bullet_height)
        self.rect.midbottom = alien.rect.midbottom

        # Store the bullet's position as a float.
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet up the screen."""
        
        # Update the exact position of the bullet.
        self.y += self.settings.alien_bullet_speed
        
        # Update the rect position.
        self.rect.y = self.y