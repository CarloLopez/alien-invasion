import pygame
from pygame.sprite import Sprite
from random import randint

class Powerup(Sprite):
    """A class to manage powerups"""

    def __init__(self, ai_game):
        """Initialise global attributes"""
        super().__init__()

        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.sb = ai_game.sb
    
    def _randomise_location(self):
        """randomise starting location of the powerup on its x-axis"""

        self.rect.y = -self.rect.height
        x_position = randint(1, self.settings.screen_width)
        self.rect.x = x_position
        
        self.y = float(self.rect.y)
    
    def update(self):
        """Move the powerup down the screen."""
        
        # Update the exact position of the powerup.
        self.y += self.settings.powerup_drop_speed
        
        # Update the rect position.
        self.rect.y = self.y

class BulletExpansion(Powerup):
    """A class for powerup that increases max bullets to shoot"""
    
    def __init__(self, ai_game):
        """Initialise bullet expansion attributes"""
        super().__init__(ai_game)

        self.image = pygame.image.load("images/gun-powerup.bmp")
        self.image = pygame.transform.scale(self.image, (35, 35))
        self.rect = self.image.get_rect()

        self._randomise_location()
    
    def _grant_powerup(self):
        self.settings.ship_bullet_width += 1
        self.settings.ship_bullet_height += 0.25
        self.settings.bullets_allowed += 1
        self.settings.bullet_speed += 0.25
        sfx = pygame.mixer.Sound("music/gun_powerup.wav")
        pygame.mixer.Sound.play(sfx)

class HealthUp(Powerup):
    """A class for powerup that restores ship lives, if below max"""
    
    def __init__(self, ai_game):
        """Initialise health restoration attributes"""
        super().__init__(ai_game)

        self.image = pygame.image.load("images/health-powerup.bmp")
        self.image = pygame.transform.scale(self.image, (35, 35))
        self.rect = self.image.get_rect()

        self._randomise_location()
    
    def _grant_powerup(self):
        if self.stats.ships_left < self.settings.ship_limit:
            self.stats.ships_left += 1
            self.sb.prep_ships()
            sfx = pygame.mixer.Sound("music/health_up.wav")
        else:
            sfx = pygame.mixer.Sound("music/health_up_false.wav")
        pygame.mixer.Sound.play(sfx)


class SpeedUp(Powerup):
    """A class for powerup that increases ship movement speed"""
    
    def __init__(self, ai_game):
        """Initialise speed powerup attributes"""
        super().__init__(ai_game)

        self.image = pygame.image.load("images/speed-powerup.bmp")
        self.image = pygame.transform.scale(self.image, (35, 35))
        self.rect = self.image.get_rect()

        self._randomise_location()
    
    def _grant_powerup(self):
        self.settings.ship_speed += 0.25
        sfx = pygame.mixer.Sound("music/speed_up.wav")
        pygame.mixer.Sound.play(sfx)