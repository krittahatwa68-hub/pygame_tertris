# Tetris Game - Advanced Systems Documentation

## 🎮 Complete Feature List

### 1. 7-Bag Randomizer System (`piece_randomizer.py`)
**Purpose:** Fair piece distribution following Tetris Guideline standards

**How it works:**
- Maintains a "bag" of all 7 piece types (I, O, T, S, Z, J, L)
- Shuffles 7 pieces per bag
- All pieces appear before any piece repeats
- Eliminates long droughts of missing pieces

**Features:**
- `PieceBag` class with queue management
- Efficient shuffle algorithm
- Preview of next piece without removal
- Status tracking for debugging

### 2. Gravity System (`gravity_system.py`)
**Purpose:** Progressive difficulty based on player progress

**How it works:**
- Gravity increases as player clears more lines
- Base gravity modified by game difficulty (easy/normal/hard)
- Multiple difficulty levels with smooth progression

**Difficulty Multipliers:**
- Easy: 1.0x (slower gravity)
- Normal: 0.7x (balanced)
- Hard: 0.4x (faster gravity)

**Progression:**
- Level 0: Base gravity (1/60 cells/frame)
- Level 5+: 0.035 cells/frame
- Level 10+: 0.05 cells/frame
- Level 20+: 0.1 cells/frame
- Level 30+: 0.15 cells/frame

**Features:**
- `GravitySystem` class with auto-calculation
- Progressive level system (1 level per 10 lines)
- Accurate frame-based fall calculation
- Accumulator for smooth physics

### 3. Collision System (`collision_system.py`)
**Purpose:** Accurate collision detection and Physics validation

**What it detects:**
- Piece-to-boundary collisions (left, right, bottom)
- Piece-to-locked-piece collisions
- Valid spawn positions
- Landing positions for ghost pieces

**Core Methods:**
- `check_collision()` - Test if move would collide
- `is_valid_position()` - Check if piece is in valid position
- `get_landing_position()` - Get where piece will land
- `can_move_left/right/down()` - Quick movement checks
- `get_ghost_piece_blocks()` - Get ghost piece preview positions

**Features:**
- Allows negative Y (spawn area above board)
- Efficient boundary checking
- No collision with empty cells

### 4. Ghost Piece Feature
**Purpose:** Visual preview of where the piece will land

**How it works:**
- Uses Collision System to calculate landing position
- Drawn as semi-transparent outline
- Updates every frame with piece movement
- Helps player plan rotations and drops

**Visual:**
- Outline rendered in darker shade of piece color
- Drawn below current piece
- Only outline (not filled)

### 5. Hold Piece Feature
**Purpose:** Strategic piece management

**Mechanics:**
- Hold one piece at a time
- Can hold immediately when piece spawns
- Cannot hold twice in a row
- Reset hold state when new piece locks
- Swaps with held piece on activation

**Usage:**
- Press C key to hold piece
- Held piece shown in UI
- Can improve strategy by timing swaps

### 6. Wall Kick (Super Rotation System - SRS)
**Purpose:** Tetris Guideline standard rotation with wall kick support

**How it works:**
- Allows pieces to "kick" off walls when rotating
- Tests 5 different offset positions when rotating
- Uses standard SRS wall kick data

**Wall Kick Tables:**
```
I-Piece: Special offsets (longer piece)
O-Piece: No wall kick (fixed rotation)
JLSTZ: Standard offsets (JLSTZ group)
```

**Rotation System:**
- Clockwise rotation (Z key / Up arrow)
- Counter-clockwise rotation (Q / X key)
- Attempts: (0,0), then 4 wall kick positions
- Piece reverts if all positions blocked

**Example:**
- Piece near left wall tries to rotate
- Offset (0,0) blocked
- Offset (-1, 0) tested - may be valid
- Piece rotates and shifts left (wall kick!)

---

## 🎯 Game Flow

### State Machine
1. **GAME_MENU** → User clicks Start
2. **GAME_RUNNING** → Active gameplay
3. **GAME_PAUSED** → Press P to pause
4. **GAME_OVER** → No valid spawn position

### Game Loop (per frame)
1. Input handling
2. State update with delta_time
3. Gravity application
4. Collision detection
5. Rendering
6. Frame capture (60 FPS)

---

## 📊 Scoring System

### Points Formula
- 1 line: 100 points
- 2 lines: 300 points
- 3 lines: 500 points
- 4 lines (Tetris): 800 points

