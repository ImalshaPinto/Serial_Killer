"""
Configuration module for Serial Killer Fighting Game.

This module contains all game constants, paths, and settings.
"""

import os
from enum import Enum

# ===== Screen Configuration =====
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 30
BACKGROUND_COLOR = (0, 0, 0)

# ===== Game Constants =====
GAME_TITLE = "Serial Killer - Fighting Game"

# ===== Asset Paths =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
SPRITES_DIR = os.path.join(ASSETS_DIR, "sprites")

# Background image path
BACKGROUND_IMAGE = os.path.join(ASSETS_DIR, "palacegrounds.png")

# Character sprite paths
SCORPION_SPRITES_DIR = os.path.join(SPRITES_DIR, "Scorpian")
SONYA_SPRITES_DIR = os.path.join(SPRITES_DIR, "sonya")

# ===== Collision Detection =====
COLLISION_COOLDOWN = 500  # milliseconds

# ===== Animation Speeds =====
DEFAULT_FRAME_RATE = 8
SLOW_FRAME_RATE = 12
FAST_FRAME_RATE = 5
WALK_FRAME_RATE = 6


class GameStateEnum(Enum):
    """Enumeration for game states."""
    IDLE = "idle"
    VILLAIN_ATTACKING = "villain_attacking"
    CHARACTER_REACTING = "character_reacting"
    VILLAIN_RECOVERING = "villain_recovering"


class CharacterActionEnum(Enum):
    """Enumeration for character actions."""
    IDLE = "idle"
    WALKING = "walking"
    RUNNING = "running"
    JUMPING = "jumping"
    DUCKING = "ducking"
    PUNCHING = "punching"
    DOUBLE_PUNCHING = "double_punching"
    KICKING = "kicking"
    HIT = "hit"
    FALLING = "falling"
    GETTING_UP = "getting_up"


class DirectionEnum(Enum):
    """Enumeration for character direction."""
    LEFT = "left"
    RIGHT = "right"


# ===== Character Spawn Positions =====
PLAYER_START_X = 100
PLAYER_START_Y = 300

ENEMY_START_X = 600
ENEMY_START_Y = 300
