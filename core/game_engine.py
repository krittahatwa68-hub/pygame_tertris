"""
Game Engine
Responsible for the main game loop and timing
"""

from config.config import FPS


class GameEngine:

    def __init__(self, game, renderer):
        self._game = game
        self._renderer = renderer
        self._clock = renderer.get_clock()
        self._running = True

    def run(self):

        while self._running:

            # update game logic
            self._running = self._game.update()

            # render frame
            self._renderer.begin_frame()
            self._game.render()
            self._renderer.end_frame()

            # control FPS
            self._clock.tick(FPS)

        self.shutdown()

    def shutdown(self):

        self._renderer.quit()