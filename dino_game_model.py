"""
Model for Dino Game
"""

import random
import pygame
from player import Player
from ground import Ground
from cactus import Cactus
from pterodactyl import Pterodactyl


class DinoGame:
    """
    Dino Game with basic play functionality

    Attributes:
     _WIN_WIDTH (int): The width of the game window.
    _WIN_HEIGHT (int): The height of the game window.
    _MIN_SPAWN_INTERVAL (int): The minimum interval in milliseconds
    for spawning obstacles.
    _MAX_SPAWN_INTERVAL (int): The maximum interval in milliseconds
    for spawning obstacles.
    _speed (float): The current speed of the game.
    _ACCELERATION (float): The acceleration factor for
    increasing speed over time.
    _MAX_SPEED (float): The maximum speed the game can reach.
    _score (int): The current score in the game.
    _restart_button (pygame.Rect): A rectangle restart button
    window (pygame.Surface): The game window surface.
    _player (Player): The player object.
    _ground (Ground): The ground object.
    _cacti (pygame.sprite.Group): A group containing cactus obstacles.
    _pterodactyls (pygame.sprite.Group): Pterodactyl obstacles.
    _spawn_interval (int):  Randomly generated interval for spawning obstacles.
    _clock (pygame.time.Clock): Clock object used for controlling game speed.
    _spawn_catcus_event(pygame.event): Event for spawning cacti.
    _game_over(bool): Boolean for game over.
    _running(bool): Boolean for if the game is still running
    _is_intro(bool): Boolean for showing the instruction screen
    """

    _WIN_WIDTH = 791
    _WIN_HEIGHT = 201
    _MIN_SPAWN_INTERVAL = 600  # Minimum interval in milliseconds
    _MAX_SPAWN_INTERVAL = 1800  # Maximum interval in milliseconds
    _speed = 2
    _ACCELERATION = 0.0005
    _MAX_SPEED = 6.5
    _score = -200
    _restart_button = pygame.Rect(
        _WIN_WIDTH // 2 - 36, _WIN_HEIGHT // 2 - 32, 72, 64
    )
    window = pygame.display.set_mode((_WIN_WIDTH, _WIN_HEIGHT))
    _player = Player(window, _WIN_WIDTH, _WIN_HEIGHT)
    _ground = Ground(_WIN_WIDTH, _WIN_HEIGHT, window, "images/ground.jpg")
    _cacti = pygame.sprite.Group()
    _pterodactyls = pygame.sprite.Group()
    _spawn_interval = random.randint(_MIN_SPAWN_INTERVAL, _MAX_SPAWN_INTERVAL)
    _clock = pygame.time.Clock()

    def __init__(self):
        """
        Initialize the dino game model.
        """

        self._spawn_cactus_event = (
            pygame.USEREVENT + 1
        )  # pylint: disable=no-member
        pygame.time.set_timer(self._spawn_cactus_event, 1500)
        self._game_over = False
        self._running = True
        self._is_intro = True

    @property
    def is_intro(self):
        """Get the _is_intro attribute"""
        return self._is_intro

    @property
    def ground(self):
        """Get the _ground attribute"""
        return self._ground

    @property
    def running(self):
        """Get the _running attribute"""
        return self._running

    @property
    def player(self):
        """Get the _player attribute"""
        return self._player

    @property
    def cacti(self):
        """Get the _cactiattribute"""
        return self._cacti

    @property
    def pterodactyls(self):
        """Get the _pterodactyls attribute"""
        return self._pterodactyls

    @property
    def score(self):
        """Get the _score attribute"""
        return self._score

    @property
    def win_width(self):
        """Get the _WIN_WIDTH attribute"""
        return self._WIN_WIDTH

    @property
    def win_height(self):
        """Get the _WIN_HEIGHT attribute"""
        return self._WIN_HEIGHT

    @property
    def game_over(self):
        """Get the _game_over attribute"""
        return self._game_over

    @property
    def restart_button(self):
        """Get the _restart_button attribute"""
        return self._restart_button

    def restart(self):
        """
        Restart the game.
        """
        self._game_over = False
        self._score = -30
        self._speed = 2
        self._pterodactyls.empty()
        self._cacti.empty()
        # Clear any accumulated spawn events to prevent burst spawning
        pygame.event.get(pygame.USEREVENT + 1)
        self.update()

    def quit(self):
        """Quit out of the game"""
        self._running = False

    def start_game(self):
        """Exit the instructions stage"""
        self._is_intro = False
        # Clear accumulated spawn events from intro screen
        pygame.event.get(pygame.USEREVENT + 1)

    def duck(self):
        """
        Changes player sprite to duck
        """
        self._player.duck()

    def unduck(self):
        """
        Changes player sprite to stand up
        """
        self._player.unduck()

    def jump(self):
        """
        Makes player jump
        """
        self._player.jump(self._ground)

    def update(self):
        """
        Updates the states of the game at every time step
        """
        self._player.update(self._ground)
        self._ground.update(self._speed)
        self._cacti.update(self._speed)
        self._pterodactyls.update(self._speed)
        for cactus in self._cacti:
            offset_x = cactus.rect.left - self._player.rect.left
            offset_y = cactus.rect.top - self._player.rect.top

            if self._player.mask.overlap(cactus.mask, (offset_x, offset_y)):
                self._game_over = True

        for ptero in self._pterodactyls:
            offset_x = ptero.rect.left - self._player.rect.left
            offset_y = ptero.rect.top - self._player.rect.top

            if self._player.mask.overlap(ptero.mask, (offset_x, offset_y)):
                self._game_over = True
        # slowly increase the speed
        if self._speed < self._MAX_SPEED:
            self._speed += self._ACCELERATION
        self._score += self._speed / 5
        # Generate cacti randomly
        for _ in pygame.event.get(pygame.USEREVENT + 1):
            if self._score >= 0:
                if self._score < 500 or random.random() > 0.25:
                    new_cactus = Cactus(
                        self.window, self._WIN_WIDTH, self._WIN_HEIGHT
                    )
                    self._cacti.add(new_cactus)
                else:  # only generate pterodactyls after score is 500
                    ptero_heights = [
                        self._WIN_HEIGHT - 40,
                        self._WIN_HEIGHT - 60,
                        self._WIN_HEIGHT - 80,
                    ]
                    height = random.choice(ptero_heights)
                    new_ptero = Pterodactyl(
                        self.window, self._WIN_WIDTH, self._WIN_HEIGHT, height
                    )
                    self._pterodactyls.add(new_ptero)
        pygame.display.flip()
        self._clock.tick(60)
