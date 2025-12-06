# Serial Killer - Professional Fighting Game

A professionally structured 2D fighting game built with Python and Pygame, featuring player vs AI combat mechanics.

## 📁 Project Structure

```
Serial_Killer/
├── config.py                          # Global game configuration
├── main.py                            # Game entry point
├── requirements.txt                   # Python dependencies
├── README.md                          # Project documentation
│
├── src/                               # Main source code
│   ├── __init__.py
│   ├── core/                          # Core game systems
│   │   ├── __init__.py
│   │   ├── game.py                    # Main game engine and loop
│   │   └── game_state.py              # Game state management
│   │
│   ├── entities/                      # Game entity classes
│   │   ├── __init__.py
│   │   ├── character.py               # Base Character class
│   │   ├── main_character.py          # Player character (Scorpion)
│   │   └── villain.py                 # Enemy character (Sonya)
│   │
│   ├── systems/                       # Game systems
│   │   ├── __init__.py
│   │   └── collision_handler.py       # Collision detection
│   │
│   └── utils/                         # Utility modules
│       ├── __init__.py
│       └── sprite_utils.py            # Sprite loading and manipulation
│
├── assets/                            # Game assets
│   ├── sprites/                       # Sprite sheets
│   │   ├── Scorpian/                  # Player sprites
│   │   └── sonya/                     # Villain sprites
│   ├── audio/                         # Sound files
│   └── backgrounds/                   # Background images
│
└── tests/                             # Unit tests
    └── test_*.py                      # Test files
```

## ✨ Key Improvements Made

### 1. **Professional Folder Structure**
   - Organized code into logical modules (core, entities, systems, utils)
   - Separated concerns following MVC pattern
   - Asset management in dedicated directories

### 2. **Code Best Practices**
   - **Type Hints**: Full type annotations for better IDE support
   - **Docstrings**: Comprehensive documentation using Google/NumPy style
   - **Error Handling**: Proper exception handling and validation
   - **Code Comments**: Clear explanations of complex logic

### 3. **Object-Oriented Design**
   - **Base Classes**: Abstract `Character` class for code reuse
   - **Inheritance**: Proper use of inheritance (MainCharacter, Villain extend Character)
   - **Encapsulation**: Private methods prefixed with `_`
   - **Single Responsibility**: Each class has one primary purpose

### 4. **Configuration Management**
   - Centralized `config.py` for all constants
   - Enums for game states and character actions
   - Easy to modify settings without touching game code

### 5. **Game State Management**
   - Dedicated `GameStateManager` class
   - Clear state transitions
   - Type-safe enum-based states

### 6. **Collision System**
   - Improved collision handler with better documentation
   - Collision cooldown to prevent rapid-fire hits
   - Type hints and cleaner method organization

### 7. **Sprite System**
   - `SpriteSheet` class for efficient sprite loading
   - Reduced code duplication
   - Better error handling for missing assets
   - Batch frame extraction methods

### 8. **Main Game Engine**
   - Centralized `Game` class managing the game loop
   - Clean separation of concerns (handle_events, update, render)
   - Debug information display
   - Proper resource cleanup

## 🎮 Game Features

### Player Controls
- **Left/Right Arrows**: Move character
- **Z**: Punch
- **X**: Double Punch
- **C**: Kick

### Game Mechanics
- **Combat System**: Multiple attack types (punch, double punch, kick)
- **AI Opponent**: Random behavior based on distance to player
- **Collision Detection**: Attack hit detection with cooldown
- **Animation System**: Smooth sprite animation for all actions
- **Game States**: Turn-based combat state management

## 🚀 Getting Started

### Prerequisites
```bash
python 3.8+
pygame
```

### Installation
```bash
# Clone the repository
git clone <repo-url>
cd Serial_Killer

# Install dependencies
pip install -r requirements.txt
```

### Running the Game
```bash
python main.py
```

## 📚 Architecture Patterns Used

### 1. **Model-View-Controller (MVC)**
   - Model: Character classes, GameState
   - View: Rendering system
   - Controller: Game class managing logic

### 2. **State Pattern**
   - GameStateManager handles state transitions
   - Clear state flow for combat mechanics

### 3. **Strategy Pattern**
   - Different character behaviors (player vs AI)
   - Pluggable collision handler

### 4. **Singleton Pattern**
   - Game instance manages all global state

## 🔧 Configuration

Edit `config.py` to customize:
- Screen resolution
- FPS (frames per second)
- Game title
- Character spawn positions
- Animation speeds
- Collision cooldown

Example:
```python
# Game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 30

# Character positions
PLAYER_START_X = 100
ENEMY_START_X = 600
```

## 📝 Code Examples

### Creating a Character
```python
from src.entities.main_character import MainCharacter

player = MainCharacter(x=100, y=300)
player.punch(target_x=600)
player.update_frame(target_x=600)
player.draw(screen)
```

### Game Loop Integration
```python
from src.core.game import Game

game = Game(width=800, height=600)
game.run()
```

### Collision Detection
```python
from src.systems.collision_handler import CollisionHandler

collision_handler = CollisionHandler(collision_cooldown=500)
collision_handler.update(player, villain)
```

## 🎯 Best Practices Implemented

✅ DRY (Don't Repeat Yourself) - Reusable base classes
✅ SOLID Principles - Single responsibility, Open/closed, etc.
✅ Clean Code - Meaningful names, small functions
✅ Type Safety - Full type hints throughout
✅ Documentation - Comprehensive docstrings
✅ Error Handling - Proper exception management
✅ Code Organization - Logical module structure
✅ Configuration Management - Centralized settings
✅ Performance - Efficient sprite subsurface usage
✅ Maintainability - Easy to extend and modify

## 🔄 Extending the Game

### Adding a New Enemy Type
```python
from src.entities.character import Character

class BossCharacter(Character):
    def __init__(self, x, y):
        super().__init__(x, y)
        # Custom initialization
    
    def update_frame(self, target_x):
        # Custom animation logic
        pass
    
    def draw(self, screen):
        # Custom rendering
        pass
```

### Adding New Game States
```python
# In config.py
class GameStateEnum(Enum):
    PAUSE = "pause"
    GAME_OVER = "game_over"
    # ... existing states
```

## 📦 Dependencies
- **pygame**: Game rendering and input handling

## 🐛 Debugging

Enable debug info by uncommenting in `src/core/game.py`:
```python
def _draw_debug_info(self):
    # Shows player action, villain action, and game state
```

## 📄 License
[Add your license here]

## 👥 Contributors
[Add contributor information]

## 🎓 Learning Resources

This codebase demonstrates:
- Object-oriented design patterns
- Game development architecture
- Professional Python practices
- Type hints and documentation
- Error handling
- State management
- Collision detection
- Animation systems

Perfect for learning professional game development practices!

---

**Last Updated**: December 2025
**Version**: 1.0.0
