class BattleState:
    """
    A class to represent the different states in a battle.
    These states are used to manage the flow of the game during combat.
    """
    IDLE = "idle"  # No action is being performed
    VILLAIN_ATTACKING = "villain_attacking"  # Villain is attacking the player
    CHARACTER_REACTING = "character_reacting"  # Player is reacting to the villain's attack
    VILLAIN_RECOVERING = "villain_recovering"  # Villain is recovering after an attack
