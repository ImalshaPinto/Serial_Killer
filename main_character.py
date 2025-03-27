import pygame
from sprite_utils import get_frame_Stance, get_frame_Running, get_frame_Duck_Up, get_frame_Jump_Directional, get_frame_Jump_Vertical, get_frame_Double_Punch, get_frame_Punch, get_frame_Underkick, get_frame_Kick

class BattleState:
    IDLE = "idle"
    VILLAIN_ATTACKING = "villain_attacking"
    CHARACTER_REACTING = "character_reacting"
    VILLAIN_RECOVERING = "villain_recovering"

game_state = BattleState.IDLE
villain_attack_done = False  # Flag to indicate if the villain's attack is done
character_react_done = False  # Flag to indicate if the character's reaction is done

# Load the sprite sheets
sprite_sheet = pygame.image.load('Scorpian/Sstance1.png')
sprite_sheet2 = pygame.image.load('Scorpian/Srunning.png')
sprite_sheet3 = pygame.image.load('Scorpian/duck&up.png')
sprite_sheet4 = pygame.image.load('Scorpian/jumpfront3.png')
sprite_sheet5 = pygame.image.load('Scorpian/jump.png')
sprite_sheet6 = pygame.image.load('Scorpian/Dpunch.png')
sprite_sheet7 = pygame.image.load('Scorpian/punch.png')
sprite_sheet8 = pygame.image.load('Scorpian/bBkick.png')
sprite_sheet9 = pygame.image.load('Scorpian/Undkick.png')
# Load hit and fall animations
small_hit = pygame.image.load('Scorpian/smallhit.png')
falling = pygame.image.load('Scorpian/falling1.png')

class Villain:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.current_frame = None
        self.frame_index = 0
        self.frame_counter = 0

    def random_behavior(self, target_x):
        # Implement random behavior logic here
        pass

    def update_frame(self, target_x):
        # Implement frame update logic here
        pass

    def update_position(self, target_x):
        # Implement position update logic here
        pass

    def draw(self, screen):
        # Implement draw logic here
        pass

