"""Module defining the Ground class.

The Ground class represents the ground in the game. It handles the ground's
movement behavior.

Classes:
    Ground: Represents the player character in the game.
"""

import pygame


class Ground(pygame.sprite.Sprite):
    """A class representing the ground in the game."""

    def __init__(self, winwidth, winheight, surface, image_path):
        """Initialize the Ground object.

        Args:
            winwidth (int): The width of the game window.
            winheight (int): The height of the game window.
            surface (pygame.Surface): The surface on which the ground will be
            drawn.
            image_path (str): The file path to the image of the ground.
        """
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.winwidth = winwidth
        self.winheight = winheight
        self._surface = surface

        self.rect.y = self.winheight - self.rect.height

        self.x_1 = 0
        self.x_2 = self.rect.width

    def update(self, speed):
        """Update the position of the ground.

        Args:
            speed (int): The speed at which the ground moves horizontally.
        """
        self.x_1 -= speed
        self.x_2 -= speed

        if self.x_1 + self.rect.width < 0:
            self.x_1 = self.x_2 + self.rect.width
        if self.x_2 + self.rect.width < 0:
            self.x_2 = self.x_1 + self.rect.width

    def draw_ground(self):
        """Draw the ground on the surface."""
        # Apply blue tint to ground
        tinted1 = self.image.copy()
        tinted1.fill((30, 58, 95), special_flags=pygame.BLEND_MULT)
        tinted2 = self.image.copy()
        tinted2.fill((30, 58, 95), special_flags=pygame.BLEND_MULT)
        self._surface.blit(tinted1, (self.x_1, self.rect.y))
        self._surface.blit(tinted2, (self.x_2, self.rect.y))

    def get_rect(self):
        """Return the rectangular area occupied by the ground."""
        return pygame.Rect(0, self.rect.y, self.winwidth, 0.1 * self.winheight)
