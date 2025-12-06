"""
Main entry point for the Serial Killer Fighting Game.

This script initializes and runs the game.
"""

import sys
import os

# Add the project root to the path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.core.game import Game


def main():
    """
    Main entry point for the game.
    
    Initializes and runs the game engine.
    """
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"Error starting game: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
