"""
Controller for dino game
"""

from abc import ABC, abstractmethod
import pygame


class DinoGameController(ABC):
    """
    Dino game controller super class.
    """

    def __init__(self, DinoGame):  # pylint: disable=invalid-name
        self._game = DinoGame

    @property
    def game(self):
        return self._game

    @abstractmethod
    def get_input(self):
        """Check if the user has inputed a jump"""

    @abstractmethod
    def get_restart(self):
        """Check if the user has requested to restart"""


class KeyboardDinoGameController(DinoGameController):
    """
    Keyboard based controller for dino game
    """

    def get_restart(self):
        for event in pygame.event.get(pygame.MOUSEBUTTONDOWN):
            if self._game.restart_button.collidepoint(event.pos):
                self._game.restart()

    def get_input(self):
        for event in pygame.event.get((pygame.QUIT, pygame.KEYDOWN)):
            if event.type == pygame.QUIT:
                self._game.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self._game.start_game()
                    self._game.player.jump(self._game.ground)