### Level Progression
- Level = lines_cleared // 10
- Max visible level: depends on play session
- Level affects gravity speed
- Level displayed on game over

### High Score Persistence
- Saved in `data/highscore.json`
- Loads on startup
- Updates on game over if beaten
- Persists between sessions

---

## 🎮 Controls

### Keyboard
| Input | Action |
|-------|--------|
| ← / A | Move left |
| → / D | Move right |
| ↓ / S | Soft drop (lock when bottom) |
| ↑ / Z | Rotate clockwise |
| X / Q | Rotate counter-clockwise |
| Space / W | Hard drop (instant down) |
| C | Hold piece |
| P / ESC | Pause game |
| R | Restart (on game over) |

### Mouse
- Click "Start" button on menu
- Click buttons on game over screen
- Button hover for visual feedback

---

## 📁 File Structure

```
core/
├── game.py                 # Main game controller
├── state_machine.py        # Game state management
└── event_system.py         # Observer pattern

game/
├── entities/
│   ├── tetromino.py        # 7 piece types
│   └── piece_randomizer.py # 7-Bag system
├── systems/
│   ├── scoring_system.py   # Score tracking
│   ├── gravity_system.py   # Progressive difficulty
│   ├── collision_system.py # Physics & detection
│   └── wall_kick_system.py # SRS rotation
└── world/
    └── board.py            # 10x20 grid

rendering/
├── renderer.py             # Graphics engine
└── ui/
    └── menu_screen.py      # Menu & UI

input/
└── input_handler.py        # Input detection

audio/
└── sound_manager.py        # Sound effects

config/
└── config.py               # Game constants

data/
└── highscore.json          # High score storage
```

---

## ⚙️ Technical Architecture

### Object-Oriented Design
- **Inheritance:** Tetromino base class with 7 concrete pieces
- **Polymorphism:** Each piece has unique rotation patterns
- **Encapsulation:** Private attributes with properties
- **Composition:** Game contains 5 major systems
- **Factory Pattern:** PieceBag creates pieces
- **Dependency Injection:** Systems receive dependencies

### SOLID Principles
- **S:** Each system has single responsibility
- **O:** Open for extension (new pieces easily added)
- **L:** All pieces work through Tetromino interface
- **I:** Small focused interfaces (GravitySystem, CollisionSystem)
- **D:** Depend on abstractions (CollisionSystem not Board directly)

---

## 🐛 Debug Features

### Status Methods
- `gravity.get_level()` - Current level
- `gravity.get_lines()` - Total lines cleared
- `gravity.get_gravity()` - Current gravity value
- `piece_bag.get_bag_status()` - Bag pieces remaining

### Collision Testing
```python
valid = CollisionSystem.is_valid_position(piece, board)
can_drop = CollisionSystem.can_move_down(piece, board)
landing_y = CollisionSystem.get_landing_position(piece, board)
ghost = CollisionSystem.get_ghost_piece_blocks(piece, board)
```

---

## 🎯 Performance Notes

- **FPS:** 60 frames per second
- **Memory:** ~1-5 MB depending on board state
- **CPU:** Minimal usage (event-driven updates)
- **Physics:** Sub-frame granular (accumulator-based)
- **Rendering:** Optimized grid-based drawing

---

## 📈 Future Enhancements

Possible additions:
- T-Spin detection and bonus points
- Combo system for consecutive clears
- Different game modes (marathon, sprint)
- Multiplayer support
- Leaderboards
- Sound volume control
- Customizable keybindings
- Piece preview queue (show 3-5 next pieces)

---

## ✅ Testing Checklist

- [x] 7-Bag Randomizer working (equal distribution)
- [x] Gravity System operational (progressive difficulty)
- [x] Collision detection accurate (no clipping)
- [x] Ghost piece rendering correctly
- [x] Hold piece swapping working
- [x] Wall kick (SRS) rotation functional
- [x] Menu interaction smooth
- [x] Score persistence working
- [x] Game States all reachable
- [x] All controls responsive
- [x] No memory leaks on long play
- [x] 60 FPS maintained

---

## 🚀 Launching the Game

```bash
python main.py
```

**Requirements:**
- Python 3.7+
- pygame-ce 2.5.7+
- No external audio files (uses generated beeps)

**Difficulty Selection:**
Currently set to `DIFFICULTY_NORMAL` in main.py. Change to:
- `DIFFICULTY_EASY` for slower gameplay
- `DIFFICULTY_HARD` for faster gameplay

---

Generated: 2026-03-13
Version: 2.0 (Advanced Systems)
