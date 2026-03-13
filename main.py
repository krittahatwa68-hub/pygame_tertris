#!/usr/bin/env python3
"""
Tetris Game with OOP and SOLID Principles
Main entry point
"""

from src.game import Game
from src.config import DIFFICULTY_NORMAL


def main():
    """Main entry point for the game"""
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
    print("\nSOLID Principles Applied:")
    print("  - Single Responsibility: Each class has one reason to change")
    print("  - Open/Closed: Open for extension (new piece types easily added)")
    print("  - Liskov Substitution: All pieces work through Tetromino interface")
    print("  - Interface Segregation: Small, focused interfaces")
    print("  - Dependency Inversion: Depend on abstractions, not concretions")
    print("\n" + "=" * 60)
    print("Starting game...\n")
    
    # Create and run game
    game = Game(difficulty=DIFFICULTY_NORMAL)
    game.run()


if __name__ == "__main__":
    main()
