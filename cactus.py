"""Module defining the Cactus class.

The Cactus class represents the cactus obstacle in the game. It handles the
cactus's movement behavior.

Classes:
    Cactus: Represents the cactus character in the game.
"""

import random
import pygame


class Cactus(pygame.sprite.Sprite):
    """A class representing a cactus obstacle in the game."""

    def __init__(self, surface, winwidth, winheight):
        """Initialize the Cactus object.

        Args:
            surface (pygame.Surface): The surface on which the cactus will be
            drawn.
            image_path (str): The file path to the image of the cactus.
            winwidth (int): The width of the game window.
            winheight (int): The height of the game window.
        """
        super().__init__()
        # Removed wide cacti (group=75px, 10=50px) that are impossible to jump over
        self.images = [
            pygame.image.load("images/cactus-1.png").convert_alpha(),
            pygame.image.load("images/cactus-2.png").convert_alpha(),
            pygame.image.load("images/cactus-3.png").convert_alpha(),
            pygame.image.load("images/cactus-11.png").convert_alpha(),
            pygame.image.load("images/cactus-6.png").convert_alpha(),
            pygame.image.load("images/cactus-7.png").convert_alpha(),
            pygame.image.load("images/cactus-8.png").convert_alpha(),
            pygame.image.load("images/cactus-9.png").convert_alpha(),
        ]

        self._surface = surface
        self.winwidth = winwidth
        self.winheight = winheight

        self.image_choice = random.choice(self.images)
        self.mask = pygame.mask.from_surface(self.image_choice)
        self.rect = self.image_choice.get_rect()

        self.rect.x = winwidth
        self.rect.y = winheight - self.rect.height

    def update(self, speed):
        """Update the position of the cactus.

        Args:
            speed (int): The speed at which the cactus moves horizontally.
        """
        self.rect.x -= speed

        if self.rect.right < 0:
            self.kill()

    def draw(self):
        """Draw the cactus on the surface."""
        tinted = self.image_choice.copy()
        tinted.fill((255, 107, 107), special_flags=pygame.BLEND_MULT)
        self._surface.blit(tinted, self.rect)