class MainCharacter:
    SPRITE_WIDTH, SPRITE_HEIGHT = 167, 290  # Width and height of the character sprite
    SPRITE_WIDTH_STANCE, SPRITE_HEIGHT_STANCE = 133, 290  # Width and height of the stance sprite
    SPRITE_WIDTH_RUNNING, SPRITE_HEIGHT_RUNNING = 132, 300  # Width and height of the running sprite
    SPRITE_WIDTH_DUCK, SPRITE_HEIGHT_DUCK = 132, 290  # Width and height of the duck sprite
    SPRITE_WIDTH_UP, SPRITE_HEIGHT_UP = 132, 290  # Width and height of the up sprite
    SPRITE_WIDTH_JUMP_DIRECTIONAL, SPRITE_HEIGHT_JUMP_DIRECTIONAL = 132, 290  # Width and height of the directional jump sprite
    SPRITE_WIDTH_JUMP_VERTICAL, SPRITE_HEIGHT_JUMP_VERTICAL = 132, 290  # Width and height of the vertical jump sprite
    SPRITE_WIDTH_DOUBLE_PUNCH, SPRITE_HEIGHT_DOUBLE_PUNCH = 183, 290  # Width and height of the double punch sprite
    SPRITE_WIDTH_PUNCH, SPRITE_HEIGHT_PUNCH = 183, 290  # Width and height of the punch sprite
    SPRITE_WIDTH_KICK, SPRITE_HEIGHT_KICK = 185, 290  # Width and height of the kick sprite
    SPRITE_WIDTH_UNDERKICK, SPRITE_HEIGHT_UNDERKICK = 185, 290  # Width and height of the underkick sprite
    SPRITE_WIDTH_SMALLHIT, SPRITE_HEIGHT_SMALLHIT  = 183, 290  # Width and height of the double punch sprite
    SPRITE_WIDTH_FALL, SPRITE_HEIGHT_FALL = 183, 290  # Width and height of the fall sprite
    def __init__(self, x, y):
        self.x = x  # Character's x position
        self.y = y  # Character's y position
        self.x_change = 0  # Change in x position (for movement)
        self.is_ducking = False  # Flag to check if the character is ducking
        self.is_getting_up = False  # Flag to check if the character is getting up
        self.is_jumping_directional = False  # Flag to check if the character is performing a directional jump
        self.is_jumping_vertical = False  # Flag to check if the character is performing a vertical jump
        self.is_double_punching = False  # Flag to check if the character is performing a double punch
        self.is_punching = False  # Flag to check if the character is performing a punch
        self.is_kicking = False  # Flag to check if the character is performing a kick
        self.is_und_kicking = False  # Flag to check if the character is performing an underkick
        self.is_hit = False  # Flag to check if the character is hit
        self.is_falling = False  # Flag to check if the character is falling
        self.current_frame = get_frame_Stance(sprite_sheet, 0, 0, self.SPRITE_WIDTH, self.SPRITE_HEIGHT)  # Initial frame
        self.frame_index = 0  # Index of the current frame
        self.frame_counter = 0  # Counter for frame updates
        self.last_a_press_time = 0  # Time of the last 'A' key press
        self.last_down_press_time = 0  # Time of the last 'DOWN' key press
        self.is_movement_in_progress = False  # Flag to indicate if a movement loop is in progress
        self.current_action = None  # Flag to get the current action of the main character

        # Load stance frames
        self.stance_frames_left = [get_frame_Stance(sprite_sheet, 0, i, self.SPRITE_WIDTH_STANCE, self.SPRITE_HEIGHT_STANCE) for i in range(8)]
        self.stance_frames_right = [get_frame_Stance(sprite_sheet, 1, i, self.SPRITE_WIDTH_STANCE, self.SPRITE_HEIGHT_STANCE) for i in range(8)]
        self.stance_frames_left = [frame for frame in self.stance_frames_left if frame is not None]
        self.stance_frames_right = [frame for frame in self.stance_frames_right if frame is not None]

        # Load running frames
        self.running_frames_left = [get_frame_Running(sprite_sheet2, 1, i, self.SPRITE_WIDTH_RUNNING, self.SPRITE_HEIGHT_RUNNING) for i in range(12)]
        self.running_frames_right = [get_frame_Running(sprite_sheet2, 0, i, self.SPRITE_WIDTH_RUNNING, self.SPRITE_HEIGHT_RUNNING) for i in range(12)]
        self.running_frames_left = [frame for frame in self.running_frames_left if frame is not None]
        self.running_frames_right = [frame for frame in self.running_frames_right if frame is not None]

        # Load duck frames
        self.duck_frames_left = [get_frame_Duck_Up(sprite_sheet3, 0, i, self.SPRITE_WIDTH_DUCK, self.SPRITE_HEIGHT_DUCK) for i in range(3)]
        self.duck_frames_right = [get_frame_Duck_Up(sprite_sheet3, 1, i, self.SPRITE_WIDTH_DUCK, self.SPRITE_HEIGHT_DUCK) for i in range(3)]
        self.duck_frames_left = [frame for frame in self.duck_frames_left if frame is not None]
        self.duck_frames_right = [frame for frame in self.duck_frames_right if frame is not None]

        # Load up frames
        self.up_frames_left = [get_frame_Duck_Up(sprite_sheet3, 0, i, self.SPRITE_WIDTH_UP, self.SPRITE_HEIGHT_UP) for i in range(3)]
        self.up_frames_right = [get_frame_Duck_Up(sprite_sheet3, 1, i, self.SPRITE_WIDTH_UP, self.SPRITE_HEIGHT_UP) for i in range(3)]
        self.up_frames_left = [frame for frame in self.up_frames_left if frame is not None]
        self.up_frames_right = [frame for frame in self.up_frames_right if frame is not None]

        # Load directional jump frames
        self.jump_right_frames = [get_frame_Jump_Directional(sprite_sheet4, 0, i, self.SPRITE_WIDTH_JUMP_DIRECTIONAL, self.SPRITE_HEIGHT_JUMP_DIRECTIONAL) for i in range(9)]
        self.jump_right_frames = [frame for frame in self.jump_right_frames if frame is not None]
        self.jump_left_frames = [get_frame_Jump_Directional(sprite_sheet4, 1, i, self.SPRITE_WIDTH_JUMP_DIRECTIONAL, self.SPRITE_HEIGHT_JUMP_DIRECTIONAL) for i in range(9)]
        self.jump_left_frames = [frame for frame in self.jump_left_frames if frame is not None]

        # Load vertical jump frames
        self.jump_vertical_frames_left = [get_frame_Jump_Vertical(sprite_sheet5, 0, i, self.SPRITE_WIDTH_JUMP_VERTICAL, self.SPRITE_HEIGHT_JUMP_VERTICAL) for i in range(3)]
        self.jump_vertical_frames_right = [get_frame_Jump_Vertical(sprite_sheet5, 1, i, self.SPRITE_WIDTH_JUMP_VERTICAL, self.SPRITE_HEIGHT_JUMP_VERTICAL) for i in range(3)]
        self.jump_vertical_frames_left = [frame for frame in self.jump_vertical_frames_left if frame is not None]
        self.jump_vertical_frames_right = [frame for frame in self.jump_vertical_frames_right if frame is not None]

        # Load double punch frames
        self.double_punch_frames_left = [get_frame_Double_Punch(sprite_sheet6, 0, i, self.SPRITE_WIDTH_DOUBLE_PUNCH, self.SPRITE_HEIGHT_DOUBLE_PUNCH) for i in range(6)]
        self.double_punch_frames_right = [get_frame_Double_Punch(sprite_sheet6, 1, i, self.SPRITE_WIDTH_DOUBLE_PUNCH, self.SPRITE_HEIGHT_DOUBLE_PUNCH) for i in range(6)]
        self.double_punch_frames_left = [frame for frame in self.double_punch_frames_left if frame is not None]
        self.double_punch_frames_right = [frame for frame in self.double_punch_frames_right if frame is not None]

        # Load punch frames
        self.punch_frames_left = [get_frame_Punch(sprite_sheet7, 0, i, self.SPRITE_WIDTH_PUNCH, self.SPRITE_HEIGHT_PUNCH) for i in range(3)]
        self.punch_frames_right = [get_frame_Punch(sprite_sheet7, 1, i, self.SPRITE_WIDTH_PUNCH, self.SPRITE_HEIGHT_PUNCH) for i in range(3)]
        self.punch_frames_left = [frame for frame in self.punch_frames_left if frame is not None]
        self.punch_frames_right = [frame for frame in self.punch_frames_right if frame is not None]

        # Load kick frames
        self.kick_frames_left = [get_frame_Kick(sprite_sheet8, 0, i, self.SPRITE_WIDTH_KICK, self.SPRITE_HEIGHT_KICK) for i in range(8)]
        self.kick_frames_right = [get_frame_Kick(sprite_sheet8, 1, i, self.SPRITE_WIDTH_KICK, self.SPRITE_HEIGHT_KICK) for i in range(8)]
        self.kick_frames_left = [frame for frame in self.kick_frames_left if frame is not None]
        self.kick_frames_right = [frame for frame in self.kick_frames_right if frame is not None]

        # Load underkick frames
        self.und_kick_frames_left = [get_frame_Underkick(sprite_sheet9, 0, i, self.SPRITE_WIDTH_UNDERKICK, self.SPRITE_HEIGHT_UNDERKICK) for i in range(8)]
        self.und_kick_frames_right = [get_frame_Underkick(sprite_sheet9, 1, i, self.SPRITE_WIDTH_UNDERKICK, self.SPRITE_HEIGHT_UNDERKICK) for i in range(8)]
        self.und_kick_frames_left = [frame for frame in self.und_kick_frames_left if frame is not None]
        self.und_kick_frames_right = [frame for frame in self.und_kick_frames_right if frame is not None]

        # Load hit frames
        self.hit_frames_left = [self.get_frame(small_hit, i, 0, small_hit.get_width() // 3, small_hit.get_height() // 2) for i in range(3)]
        self.hit_frames_right = [self.get_frame(small_hit, i, 0, small_hit.get_width() // 3, small_hit.get_height() // 2) for i in range(3)]
        self.hit_frames_left = [frame for frame in self.hit_frames_left if frame is not None]
        self.hit_frames_right = [frame for frame in self.hit_frames_right if frame is not None]
        
        # Load fall frames
        self.fall_frames_left = [self.get_frame(falling, i, 0, falling.get_width() // 7, falling.get_height() // 2) for i in range(7)]
        self.fall_frames_right = [self.get_frame(falling, i, 0, falling.get_width() // 7, falling.get_height() // 2) for i in range(7)]
        self.fall_frames_left = [frame for frame in self.fall_frames_left if frame is not None]
        self.fall_frames_right = [frame for frame in self.fall_frames_right if frame is not None]

    def update_position(self):
        # Update x position
        self.x += self.x_change

        # Ensure the character stays within the screen bounds
        if self.x < 0:
            self.x = 0
        elif self.x > pygame.display.get_surface().get_width() - self.SPRITE_WIDTH:
            self.x = pygame.display.get_surface().get_width() - self.SPRITE_WIDTH

    def execute_hit_animation(self, sprite_sheet, columns, rows):
        self.hit_frames = [self.get_frame(sprite_sheet, i, j, sprite_sheet.get_width() // columns, sprite_sheet.get_height() // rows) for j in range(rows) for i in range(columns)]
        self.is_hit = True
        self.frame_index = 0

    def execute_fall_animation(self, sprite_sheet, columns, rows, direction):
        self.fall_frames = [self.get_frame(sprite_sheet, i, j, sprite_sheet.get_width() // columns, sprite_sheet.get_height() // rows) for j in range(rows) for i in range(columns)]
        self.is_falling = True
        self.frame_index = 0
        self.fall_direction = direction

    def get_frame(self, sprite_sheet, column, row, width, height):
        frame = pygame.Surface((width, height), pygame.SRCALPHA)
        frame.blit(sprite_sheet, (0, 0), (column * width, row * height, width, height))
        return frame

    def update_frame(self, target_x):
        # Update frames based on movement
        self.frame_counter += 1

        # Reset frame_index when changing animations
        if self.is_ducking:
            if not self.duck_frames_left or not self.duck_frames_right:
                return
            if self.frame_counter % 8 == 0:
                self.frame_index = (self.frame_index + 1) % len(self.duck_frames_left)
            if self.x < target_x:
                self.current_frame = self.duck_frames_left[min(self.frame_index, len(self.duck_frames_left) - 1)]
            else:
                self.current_frame = self.duck_frames_right[min(self.frame_index, len(self.duck_frames_right) - 1)]
        elif self.is_getting_up:
            if not self.up_frames_left or not self.up_frames_right:
                return
            if self.frame_counter % 8 == 0:
                self.frame_index = (self.frame_index + 1) % len(self.up_frames_left)
                if self.frame_index == 0:
                    self.is_getting_up = False  # Stop getting up after one loop
            if self.x < target_x:
                self.current_frame = self.up_frames_left[min(self.frame_index, len(self.up_frames_left) - 1)]
            else:
                self.current_frame = self.up_frames_right[min(self.frame_index, len(self.up_frames_right) - 1)]
        elif self.is_jumping_directional:
            if not self.jump_right_frames or not self.jump_left_frames:
                return
            if self.frame_counter % 6 == 0:
                self.frame_index = (self.frame_index + 1) % len(self.jump_right_frames)
                if self.frame_index == 0:
                    self.is_jumping_directional = False  # Stop jumping after one loop
                    self.is_movement_in_progress = False  # Movement loop finished
            if self.x_change >= 0:
                self.current_frame = self.jump_right_frames[min(self.frame_index, len(self.jump_right_frames) - 1)]
            else:
                self.current_frame = self.jump_left_frames[min(self.frame_index, len(self.jump_left_frames) - 1)]
              # Play jump sound at the start of the jump
               
        elif self.is_jumping_vertical:
            if not self.jump_vertical_frames_left or not self.jump_vertical_frames_right:
                return
            if self.frame_counter % 12 == 0:
                self.frame_index = (self.frame_index + 1) % len(self.jump_vertical_frames_left)
                if self.frame_index == 0:
                    self.is_jumping_vertical = False  # Stop jumping after one loop
                    self.is_movement_in_progress = False  # Movement loop finished
            if self.x < target_x:
                self.current_frame = self.jump_vertical_frames_left[min(self.frame_index, len(self.jump_vertical_frames_left) - 1)]
            else:
                self.current_frame = self.jump_vertical_frames_right[min(self.frame_index, len(self.jump_vertical_frames_right) - 1)]
             # Play jump sound at the start of the jump
               
        elif self.is_double_punching:
            if not self.double_punch_frames_left or not self.double_punch_frames_right:
                return
            if self.frame_counter % 8 == 0:
                self.frame_index = (self.frame_index + 1) % len(self.double_punch_frames_left)
                if self.frame_index == 0:
                    self.is_double_punching = False  # Stop double punching after one loop
                    self.is_movement_in_progress = False  # Movement loop finished
            if self.x < target_x:
                self.current_frame = self.double_punch_frames_left[min(self.frame_index, len(self.double_punch_frames_left) - 1)]
            else:
                self.current_frame = self.double_punch_frames_right[min(self.frame_index, len(self.double_punch_frames_right) - 1)]
        elif self.is_punching:
            if not self.punch_frames_left or not self.punch_frames_right:
                return
            if self.frame_counter % 8 == 0:
                self.frame_index = (self.frame_index + 1) % len(self.punch_frames_left)
                if self.frame_index == 0:
                    self.is_punching = False  # Stop punching after one loop
                    self.is_movement_in_progress = False  # Movement loop finished
            if self.x < target_x:
                self.current_frame = self.punch_frames_left[min(self.frame_index, len(self.punch_frames_left) - 1)]
            else:
                self.current_frame = self.punch_frames_right[min(self.frame_index, len(self.punch_frames_right) - 1)]
        elif self.is_kicking:
            if not self.kick_frames_left or not self.kick_frames_right:
                return
            if self.frame_counter % 5 == 0:
                self.frame_index = (self.frame_index + 1) % len(self.kick_frames_left)
                if self.frame_index == 0:
                    self.is_kicking = False  # Stop kicking after one loop
                    self.is_movement_in_progress = False  # Movement loop finished
            if self.x < target_x:
                self.current_frame = self.kick_frames_left[min(self.frame_index, len(self.kick_frames_left) - 1)]
            else:
                self.current_frame = self.kick_frames_right[min(self.frame_index, len(self.kick_frames_right) - 1)]
        elif self.is_und_kicking:
            if not self.und_kick_frames_left or not self.und_kick_frames_right:
                return
            if self.frame_counter % 5 == 0:
                self.frame_index = (self.frame_index + 1) % len(self.und_kick_frames_left)
                if self.frame_index == 0:
                    self.is_und_kicking = False  # Stop underkicking after one loop
                    self.is_movement_in_progress = False  # Movement loop finished
            if self.x < target_x:
                self.current_frame = self.und_kick_frames_left[min(self.frame_index, len(self.und_kick_frames_left) - 1)]
            else:
                self.current_frame = self.und_kick_frames_right[min(self.frame_index, len(self.und_kick_frames_right) - 1)]
        elif self.is_hit:
            if self.frame_counter % 8 == 0:
                self.frame_index = (self.frame_index + 1) % len(self.hit_frames)
                if self.frame_index == 0:
                    self.is_hit = False  # Stop hit animation after one loop
            self.current_frame = self.hit_frames[self.frame_index]
        elif self.is_falling:
            if self.frame_counter % 8 == 0:
                self.frame_index = (self.frame_index + 1) % len(self.fall_frames)
                if self.frame_index == 0:
                    self.is_falling = False  # Stop fall animation after one loop
            self.current_frame = self.fall_frames[self.frame_index]
        elif self.x_change > 0:  # Running right
            if not self.running_frames_right:
                return
            if self.frame_counter % 7 == 0:
                self.frame_index = (self.frame_index + 1) % len(self.running_frames_right)
            self.current_frame = self.running_frames_right[min(self.frame_index, len(self.running_frames_right) - 1)]
        elif self.x_change < 0:  # Running left
            if not self.running_frames_left:
                return
            if self.frame_counter % 8 == 0:
                self.frame_index = (self.frame_index - 1) % len(self.running_frames_left)
                if self.frame_index < 0:
                    self.frame_index = len(self.running_frames_left) - 1
            self.current_frame = self.running_frames_left[min(self.frame_index, len(self.running_frames_left) - 1)]
        else:  # Stance (display the 0th frame)
            if not self.stance_frames_left or not self.stance_frames_right:
                return
            if self.frame_counter % 7 == 0:  # Adjust the modulus value to control the speed
                self.frame_index = (self.frame_index + 1) % len(self.stance_frames_left)
            if self.x < target_x:
                self.current_frame = self.stance_frames_left[min(self.frame_index, len(self.stance_frames_left) - 1)]
            else:
                self.current_frame = self.stance_frames_right[min(self.frame_index, len(self.stance_frames_right) - 1)]

    def draw(self):
        pygame.display.get_surface().blit(self.current_frame, (self.x, self.y))  # Draw the current frame on the screen

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.SPRITE_WIDTH, self.SPRITE_HEIGHT)

    def get_current_action(self):
        return self.current_action

# Main loop
def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    main_character = MainCharacter(100, 100)
    villain = Villain(400, 100)
    running = True

    # Set a timer event to change behavior every 1 second
    pygame.time.set_timer(pygame.USEREVENT + 1, 1000)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.USEREVENT + 1:
                villain.random_behavior(main_character.x)

        global villain_attack_done, character_react_done

        if game_state == BattleState.VILLAIN_ATTACKING:
            # Play villain attack animation
            villain.update_frame(main_character.x)
            # Check if the villain's attack is done
            if villain.frame_index == 0 and villain.is_double_punching == False and villain.is_kicking == False:
                villain_attack_done = True

        elif game_state == BattleState.CHARACTER_REACTING:
            # Character dodges or takes damage
            main_character.update_frame(villain.x)
            # Check if the character's reaction is done
            if main_character.frame_index == 0 and main_character.is_hit == False and main_character.is_falling == False:
                character_react_done = True

        elif game_state == BattleState.VILLAIN_RECOVERING:
            # Reset villain animation
            game_state = BattleState.IDLE  # Back to neutral

        main_character.update_position()
        villain.update_position(main_character.x)

        screen.fill((0, 0, 0))
        main_character.draw()
        villain.draw(screen)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()