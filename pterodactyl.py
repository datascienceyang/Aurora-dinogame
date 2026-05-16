"""Module defining the Pterodactyl class.

The Pterodactyl class represents the pterodactyl obstacle in the game.
It handles the pterodactyls movement and animation behaviors.

Classes:
    Pterodactyl: Represents the pterodactyl obstacle in the game.
"""

import math
import pygame


# pylint: disable=too-many-instance-attributes
class Pterodactyl(pygame.sprite.Sprite):
    """A class representing a pterodactyl sprite in the game."""

    def __init__(self, surface, winwidth, winheight, height):
        """Initialize a pterodactyl sprite object.

        Args:
            surface (pygame.Surface): The surface on which the sprite will be
            drawn.
            winwidth (int): The width of the game window.
            winheight (int): The height of the game window.
            height (int): The initial height of the sprite.
        """
        super().__init__()
        self.images = [
            pygame.image.load("images/velociraptor-1.png").convert_alpha(),
            pygame.image.load("images/velociraptor-2.png").convert_alpha(),
        ]
        self.image = self.images[0]  # Set the initial image
        self.rect = self.image.get_rect()
        self._surface = surface
        self.winwidth = winwidth
        self.winheight = winheight

        self.rect.x = winwidth
        self.rect.y = height

        self.mask = pygame.mask.from_surface(self.image)
        self.animation_frame = 0

    def update(self, speed):
        """Update the position of the sprite based on the given speed.

        Args:
            speed (int): The speed at which the sprite moves.
        """
        self.rect.x -= speed

        if self.rect.right < 0:
            self.kill()

    def draw_ptero(self):
        """Draw the pterodactyl sprite on the surface."""
        if self.animation_frame > len(self.images) - 0.2:
            self.animation_frame = 0
        else:
            self.animation_frame += 0.05
        self.image = self.images[math.floor(self.animation_frame)]
        tinted = self.image.copy()
        tinted.fill((78, 205, 196), special_flags=pygame.BLEND_MULT)
        self._surface.blit(tinted, self.rect)
        self.mask = pygame.mask.from_surface(self.image)
