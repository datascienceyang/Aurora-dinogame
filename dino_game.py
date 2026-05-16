"""
Main program to setup and run the dino game
EOG Blink Control + Keyboard fallback
"""
import os
import sys

# Fix resource path for packaged exe
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
    os.chdir(base_path)

import pygame
from dino_game_controller import KeyboardDinoGameController
from dino_game_model import DinoGame
from dino_game_view import DinoGameView

# Try to import EOG controller; if bleak missing, use keyboard only
try:
    from eog_controller import EOGDinoGameController
    EOG_AVAILABLE = True
except ImportError:
    EOG_AVAILABLE = False
    print("[INFO] EOG module not available. Running in keyboard-only mode.")


def main():
    pygame.init()
    game = DinoGame()
    game_view = DinoGameView(game)
    keyboard_player = KeyboardDinoGameController(game)

    eog_player = None
    if EOG_AVAILABLE:
        try:
            eog_player = EOGDinoGameController(game)
            print("[EOG] Controller initialized. Waiting for BLE connection...")
        except Exception as e:
            print(f"[EOG] Failed to init: {e}")

    while game.running and game.is_intro:
        keyboard_player.get_input()
        if eog_player:
            eog_player.get_input()
        game_view.draw_intro()

    while game.running:
        keyboard_player.get_input()
        if eog_player:
            eog_player.get_input()
        if not game.game_over:
            game.update()
            game_view.update_view()
        else:
            keyboard_player.get_restart()
            if eog_player:
                eog_player.get_restart()
            game_view.show_end_screen()

    if eog_player:
        eog_player.eog.stop()
    pygame.quit()


if __name__ == "__main__":
    main()
