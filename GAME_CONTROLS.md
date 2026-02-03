# Serial Killer - Game Controls & Features

## 🎮 **PLAYER CONTROLS**

### Movement
- **LEFT ARROW** - Move left
- **RIGHT ARROW** - Move right
- **UP ARROW** - Jump
- **DOWN ARROW** - Crouch

### Combat
- **D KEY (Single Press)** - Single Punch (8 damage)
- **D KEY (Double-Click)** - Double Punch (15 damage) - Uses Dpunch.png sprite
- **C KEY** - Kick (20 damage)
- **S KEY (Hold)** - Block (reduces incoming damage by 2/3)

---

## ⚙️ **PHYSICS SYSTEM**

### Gravity & Jumping
- **Gravity**: 0.8 pixels/frame acceleration
- **Jump Power**: -15 initial velocity
- **Ground Detection**: Characters automatically land on ground
- **Air Control**: Can move left/right while jumping

### Knockback
- **Punch Knockback**: ±15 pixels
- **Double Punch Knockback**: ±15 pixels
- **Kick Knockback**: ±30 pixels (more powerful)
- Direction based on relative positions

---

## 💚 **HEALTH SYSTEM**

### Health Points
- **Starting Health**: 100 HP per character
- **Health Bars**: Green bars at top of screen with character names
- **Real-time Updates**: Bars decrease as damage is taken

### Damage Values
| Attack Type | Damage | Blocked Damage |
|------------|--------|----------------|
| Single Punch | 8 HP | 3 HP |
| Double Punch | 15 HP | 5 HP |
| Kick | 20 HP | 7 HP |

---

## 🏆 **ROUND SYSTEM**

### Round Rules
- **Best of 3 Rounds**: First to win 2 rounds wins the match
- **Round Timer**: 90 seconds per round
- **Win Conditions**:
  - Reduce opponent's health to 0
  - Have more health when time expires
  - Tie = Round restarts

### Round Display
- **Round Number**: Displayed at top center
- **Win Indicators**: Gold circles below character names
  - Filled gold = Round won
  - Gray outline = Round not won yet
- **Timer**: Large yellow number in circle at top center

---

## 🎯 **GAME STATES**

### During Round
- Active combat
- Health depleting
- Timer counting down

### Between Rounds
- 2-second pause
- Characters reset to starting positions
- Health fully restored

### Game Over
- Semi-transparent black overlay
- Winner announcement (SCORPION WINS! or SONYA WINS!)
- **Press ENTER** to restart entire match

---

## 🤖 **AI BEHAVIOR**

### Villain (Sonya) AI
- Makes decisions every 1 second
- Approaches player when out of range
- Randomly attacks when in range
- Blocks incoming attacks
- Counter-attacks after being hit

---

## 🎨 **UI ELEMENTS**

### Top Bar (Left Side)
- Player health bar (green)
- "SCORPION" label
- Round win indicators (3 circles)

### Top Bar (Right Side)
- Villain health bar (green)
- "SONYA" label
- Round win indicators (3 circles)

### Top Center
- Round timer (yellow circle)
- Round number
- Current time remaining

### Game Over Screen
- Winner announcement
- Restart instructions
- Score display

---

## 🔧 **TECHNICAL DETAILS**

### Frame Rate
- 30 FPS gameplay

### Screen Size
- 800×600 pixels

### Background
- **palacegrounds.png** - Scaled to fit screen

### Character Starting Positions
- **Player (Scorpion)**: X=100, Y=300
- **Villain (Sonya)**: X=600, Y=300

---

## 🐛 **DEBUG MODE**

Uncomment line in `game.py` render method to enable:
```python
self._draw_debug_info()
```

Shows:
- Current character actions
- Health points
- Game state
- Physics info

---

## 🎯 **TIPS & STRATEGIES**

1. **Use Blocking** - Hold S when enemy attacks to reduce damage
2. **Jump Attacks** - Jump and attack for unpredictable movements  
3. **Double Punch** - Master double-clicking D for more damage
4. **Kick for Knockback** - Use kicks to create distance
5. **Watch the Timer** - Play defensively if you're ahead on health
6. **Crouch** - Dodge high attacks by pressing DOWN

---

## 🚀 **FUTURE ENHANCEMENTS** (Ready to Add)

- Special moves (combo attacks)
- Power-ups and items
- Multiple stages/backgrounds
- Character selection screen
- Difficulty levels
- Sound effects and music
- Combo counter
- Perfect round bonus

