import pygame
from main_character import MainCharacter
from vilan import Villain
from sprite_utils import BattleState

def handle_game_state(game_state, main_character, villain, villain_hit_first, character_hit_first):
    if villain_hit_first:
        if game_state == BattleState.VILLAIN_ATTACKING:
            villain.update_frame(main_character.x)
            if villain.frame_index == 0 and not villain.is_double_punching and not villain.is_kicking:
                return BattleState.CHARACTER_REACTING, False, villain_hit_first
        elif game_state == BattleState.CHARACTER_REACTING:
            main_character.update_frame(villain.x)
            if main_character.frame_index == 0 and not main_character.is_hit and not main_character.is_falling:
                return BattleState.VILLAIN_RECOVERING, False, villain_hit_first
        elif game_state == BattleState.VILLAIN_RECOVERING:
            return BattleState.IDLE, False, villain_hit_first
    elif character_hit_first:
        if game_state == BattleState.CHARACTER_REACTING:
            main_character.update_frame(villain.x)
            if main_character.frame_index == 0 and not main_character.is_hit and not main_character.is_falling:
                return BattleState.VILLAIN_RECOVERING, character_hit_first, False
        elif game_state == BattleState.VILLAIN_RECOVERING:
            villain.update_frame(main_character.x)
            if villain.frame_index == 0 and not villain.is_double_punching and not villain.is_kicking:
                return BattleState.IDLE, character_hit_first, False
    return game_state, character_hit_first, villain_hit_first

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    main_character = MainCharacter(100, 300)
    villain = Villain(600, 300)

    # Flags to determine who hits first
    villain_hit_first = False
    character_hit_first = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.USEREVENT + 1:
                villain.random_behavior(main_character.x)

        # Check for collisions
        if villain.get_rect().colliderect(main_character.get_rect()):
            if not villain_hit_first and not character_hit_first:
                # Determine who hits first based on their states
                if villain.is_double_punching or villain.is_kicking:
                    villain_hit_first = True
                elif main_character.is_punching or main_character.is_kicking:
                    character_hit_first = True

        # Handle game states based on who hit first
        game_state, character_hit_first, villain_hit_first = handle_game_state(
            game_state, main_character, villain, villain_hit_first, character_hit_first
        )

        # Update positions and draw everything
        main_character.update_position()
        villain.update_position(main_character.x)

        screen.fill((0, 0, 0))
        main_character.draw(screen)
        villain.draw(screen)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
