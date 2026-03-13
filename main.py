#!/usr/bin/env python3
"""
Tetris Game with OOP and SOLID Principles
Main entry point
"""

import sys
import os

# Ensure project root is in Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.game import Game
from rendering.renderer import Renderer
from input.input_handler import InputHandler
from config.config import DIFFICULTY_NORMAL


def print_banner():
    """Print game information banner"""

    print("=" * 60)
    print("TETRIS GAME - OOP & SOLID Principles Demonstration")
    print("=" * 60)

    print("\nGame Architecture Highlights:")
    print("  - Inheritance: Tetromino base class with 7 piece subclasses")
    print("  - Polymorphism: Each piece implements rotation differently")
    print("  - Encapsulation: Private attributes with property decorators")
    print("  - Composition: Game contains Board, Renderer, InputHandler")
    print("  - Factory Pattern: PieceFactory for creating pieces")
    print("  - Dependency Injection: Dependencies passed to classes")

    print("\nAdvanced Features:")
    print("  - 7-Bag Randomizer: Fair piece distribution")
    print("  - Gravity System: Progressive difficulty based on lines")
    print("  - Collision System: Accurate collision detection")
    print("  - Ghost Piece: Preview landing position")
    print("  - Wall Kick (SRS): Tetris Guideline rotation")
    print("  - Hold Piece: Hold and swap pieces")

    print("\nSOLID Principles Applied:")
    print("  - Single Responsibility Principle")
    print("  - Open/Closed Principle")
    print("  - Liskov Substitution Principle")
    print("  - Interface Segregation Principle")
    print("  - Dependency Inversion Principle")

    print("\n" + "=" * 60)
    print("Starting game...\n")


def main():
    """Main entry point for the game"""

    print_banner()

    try:
        # Initialize renderer
        renderer = Renderer()
        renderer.init()

        # Initialize input system
        input_handler = InputHandler()

        # Create game
        game = Game(
            renderer=renderer,
            input_handler=input_handler,
            difficulty=DIFFICULTY_NORMAL
        )

        # Run game loop
        game.run()

    except Exception as e:
        print("\nUnexpected error occurred:")
        print(e)

    finally:
        # Ensure pygame closes properly
        try:
            renderer.quit()
        except:
            pass


if __name__ == "__main__":
    main()