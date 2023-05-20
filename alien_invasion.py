import sys
from time import sleep
from random import randint

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import NormalButton, HardModeButton
from ship import Ship
from bullet import ShipBullet, AlienBullet
from alien import Alien
from powerup import BulletExpansion, HealthUp, SpeedUp

class AlienInvasion:
    """Overall class to manage game assets and behaviour"""

    def __init__(self):
        """Initialise the game, and create game resources"""
        pygame.init()

        self.clock = pygame.time.Clock()
        self.settings = Settings()
        
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        self.bg = self.image = pygame.image.load("images/bg.bmp")

        # Create an instance to store game statistics and scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.alienbullets = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()

        # Start Alien Invasion in an active state.
        self.game_active = False

        # Make the Play buttons.
        self.play_button = NormalButton(self, "Normal Mode")
        self.play_button_hardmode = HardModeButton(self, "Hard Mode")

    def run_game(self):
        """Start the main loop for the game"""

        pygame.mixer.music.load('music/bgm.wav')

        TIMED_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(TIMED_EVENT, self.settings.alien_bullet_interval)

        while True:
            self._check_events(TIMED_EVENT)

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._update_powerups()
            
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self, TIMED_EVENT):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos)
                
                if (self.game_active == True) and (event.type == TIMED_EVENT):
                    self.fire_alien_bullets()
                    self._roll_powerup()

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        normal_button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if normal_button_clicked and not self.game_active:
            self.settings.hardmode_on = False
            self._new_game()
        hardmode_button_clicked = self.play_button_hardmode.rect.collidepoint(mouse_pos)
        if hardmode_button_clicked and not self.game_active:
            self.settings.hardmode_on = True
            self._new_game()
        
    def _new_game(self):
        """Reset the game statistics and speed settings."""
        self.settings.initialise_difficulty_settings()
        self.stats.reset_stats()
        self.sb.prep_score()
        self.sb.prep_high_score()
        self.sb.prep_level()
        self.sb.prep_ships()
        self.settings.initialise_dynamic_settings()

        self.game_active = True
        pygame.mixer.music.play(-1)

        # Get rid of any remaining bullets and aliens.
        self.bullets.empty()
        self.alienbullets.empty()
        self.aliens.empty()

        #Create a new fleet and center the ship.
        self._create_fleet()
        self.ship.center_ship()

        #Hide the mouse cursor.
        pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            if self.game_active:
                self._fire_bullet()
        elif event.key == pygame.K_q:
            self.stats.save_highscore()
            sys.exit()

    def _check_keyup_events(self, event):
        """Respond to keyreleases."""
        if event.key == pygame.K_RIGHT:
           self.ship.moving_right = False 
        elif event.key == pygame.K_LEFT: 
           self.ship.moving_left = False

    def fire_alien_bullets(self):
        """Periodically shoot a bullet from x number of random aliens present on screen."""
        aliens_list = list(self.aliens.sprites())
        aliens_alive = len(aliens_list)
        
        # Choose maximum number of alien shooters per cycle, based on difficulty level
        rand_max = aliens_alive/self.settings.max_alien_bullet_factor
        if rand_max > 1:
            max_shooters = randint(1, int(rand_max))
        else:
            max_shooters = 1
        
        # Generate a random number to index from the aliens list created earlier
        for num in range(max_shooters):
            if aliens_alive > 1:
                shooter = randint(0, aliens_alive - 1)
            else:
                shooter = 0
            
            # Index the specific alien to shoot a bullet from using the number, then create an alien bullet
            specific_alien = aliens_list[shooter]
            new_bullet = AlienBullet(self, specific_alien)
            self.alienbullets.add(new_bullet) 
        
        bulletsound = pygame.mixer.Sound("music/alien_bullet.wav")
        pygame.mixer.Sound.play(bulletsound)
        
    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = ShipBullet(self)
            self.bullets.add(new_bullet)
            bulletsound = pygame.mixer.Sound("music/ship_bullet.wav")
            pygame.mixer.Sound.play(bulletsound)

    def _spawn_powerup(self):
        """Create a random powerup at a random horizonal location at the top of the screen."""

        rand_num = randint(1, 3)

        if rand_num == 1:
            spawned_powerup = BulletExpansion(self)
        elif rand_num == 2:
            spawned_powerup = HealthUp(self)
        else:
            spawned_powerup = SpeedUp(self)
        
        self.powerups.add(spawned_powerup)
    
    def _update_bullets(self):
        """Update the position of bullets to get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()
        self.alienbullets.update()

        # Get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        for bullet in self.alienbullets.copy():
            if bullet.rect.top >= self.settings.screen_height:
                self.alienbullets.remove(bullet)

        self._check_bullet_ship_collisions()
        self._check_bullet_alien_collisions()

    def _update_powerups(self):
        """Update the position of powerups"""
        self.powerups.update()

        # Check for any powerups that have passed the bottom of the screen.
        self._check_powerups_bottom()

        # Look for any collisions with the powerup and the player ship.
        self._check_powerup_ship_collisions()

    def _check_powerup_ship_collisions(self):
        """Respond to any collisions between powerups and the player ship."""

        # Remove powerups that have collided and grant powerup to player
        for powerup in self.powerups:
            if powerup.rect.colliderect(self.ship.rect):
                powerup._grant_powerup()
                self.powerups.remove(powerup)

    def _roll_powerup(self):
        """20% Chance to spawn a powerup when method called"""
        powerup_rand = randint(1, 5)
        if powerup_rand == 5:
            self._spawn_powerup()

    def _check_bullet_alien_collisions(self):
        """Respond to any bullet collisions from the player."""
        
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                
            self.sb.prep_score()
            self.sb.check_high_score()

            deathsound = pygame.mixer.Sound("music/alien_death.wav")
            pygame.mixer.Sound.play(deathsound)

        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_difficulty()

            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()
    
    def _check_bullet_ship_collisions(self):
        """Respond to any collisions from alien bullets."""

        if pygame.sprite.spritecollideany(self.ship, self.alienbullets):
            self._ship_hit()

    def _update_aliens(self):
        """Update the positions of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _cycle_alien_bullets(self, TIMED_EVENT):

        for event in pygame.event.get():
            if event.type == TIMED_EVENT:
                self.fire_alien_bullets()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""

        if self.stats.ships_left > 0:
            # Decrement ships left, and update scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.alienbullets.empty()
            self.aliens.empty()
            self.powerups.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            deathsound = pygame.mixer.Sound("music/ship_death.wav")
            pygame.mixer.Sound.play(deathsound)

            # Pause.
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)
            pygame.mixer.music.stop()

            game_over = pygame.mixer.Sound("music/game_over.wav")
            pygame.mixer.Sound.play(game_over)

            self.stats.save_highscore()
    
    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                #Treat this the same as if the ship got hit.
                self._ship_hit()
                break
    
    def _check_powerups_bottom(self):
        """Check if any powerups have reached the bottom of the screen"""
        for powerup in self.powerups.sprites():
            if powerup.rect.top >= self.settings.screen_height:
                self.powerups.remove(powerup)

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and keep adding aliens until there's no room left.
        # Spacing between aliens is one alien width and one alien height.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, (alien_height + 50)
        while current_y < (self.settings.screen_height - 4 * alien_height):
            while current_x < (self.settings.screen_width - 2* alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            
            #Finished a row; reset x value, and increment y value.
            current_x = alien_width
            current_y += 2 * alien_height
        
        spawn_sfx = pygame.mixer.Sound("music/alien_spawn.wav")
        pygame.mixer.Sound.play(spawn_sfx)

    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the fleet."""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position 
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
           if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _draw_bg(self):
        self.screen.blit(self.bg)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.screen.blit(self.bg, (0, 0))
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for bullet in self.alienbullets.sprites():
            bullet.draw_bullet()
        self.powerups.draw(self.screen)
        self.ship.blitme()
        self.aliens.draw(self.screen)

        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.game_active:
            self.play_button.draw_button()
            self.play_button_hardmode.draw_button()

        pygame.display.flip()

if __name__ == "__main__":
    #Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()