# Tetris Game - OOP & SOLID Principles Demonstration

## 📋 Overview

This is a comprehensive Tetris game implementation using Python and Pygame, specifically designed to demonstrate the application of **Object-Oriented Programming (OOP)** principles and **SOLID** design principles in game development.

## 👥 Team Information

**Team Name:** Game Development Team

**Team Members:**
- Lead Developer: Comprehensive Game Architecture
- Contributing Developer: Educational Code Examples

**Project Focus:** Educational demonstration of software engineering best practices through game implementation

## 🎯 Project Objectives

This project demonstrates professional software engineering practices:

1. **Object-Oriented Programming (OOP)**
   - Inheritance
   - Polymorphism
   - Encapsulation
   - Composition/Aggregation

2. **SOLID Principles**
   - **S**ingle Responsibility Principle
   - **O**pen/Closed Principle
   - **L**iskov Substitution Principle
   - **I**nterface Segregation Principle
   - **D**ependency Inversion Principle

## 🏗️ Architecture

### Project Structure

```
pygame_tetris/
├── main.py                 # Entry point (demonstrates orchestration)
├── requirements.txt        # Python dependencies
├── pyproject.toml         # Project configuration (PEP 517/518)
├── README.md              # This file
└── src/
    ├── __init__.py
    ├── config.py          # Configuration constants (Single Responsibility)
    ├── pieces.py          # Tetromino classes (Inheritance, Polymorphism)
    ├── board.py           # Game board logic (Encapsulation)
    ├── renderer.py        # Rendering system (Single Responsibility)
    ├── input_handler.py   # Input handling (Single Responsibility)
    └── game.py            # Main game controller (Composition, Dependency Injection)
```

### Design Patterns & Principles Applied

#### **OOP: Inheritance & Polymorphism**

```python
# Abstract Base Class
class Tetromino(ABC):
    @abstractmethod
    def _define_blocks(self) -> List[List[Tuple[int, int]]]:
        pass
    
    def get_color(self) -> Tuple[int, int, int]:
        pass

# Concrete Implementations (Subclasses)
class IPiece(Tetromino):      # Cyan I-piece
class OPiece(Tetromino):      # Yellow O-piece
class TPiece(Tetromino):      # Magenta T-piece
# ... etc for S, Z, J, L pieces
```

- **Polymorphism**: Each piece type implements its own rotation logic and color while adhering to the common interface
- **Liskov Substitution**: All pieces can be used interchangeably through the `Tetromino` interface

#### **OOP: Encapsulation**

```python
class Tetromino(ABC):
    def __init__(self, x: int, y: int):
        self._x = x              # Private attributes
        self._y = y
        self._rotation = 0
        self._blocks = self._define_blocks()
    
    @property                     # Property decorators for controlled access
    def x(self) -> int:
        return self._x
    
    def set_position(self, x: int, y: int) -> None:
        self._x = x
        self._y = y
```

#### **OOP: Composition**

```python
class Game:
    def __init__(self):
        # Composition: Game "has-a" Board, Renderer, InputHandler
        self._board = Board()
        self._renderer = Renderer()
        self._input_handler = InputHandler()
        self._current_piece: Tetromino = None
```

#### **Design Patterns**

- **Factory Pattern**: `PieceFactory` for creating Tetromino instances
- **Dependency Injection**: Components receive dependencies rather than creating them

#### **SOLID Principles**

| Principle | Implementation |
|-----------|----------------|
| **S**ingle Responsibility | Each class has one reason to change: `config.py` (configuration), `board.py` (board state), `renderer.py` (rendering), `input_handler.py` (input) |
| **O**pen/Closed | `Tetromino` base class is open for extension (new piece types) but closed for modification |
| **L**iskov Substitution | All `Tetromino` subclasses can replace the base class in `Game` logic |
| **I**nterface Segregation | Small, focused classes with specific responsibilities |
| **D**ependency Inversion | `Game` depends on abstractions (`Board`, `Renderer`) not concrete implementations |

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

#### Option 1: Using requirements.txt

```bash
# Navigate to project directory
cd pygame_tetris

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Option 2: Using pyproject.toml (PEP 517/518)

```bash
# Navigate to project directory
cd pygame_tetris

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install the package in development mode
pip install -e .

# Optional: Install with development dependencies
pip install -e ".[dev]"
```

#### Option 3: Direct Dependencies Installation

```bash
pip install pygame>=2.1.0
```

## 🎮 Usage

### Running the Game

```bash
python main.py
```

### Game Controls

| Key | Action |
|-----|--------|
| **← →** | Move piece left/right |
| **↓** | Move piece down faster |
| **Z** | Rotate piece |
| **Space** | Drop piece instantly |
| **P** | Pause/Resume game |
| **ESC** or Close Window | Exit game |

### Game Rules

1. Pieces fall from the top of the board
2. Players can move left/right and rotate falling pieces
3. When a piece reaches the bottom or another piece, it locks in place
4. Completed rows (fully filled with blocks) are cleared
5. Score increases based on number of rows cleared at once
6. Game ends when pieces reach the top of the board

## 🎓 Learning Points

### Understanding the Code

1. **pieces.py**: Study inheritance and polymorphism
   - `Tetromino` is the abstract base class
   - Seven concrete classes (IPiece, OPiece, etc.) inherit from it
   - Each implements `_define_blocks()` with different rotation patterns

2. **board.py**: Learn about encapsulation
   - Private `_grid` attribute
   - Public methods for interaction: `is_valid_position()`, `lock_piece()`, etc.

3. **game.py**: Study composition and orchestration
   - Contains all game components through composition
   - Dependency injection pattern in action

4. **renderer.py**: Single responsibility in action
   - Only handles rendering
   - Receives game state, doesn't manage it

5. **input_handler.py**: Separation of concerns
   - Only converts input events to actions
   - Game logic remains in `Game` class

## 🔧 Extension Points

The architecture makes it easy to extend:

```python
# Add a new piece type:
class NewPiece(Tetromino):
    def _define_blocks(self):
        # Define rotations
        pass
    
    def get_color(self):
        return NEW_COLOR

# Register in PieceFactory
PieceFactory._pieces['NEW'] = NewPiece

# Add new difficulty level - modify config.py
DIFFICULTY_INSANE = 0.2

# Add new input action - modify InputHandler
```

## 📦 Dependencies

- **pygame** (>=2.1.0): Game development library for graphics, sound, and input handling

Optional development dependencies (in `pyproject.toml`):
- pytest: Unit testing framework
- pytest-cov: Code coverage
- black: Code formatting
- flake8: Linting
- mypy: Static type checking

## 📄 License

MIT License - See project files for details

## 🤝 Contributing

To improve this codebase:

1. Follow the established architecture patterns
2. Maintain SOLID principles
3. Add unit tests for new features
4. Update documentation

## 🎯 Educational Resources

For deeper understanding of the concepts used:

- **OOP Concepts**: Consider reading "Python Object-Oriented Programming" by Duncan
- **SOLID Principles**: "Clean Code" by Robert C. Martin
- **Design Patterns**: "Design Patterns: Elements of Reusable Object-Oriented Software" by Gang of Four

## ⚠️ Notes

- This is an educational project demonstrating best practices
- Performance optimizations for production use may vary
- Graphics and sound are intentionally minimal to focus on architecture
- Type hints are included for clarity (Python 3.8+)

## 📞 Support

For questions or issues:
1. Review the source code comments
2. Check the architecture documentation above
3. Study the specific module implementing a feature

---

**Version:** 1.0.0  
**Created:** 2024  
**Focus:** OOP & SOLID Principles Educational Demonstration
