"""
Game Configuration Constants
Single Responsibility: Contains all configuration values
"""

# Window Configuration
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Board Configuration
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
CELL_SIZE = 25

# Board Position
BOARD_X = 50
BOARD_Y = 50

# Colors (RGB)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GRAY = (128, 128, 128)
COLOR_LIGHT_GRAY = (200, 200, 200)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_CYAN = (0, 255, 255)
COLOR_MAGENTA = (255, 0, 255)
COLOR_YELLOW = (255, 255, 0)
COLOR_ORANGE = (255, 165, 0)

# Tetromino Colors
TETROMINO_COLORS = {
    'I': COLOR_CYAN,
    'O': COLOR_YELLOW,
    'T': COLOR_MAGENTA,
    'S': COLOR_GREEN,
    'Z': COLOR_RED,
    'J': COLOR_BLUE,
    'L': COLOR_ORANGE,
}

# Game States
GAME_MENU = 0
GAME_RUNNING = 1
GAME_PAUSED = 2
GAME_OVER = 3

# Difficulty Levels
DIFFICULTY_EASY = 1.0
DIFFICULTY_NORMAL = 0.7
DIFFICULTY_HARD = 0.4

# Button Configuration
BUTTON_WIDTH = 150
BUTTON_HEIGHT = 50
BUTTON_COLOR = COLOR_BLUE
BUTTON_HOVER_COLOR = (0, 0, 200)
BUTTON_TEXT_COLOR = COLOR_WHITE

# Advanced Mechanics Configuration
DAS_DELAY = 10         # Delayed Auto Shift (frames)
ARR = 2                # Auto Repeat Rate (frames)
LOCK_DELAY_MS = 500    # Lock delay in milliseconds
MAX_LOCK_RESETS = 15   # Maximum number of times lock delay can be reset
