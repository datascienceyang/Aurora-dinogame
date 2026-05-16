"""
EOG Blink Controller for Dino Game
Receives RELAX values via BLE from Aurora device, detects blink.
"""

import threading
import queue
import time


class EOGInputController:
    """
    EOG-based input controller.
    Runs BLE connection in background thread, exposes synchronous interface
    for pygame main loop.
    """

    def __init__(self, threshold=50.0, cooldown_ms=400):
        """
        Args:
            threshold: RELAX value below this triggers jump (blink detected).
                       Lower RELAX = more tension/blink.
            cooldown_ms: Minimum time between jumps to prevent spam.
        """
        self.threshold = threshold
        self.cooldown_ms = cooldown_ms
        self._last_jump_time = 0
        self._jump_queue = queue.Queue(maxsize=5)
        self._relax_history = []
        self._latest_relax = None
        self._running = True
        self._thread = None
        self._connected = False

    def start(self):
        """Start BLE connection in background thread."""
        self._thread = threading.Thread(target=self._ble_worker, daemon=True)
        self._thread.start()

    def stop(self):
        """Stop the BLE worker thread."""
        self._running = False

    def _ble_worker(self):
        """Background thread: connect BLE and listen for messages."""
        try:
            from eog_ble import start as ble_start

            def handler(msg):
                if not self._running:
                    return
                if msg.startswith("RELAX:"):
                    try:
                        value = float(msg[len("RELAX:"):])
                    except ValueError:
                        return
                    self._latest_relax = value
                    self._relax_history.append(value)
                    if len(self._relax_history) > 100:
                        self._relax_history.pop(0)
                    self._detect_blink(value)

            self._connected = True
            ble_start(handler)
        except Exception as e:
            print(f"[EOG] BLE connection error: {e}")
            self._connected = False

    def _detect_blink(self, value):
        """Detect blink based on RELAX threshold with cooldown."""
        now = time.time() * 1000
        if now - self._last_jump_time < self.cooldown_ms:
            return
        # Blink = RELAX drops below threshold (less relaxed = blink)
        if value < self.threshold:
            self._last_jump_time = now
            try:
                self._jump_queue.put_nowait(True)
            except queue.Full:
                pass

    def is_blinking(self):
        """
        Check if a blink/jump was detected.
        Call this every frame in the main game loop.
        """
        try:
            self._jump_queue.get_nowait()
            return True
        except queue.Empty:
            return False

    @property
    def latest_relax(self):
        return self._latest_relax

    @property
    def is_connected(self):
        return self._connected

    def auto_calibrate(self):
        """
        Auto-calibrate threshold based on recent RELAX history.
        Call after a few seconds of normal eye state.
        """
        if len(self._relax_history) < 10:
            return
        avg = sum(self._relax_history) / len(self._relax_history)
        std = (sum((x - avg) ** 2 for x in self._relax_history) / len(self._relax_history)) ** 0.5
        # Threshold = average - 1.5 standard deviations
        self.threshold = max(avg - 1.5 * std, avg * 0.6)
        print(f"[EOG] Auto-calibrated threshold: {self.threshold:.1f}")


class EOGDinoGameController:
    """
    Adapter: EOGInputController -> DinoGame controller interface.
    """

    def __init__(self, DinoGame):
        self._game = DinoGame
        self.eog = EOGInputController()
        self.eog.start()
        self.jump_flag = False
        self._calibrated = False

    def get_input(self):
        """Check EOG blink and trigger jump."""
        if not self._calibrated and self.eog.latest_relax is not None:
            # Auto-calibrate after collecting some data
            self.eog.auto_calibrate()
            self._calibrated = True

        if self.eog.is_blinking() and not self.jump_flag:
            self.jump_flag = True
            self._game.start_game()
            self._game.player.jump(self._game.ground)
        elif not self.eog.is_blinking():
            self.jump_flag = False

    def get_restart(self):
        """Blink to restart on game over."""
        if self.eog.is_blinking() and not self.jump_flag:
            self.jump_flag = True
            self._game.player.jump(self._game.ground)
            self._game.restart()
        elif not self.eog.is_blinking():
            self.jump_flag = False
