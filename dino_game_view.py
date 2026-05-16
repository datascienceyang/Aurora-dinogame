"""
View for dino game
"""

import math
import pygame


class DinoGameView:
    """
    Creates a Dino Game view

    Attributes:
        _FONT_PATH: string path to custom font time
        _FONT: pygame.font object loading the font
        _game: the DinoGame object
    """

    pygame.init()
    _FONT_PATH = "PressStart2P-Regular.ttf"
    _FONT = pygame.font.Font(_FONT_PATH, 16)

    def __init__(self, DinoGame):  # pylint: disable=invalid-name
        """
        Initialize Dino Game view

        Parameters:
            DinoGame
        """

        self._game = DinoGame
        pygame.display.set_caption("Dino Game")

    def draw_intro(self):
        """
        Draw the intro screen/instructions
        """
        font = pygame.font.Font(self._FONT_PATH, 10)
        self._game.window.fill((240, 248, 255))
        self._game.ground.draw_ground()
        text = [
            "EOG Blink Dino Game",
            "Control by BLINKING your eyes!",
            "Press SPACE to jump / start.",
        ]
        spacing = 0.1
        for index, line in enumerate(text):  # draw text on new lines
            word_surface = font.render(line, 0, (0, 0, 128))
            word_rect = word_surface.get_rect(
                midtop=(
                    self._game.win_width / 2,
                    spacing * self._game.win_height,
                )
            )
            self._game.window.blit(word_surface, word_rect)
            if index != len(text) - 2:
                spacing += 0.1
            else:
                spacing += 0.25
        pygame.display.flip()

    def update_view(self):
        """
        Draw the view based on current changes in the model.
        """
        # draw background and player
        self._game.window.fill((240, 248, 255))
        self._game.ground.draw_ground()
        self._game.player.draw_player(self._game.ground)
        # draw obstacles one by one
        for cactus in self._game.cacti:
            cactus.draw()
        for ptero in self._game.pterodactyls:
            ptero.draw_ptero()
        # the score starts negative for calibration, only draw after calibration
        if self._game.score >= 0:
            score_text = self._FONT.render(  # score ticker
                f"{math.floor(self._game.score):05d}", True, (0, 0, 128)
            )
            score_rect = score_text.get_rect(
                topright=(self._game.win_width - 10, 10)
            )
            self._game.window.blit(score_text, score_rect)
        else:  # calibration loading text
            calibration_text = self._FONT.render(
                "Calibrating...", True, (0, 0, 128)
            )
            calibration_rect = calibration_text.get_rect(
                midtop=(self._game.win_width / 2, self._game.win_height / 2)
            )
            self._game.window.blit(calibration_text, calibration_rect)

    def show_end_screen(self):
        """
        Draw the game over screen when the players hits an obstacle
        """
        game_over_text = pygame.image.load(
            "images/game-over.jpg"
        ).convert_alpha()
        game_over_rect = game_over_text.get_rect(
            center=(
                self._game.win_width // 2,
                self._game.win_height // 2 - 50,
            )
        )
        self._game.window.blit(game_over_text, game_over_rect)
        # Draw restart button
        pygame.draw.rect(
            self._game.window, (30, 58, 95), self._game.restart_button
        )
        restart_text = pygame.image.load(
            "images/restart-button.jpg"
        ).convert_alpha()
        restart_rect = restart_text.get_rect(
            center=self._game.restart_button.center
        )
        self._game.window.blit(restart_text, restart_rect)
        # draw instruction text
        instruction_text = "Click the button or jump to restart!"
        instruction_surface = self._FONT.render(
            instruction_text, 0, (0, 0, 128)
        )
        instruction_rect = instruction_surface.get_rect(
            midtop=(
                self._game.win_width / 2,
                0.65 * self._game.win_height,
            )
        )
        self._game.window.blit(instruction_surface, instruction_rect)
        pygame.display.flip()
