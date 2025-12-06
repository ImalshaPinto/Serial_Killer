# Quick Start Guide

## Installation & Running

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Game
```bash
python main.py
```

## Controls

| Key | Action |
|-----|--------|
| ← / → | Move Left / Right |
| Z | Punch |
| X | Double Punch |
| C | Kick |
| ALT+F4 | Quit Game |

## Game Basics

- **Objective**: Defeat the AI opponent (Sonya) using punch and kick combos
- **Combat**: When you attack and connect with the villain, they get knocked back
- **AI**: The villain will randomly approach and attack
- **Distance**: Stay within range to land hits

## Tips for Playing

1. **Master Combos**: Mix punches and kicks for better effectiveness
2. **Spacing**: Control distance to land attacks before opponent reacts
3. **Timing**: Wait for the right moment to attack when close to enemy
4. **Evasion**: Move away after attacking to avoid counterattacks

## Configuration

Edit `config.py` to customize:

```python
# Game window size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Game speed
FPS = 30

# Character positions
PLAYER_START_X = 100
ENEMY_START_X = 600

# Collision settings
COLLISION_COOLDOWN = 500  # milliseconds between hits

# Animation speeds (lower = faster)
DEFAULT_FRAME_RATE = 8
FAST_FRAME_RATE = 5
```

## Troubleshooting

### "Cannot find sprite files"
- Ensure sprite folders (Scorpian/, sonya/) are in the game directory
- Check file names match exactly (case-sensitive on Linux)

### "pygame not found"
```bash
pip install pygame
```

### Game runs too slow/fast
- Adjust FPS in config.py
- Check if background processes are consuming CPU

### Game closes immediately
- Check console for error messages
- Ensure all sprite files exist
- Verify Python version is 3.8+

## Project Structure Quick Reference

```
src/
├── core/
│   ├── game.py          ← Main game loop and logic
│   └── game_state.py    ← State management
├── entities/
│   ├── character.py     ← Base character class
│   ├── main_character.py ← Player (Scorpion)
│   └── villain.py       ← Enemy (Sonya)
├── systems/
│   └── collision_handler.py ← Hit detection
└── utils/
    └── sprite_utils.py  ← Sprite loading

config.py        ← Game settings
main.py          ← Entry point
```

## Next Steps

1. **Learn the Code**: Read README.md and REFACTORING_GUIDE.md
2. **Modify Settings**: Edit config.py to customize gameplay
3. **Add Features**: Extend the classes to add new characters or moves
4. **Optimize**: Profile and improve performance as needed

Enjoy the game! 🎮
