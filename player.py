"""Module defining the Player class.

The Player class represents the player character in the game. It handles the
player's movement, animation, jumping, and ducking behavior.

Classes:
    Player: Represents the player character in the game.
"""

import math
import pygame


class Player(
    pygame.sprite.Sprite
):  # pylint: disable=too-many-instance-attributes
    """A class representing the player character in the game."""

    def __init__(self, surface, win_width, win_height) -> None:
        """Initialize the Player object.

        Args:
            surface (pygame.Surface): The surface on which the player will be
            drawn.
            win_width (int): The width of the game window.
            win_height (int): The height of the game window.
        """
        super().__init__()
        self._image = [
            pygame.image.load("images/mascot-run-1.png").convert_alpha(),
            pygame.image.load("images/mascot-run-2.png").convert_alpha(),
            pygame.image.load("images/mascot-run-3.png").convert_alpha(),
        ]
        self.rect = self._image[0].get_rect()
        self.rect.x = 100  # 向右挪100像素
        self.speed = [0, 1]
        self._surface = surface
        self._win_height = win_height
        self._win_width = win_width
        self._animation_frame = 0
        self.mask = 0

        self.is_ducking = False

    def draw_player(self, ground):
        """Draw the player on the surface.

        Args:
            ground (Ground): The ground object used to determine the player's
            position.
        """
        if False:  # ducking removed
            pass
        else:
            if self._animation_frame > len(self._image) - 0.2:
                self._animation_frame = 0
            else:
                self._animation_frame += 0.2
            idx = 0 if (
                self.rect.bottom
                < ground.get_rect().top + ground.get_rect().height / 2
            ) else math.floor(self._animation_frame)
            tinted = self._image[idx].copy()
            tinted.fill((30, 144, 255), special_flags=pygame.BLEND_MULT)  # 科技蓝
            self._surface.blit(tinted, self.rect)
            self.mask = pygame.mask.from_surface(self._image[idx])

    def update(self, ground):
        """Update the player's position and animation frame.

        Args:
            ground (Ground): The ground object used to determine the player's
            position.
        """
        self.rect = self.rect.move(self.speed)
        ground_target = ground.get_rect().top + ground.get_rect().height / 2 - 7  # 抬高7像素
        if self.rect.bottom > ground_target:
            self.speed[1] -= self.speed[1]
            self.rect.bottom = int(ground_target)
        else:
            self.speed[1] += 0.3

        self.rect = self._image[0].get_rect(bottomleft=(100, self.rect.bottom))

    def jump(self, ground):
        """Make the player character jump.

        Args:
            ground (Ground): The ground object used to determine if the player
            can jump.
        """
        if self.rect.bottom >= ground.get_rect().top:
            self.speed[1] -= 11

    def duck(self):
        """Make the player character duck."""
        self.is_ducking = True

    def unduck(self):
        """Make the player character stop ducking."""
        self.is_ducking = False
