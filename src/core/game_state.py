"""
Game state management module.

This module handles the state transitions and logic for the fighting game.
"""

from enum import Enum
from typing import Tuple


class GameState(Enum):
    """Enumeration for game states."""
    IDLE = "idle"
    VILLAIN_ATTACKING = "villain_attacking"
    CHARACTER_REACTING = "character_reacting"
    VILLAIN_RECOVERING = "villain_recovering"


class GameStateManager:
    """
    Manages game state transitions and logic.
    
    Attributes:
        current_state (GameState): The current game state.
        villain_hit_first (bool): Flag indicating if villain attacked first.
        character_hit_first (bool): Flag indicating if character attacked first.
    """
    
    def __init__(self):
        """Initialize the game state manager."""
        self.current_state = GameState.IDLE
        self.villain_hit_first = False
        self.character_hit_first = False
    
    def update(self, main_character, villain) -> Tuple[GameState, bool, bool]:
        """
        Update game state based on character states.
        
        Args:
            main_character: The main character entity.
            villain: The villain entity.
            
        Returns:
            Tuple[GameState, bool, bool]: Updated state, character_hit_first, villain_hit_first.
        """
        return self.handle_game_state(
            self.current_state,
            main_character,
            villain,
            self.villain_hit_first,
            self.character_hit_first
        )
    
    def handle_game_state(
        self,
        game_state: GameState,
        main_character,
        villain,
        villain_hit_first: bool,
        character_hit_first: bool
    ) -> Tuple[GameState, bool, bool]:
        """
        Handle state transitions based on attack and defense status.
        
        Args:
            game_state (GameState): Current game state.
            main_character: The main character entity.
            villain: The villain entity.
            villain_hit_first (bool): Whether villain attacked first.
            character_hit_first (bool): Whether character attacked first.
            
        Returns:
            Tuple: New state and hit flags.
        """
        if villain_hit_first:
            return self._handle_villain_attacked_first(
                game_state, main_character, villain, villain_hit_first
            )
        elif character_hit_first:
            return self._handle_character_attacked_first(
                game_state, main_character, villain, character_hit_first
            )
        
        return game_state, character_hit_first, villain_hit_first
    
    def _handle_villain_attacked_first(
        self,
        game_state: GameState,
        main_character,
        villain,
        villain_hit_first: bool
    ) -> Tuple[GameState, bool, bool]:
        """
        Handle state transitions when villain attacks first.
        
        Args:
            game_state (GameState): Current game state.
            main_character: The main character entity.
            villain: The villain entity.
            villain_hit_first (bool): Flag from previous state.
            
        Returns:
            Tuple: New state and hit flags.
        """
        if game_state == GameState.VILLAIN_ATTACKING:
            villain.update_frame(main_character.x)
            if (villain.frame_index == 0 and 
                not villain.is_double_punching and 
                not villain.is_kicking):
                return GameState.CHARACTER_REACTING, False, villain_hit_first
        
        elif game_state == GameState.CHARACTER_REACTING:
            main_character.update_frame(villain.x)
            if (main_character.frame_index == 0 and 
                not main_character.is_hit and 
                not main_character.is_falling):
                return GameState.VILLAIN_RECOVERING, False, villain_hit_first
        
        elif game_state == GameState.VILLAIN_RECOVERING:
            return GameState.IDLE, False, villain_hit_first
        
        return game_state, False, villain_hit_first
    
    def _handle_character_attacked_first(
        self,
        game_state: GameState,
        main_character,
        villain,
        character_hit_first: bool
    ) -> Tuple[GameState, bool, bool]:
        """
        Handle state transitions when character attacks first.
        
        Args:
            game_state (GameState): Current game state.
            main_character: The main character entity.
            villain: The villain entity.
            character_hit_first (bool): Flag from previous state.
            
        Returns:
            Tuple: New state and hit flags.
        """
        if game_state == GameState.CHARACTER_REACTING:
            main_character.update_frame(villain.x)
            if (main_character.frame_index == 0 and 
                not main_character.is_hit and 
                not main_character.is_falling):
                return GameState.VILLAIN_RECOVERING, character_hit_first, False
        
        elif game_state == GameState.VILLAIN_RECOVERING:
            villain.update_frame(main_character.x)
            if (villain.frame_index == 0 and 
                not villain.is_double_punching and 
                not villain.is_kicking):
                return GameState.IDLE, character_hit_first, False
        
        return game_state, character_hit_first, False
    
    def set_villain_attacked_first(self):
        """Set flag indicating villain attacked first."""
        self.villain_hit_first = True
        self.character_hit_first = False
        self.current_state = GameState.VILLAIN_ATTACKING
    
    def set_character_attacked_first(self):
        """Set flag indicating character attacked first."""
        self.character_hit_first = True
        self.villain_hit_first = False
        self.current_state = GameState.CHARACTER_REACTING
    
    def reset(self):
        """Reset game state to idle."""
        self.current_state = GameState.IDLE
        self.villain_hit_first = False
        self.character_hit_first = False
