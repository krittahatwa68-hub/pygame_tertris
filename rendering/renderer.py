"""
Game Renderer
Single Responsibility: All rendering logic
Dependency Injection: Receives pygame and board/game state
"""

import pygame
from typing import Optional
from config.config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, CELL_SIZE, BOARD_X, BOARD_Y,
    COLOR_BLACK, COLOR_WHITE, COLOR_LIGHT_GRAY, COLOR_GRAY,
    BOARD_WIDTH, BOARD_HEIGHT
)

from game.world.board import Board
from game.entities.tetromino import Tetromino
from ui.menu_screen import MenuScreen, GameOverScreen, PauseScreen


class Renderer:
    """
    Handles all rendering of the game
    Encapsulation: Private pygame objects and assets
    """

    def __init__(self, width: int = WINDOW_WIDTH, height: int = WINDOW_HEIGHT):

        self._width = width
        self._height = height

        self._screen: Optional[pygame.Surface] = None
        self._clock: Optional[pygame.time.Clock] = None

        self._font: Optional[pygame.font.Font] = None
        self._small_font: Optional[pygame.font.Font] = None

        self._menu_screen: Optional[MenuScreen] = None
        self._game_over_screen: Optional[GameOverScreen] = None
        self._pause_screen: Optional[PauseScreen] = None

    def init(self) -> None:
        """Initialize pygame and create window"""

        pygame.init()

        self._screen = pygame.display.set_mode((self._width, self._height))
        pygame.display.set_caption("Tetris - OOP & SOLID Principles Demo")

        self._clock = pygame.time.Clock()

        self._font = pygame.font.Font(None, 36)
        self._small_font = pygame.font.Font(None, 24)

        self._menu_screen = MenuScreen(self._screen, self._font)
        self._game_over_screen = GameOverScreen(self._screen, self._font)
        self._pause_screen = PauseScreen(self._screen, self._font)

    def render(
        self,
        board: Board,
        current_piece: Optional[Tetromino],
        ghost_piece: Optional[list],
        held_piece: Optional[Tetromino],
        next_piece: Optional[Tetromino],
        score: int,
        lines: int,
        level: int,
        game_state: int
    ) -> None:

        if not self._screen:
            return

        self._screen.fill(COLOR_BLACK)

        self._draw_board(board)
        self._draw_grid()

        if ghost_piece and current_piece:
            self._draw_ghost_piece(ghost_piece, current_piece)

        if current_piece:
            self._draw_piece(current_piece)

        self._draw_ui(score, lines, level, held_piece, next_piece)


    def _draw_board(self, board: Board) -> None:

        if not self._screen:
            return

        grid = board.get_grid()

        for y in range(len(grid)):
            for x in range(len(grid[y])):

                color = grid[y][x]

                if color != COLOR_BLACK:
                    self._draw_cell(x, y, color)

    def _draw_piece(self, piece: Tetromino) -> None:

        color = piece.get_color()

        for x, y in piece.get_blocks():

            if 0 <= y < BOARD_HEIGHT:
                self._draw_cell(x, y, color)

    def _draw_ghost_piece(self, ghost_blocks: list, piece: Tetromino) -> None:

        if not self._screen:
            return

        color = piece.get_color()
        ghost_color = tuple(c // 2 for c in color)

        for x, y in ghost_blocks:

            if 0 <= y < BOARD_HEIGHT and 0 <= x < BOARD_WIDTH:

                pixel_x = BOARD_X + x * CELL_SIZE
                pixel_y = BOARD_Y + y * CELL_SIZE

                rect = pygame.Rect(pixel_x, pixel_y, CELL_SIZE, CELL_SIZE)

                pygame.draw.rect(self._screen, ghost_color, rect, 2)

    def _draw_cell(self, x: int, y: int, color: tuple) -> None:

        if not self._screen:
            return

        pixel_x = BOARD_X + x * CELL_SIZE
        pixel_y = BOARD_Y + y * CELL_SIZE

        rect = pygame.Rect(pixel_x, pixel_y, CELL_SIZE, CELL_SIZE)

        pygame.draw.rect(self._screen, color, rect)
        pygame.draw.rect(self._screen, COLOR_LIGHT_GRAY, rect, 1)

    def _draw_grid(self) -> None:

        if not self._screen:
            return

        for x in range(BOARD_WIDTH + 1):

            start_pos = (BOARD_X + x * CELL_SIZE, BOARD_Y)
            end_pos = (BOARD_X + x * CELL_SIZE, BOARD_Y + BOARD_HEIGHT * CELL_SIZE)

            pygame.draw.line(self._screen, COLOR_LIGHT_GRAY, start_pos, end_pos)

        for y in range(BOARD_HEIGHT + 1):

            start_pos = (BOARD_X, BOARD_Y + y * CELL_SIZE)
            end_pos = (BOARD_X + BOARD_WIDTH * CELL_SIZE, BOARD_Y + y * CELL_SIZE)

            pygame.draw.line(self._screen, COLOR_LIGHT_GRAY, start_pos, end_pos)

    def _draw_ui(
        self,
        score: int,
        lines: int,
        level: int,
        held_piece: Optional[Tetromino],
        next_piece: Optional[Tetromino]
    ) -> None:

        if not self._screen or not self._font or not self._small_font:
            return

        ui_x = BOARD_X + BOARD_WIDTH * CELL_SIZE + 50

        level_text = self._font.render(f"Level: {level}", True, COLOR_WHITE)
        self._screen.blit(level_text, (ui_x, 30))

        score_text = self._font.render(f"Score: {score}", True, COLOR_WHITE)
        self._screen.blit(score_text, (ui_x, 80))

        lines_text = self._small_font.render(f"Lines: {lines}", True, COLOR_WHITE)
        self._screen.blit(lines_text, (ui_x, 130))

        held_label = self._small_font.render("HOLD", True, (100, 200, 255))
        self._screen.blit(held_label, (ui_x, 180))

        if held_piece:
            self._draw_preview_piece(held_piece, ui_x, 210)
        else:
            pygame.draw.rect(self._screen, COLOR_GRAY, (ui_x, 210, 80, 80), 2)

        next_label = self._small_font.render("NEXT", True, (100, 200, 255))
        self._screen.blit(next_label, (ui_x, 310))

        if next_piece:
            self._draw_preview_piece(next_piece, ui_x, 340)

        inst_y = 440

        instructions = [
            "Arrow Keys: Move",
            "Z: Rotate",
            "Space: Drop",
            "C: Hold",
            "P: Pause",
        ]

        inst_label = self._small_font.render("CONTROLS", True, (100, 200, 255))
        self._screen.blit(inst_label, (ui_x, inst_y - 20))

        for i, instruction in enumerate(instructions):

            text = self._small_font.render(instruction, True, COLOR_WHITE)

            self._screen.blit(text, (ui_x, inst_y + i * 25))

    def _draw_preview_piece(self, piece: Tetromino, x: int, y: int) -> None:

        if not self._screen:
            return

        color = piece.get_color()

        preview_cell_size = 15

        blocks = piece.get_blocks()

        min_x = min(b[0] for b in blocks)
        min_y = min(b[1] for b in blocks)

        for bx, by in blocks:

            px = x + (bx - min_x) * preview_cell_size
            py = y + (by - min_y) * preview_cell_size

            rect = pygame.Rect(px, py, preview_cell_size - 1, preview_cell_size - 1)

            pygame.draw.rect(self._screen, color, rect)
            pygame.draw.rect(self._screen, COLOR_LIGHT_GRAY, rect, 1)

    def get_clock(self) -> pygame.time.Clock:

        if not self._clock:
            raise RuntimeError("Renderer not initialized")

        return self._clock

    def render_menu(self) -> None:

        if self._menu_screen:
            self._menu_screen.render()
            pygame.display.flip()

    def update_menu(self, mouse_pos: tuple) -> None:

        if self._menu_screen:
            self._menu_screen.update(mouse_pos)

    def handle_menu_click(self, mouse_pos: tuple) -> Optional[str]:

        if self._menu_screen:
            return self._menu_screen.handle_click(mouse_pos)

        return None

    def render_pause(self) -> None:
        if self._pause_screen:
            self._pause_screen.render()

    def update_pause(self, mouse_pos: tuple) -> None:
        if self._pause_screen:
            self._pause_screen.update(mouse_pos)

    def handle_pause_click(self, mouse_pos: tuple) -> Optional[str]:
        if self._pause_screen:
            return self._pause_screen.handle_click(mouse_pos)
        return None

    def render_game_over(
        self,
        score: int,
        lines: int,
        level: int,
        high_score: int = 0
    ) -> None:

        if self._game_over_screen:
            self._game_over_screen.render(score, lines, level, high_score)
            pygame.display.flip()

    def update_game_over(self, mouse_pos: tuple) -> None:

        if self._game_over_screen:
            self._game_over_screen.update(mouse_pos)

    def handle_game_over_click(self, mouse_pos: tuple) -> Optional[str]:

        if self._game_over_screen:
            return self._game_over_screen.handle_click(mouse_pos)

        return None

    def quit(self) -> None:

        pygame.quit()