import pygame
import random
from sprite_utils import get_frame_Walking, get_frame_Stance, get_frame_Hit, get_frame_FallingDown, get_frame_GetUp

# Initialize pygame
pygame.init()

# Load the sprite sheets
sprite_sheet = pygame.image.load('sonya/Swalking.png')
stance_sheet = pygame.image.load('sonya/stance1.png')
hit_sheet = pygame.image.load('sonya/smallhit.png')
falling_down_sheet = pygame.image.load('sonya/falingdown.png')
getup_sheet = pygame.image.load('sonya/getup.png')

class Villain:
    SPRITE_WIDTH_WALKING, SPRITE_HEIGHT_WALKING = 135, 290
    SPRITE_WIDTH_STANCE, SPRITE_HEIGHT_STANCE = 133, 290
    SPRITE_WIDTH_HIT, SPRITE_HEIGHT_HIT = 133, 290
    SPRITE_WIDTH_FALLINGDOWN, SPRITE_HEIGHT_FALLINGDOWN = 195, 290
    SPRITE_WIDTH_GETUP, SPRITE_HEIGHT_GETUP = 145, 290

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x_change = 0
        self.current_frame = get_frame_Walking(sprite_sheet, 0, 0, self.SPRITE_WIDTH_WALKING, self.SPRITE_HEIGHT_WALKING)
        self.frame_index = 0
        self.frame_counter = 0
        self.is_hit = False
        self.is_falling_down = False
        self.is_getting_up = False
        self.state = "IDLE"  # FSM State
        
        # Load walking frames
        self.walking_right = [get_frame_Walking(sprite_sheet, 0, i, self.SPRITE_WIDTH_WALKING, self.SPRITE_HEIGHT_WALKING) for i in range(9)]
        self.walking_left = [get_frame_Walking(sprite_sheet, 1, i, self.SPRITE_WIDTH_WALKING, self.SPRITE_HEIGHT_WALKING) for i in range(9)]
        self.walking_right = [frame for frame in self.walking_right if frame is not None]
        self.walking_left = [frame for frame in self.walking_left if frame is not None]

        # Load stance frames
        self.stance_left = [get_frame_Stance(stance_sheet, 0, i, self.SPRITE_WIDTH_STANCE, self.SPRITE_HEIGHT_STANCE) for i in range(7)]
        self.stance_right = [get_frame_Stance(stance_sheet, 1, i, self.SPRITE_WIDTH_STANCE, self.SPRITE_HEIGHT_STANCE) for i in range(7)]
        self.stance_left = [frame for frame in self.stance_left if frame is not None]
        self.stance_right = [frame for frame in self.stance_right if frame is not None]

        # Load hit frames
        self.hit_left = [get_frame_Hit(hit_sheet, 0, i, self.SPRITE_WIDTH_HIT, self.SPRITE_HEIGHT_HIT) for i in range(3)]
        self.hit_right = [get_frame_Hit(hit_sheet, 1, i, self.SPRITE_WIDTH_HIT, self.SPRITE_HEIGHT_HIT) for i in range(3)]
        self.hit_left = [frame for frame in self.hit_left if frame is not None]
        self.hit_right = [frame for frame in self.hit_right if frame is not None]

        # Load falling down frames
        self.falling_down_left = [get_frame_FallingDown(falling_down_sheet, 1, i, self.SPRITE_WIDTH_FALLINGDOWN, self.SPRITE_HEIGHT_FALLINGDOWN) for i in range(7)]
        self.falling_down_right = [get_frame_FallingDown(falling_down_sheet, 0, i, self.SPRITE_WIDTH_FALLINGDOWN, self.SPRITE_HEIGHT_FALLINGDOWN) for i in range(7)]
        self.falling_down_left = [frame for frame in self.falling_down_left if frame is not None]
        self.falling_down_right = [frame for frame in self.falling_down_right if frame is not None]

        # Load get up frames
        self.get_up_left = [get_frame_GetUp(getup_sheet, 1, i, self.SPRITE_WIDTH_GETUP, self.SPRITE_HEIGHT_GETUP) for i in range(2)]
        self.get_up_right = [get_frame_GetUp(getup_sheet, 0, i, self.SPRITE_WIDTH_GETUP, self.SPRITE_HEIGHT_GETUP) for i in range(2)]
        self.get_up_left = [frame for frame in self.get_up_left if frame is not None]
        self.get_up_right = [frame for frame in self.get_up_right if frame is not None]
        
    def update_position(self, target_x):
        if self.state == "WALK":
            if self.x < target_x - 10:
                self.x_change = 1
            elif self.x > target_x + 100:
                self.x_change = -1
            else:
                self.x_change = 0
            self.x += self.x_change

    def update_frame_right(self):
        self.frame_counter += 1
        if self.state == "WALK" and self.x_change != 0:
            if self.frame_counter % 6 == 0:
                self.frame_index = (self.frame_index + 1) % len(self.walking_right)
            self.current_frame = self.walking_right[min(self.frame_index, len(self.walking_right) - 1)]
        else:
            if self.frame_counter % 6 == 0:
                self.frame_index = (self.frame_index + 1) % len(self.stance_right)
            self.current_frame = self.stance_right[min(self.frame_index, len(self.stance_right) - 1)]

    def update_frame_left(self):
        self.frame_counter += 1
        if self.state == "WALK" and self.x_change != 0:
            if self.frame_counter % 6 == 0:
                self.frame_index = (self.frame_index + 1) % len(self.walking_left)
            self.current_frame = self.walking_left[min(self.frame_index, len(self.walking_left) - 1)]
        else:
            if self.frame_counter % 6 == 0:
                self.frame_index = (self.frame_index + 1) % len(self.stance_left)
            self.current_frame = self.stance_left[min(self.frame_index, len(self.stance_left) - 1)]

    def update_frame_hit(self, target_x):
        self.frame_counter += 1
        if self.frame_counter % 6 == 0:
            self.frame_index = (self.frame_index + 1) % len(self.hit_left)
            if self.frame_index == 0:
                self.is_hit = False
                self.state = "IDLE"
        if self.x < target_x:
            self.current_frame = self.hit_left[min(self.frame_index, len(self.hit_left) - 1)]
        else:
            self.current_frame = self.hit_right[min(self.frame_index, len(self.hit_right) - 1)]

    def update_frame_falling_down(self, target_x):
        self.frame_counter += 1
        if self.frame_counter % 6 == 0:
            if self.frame_index < 6:
                self.frame_index += 1
            else:
                self.is_falling_down = False
                self.state = "HOLD_FALLING_DOWN"
                # Set a timer event to hold the last frame of the falling down animation for 1000ms
                pygame.time.set_timer(pygame.USEREVENT + 2, 1000)
        if self.x < target_x:
            self.current_frame = self.falling_down_left[min(self.frame_index, len(self.falling_down_left) - 1)]
        else:
            self.current_frame = self.falling_down_right[min(self.frame_index, len(self.falling_down_right) - 1)]

    def update_frame(self, target_x):
        if self.is_falling_down:
            self.update_frame_falling_down(target_x)
        elif self.state == "HOLD_FALLING_DOWN":
            # Do nothing, just hold the last frame
            pass
        elif self.is_getting_up:
            self.update_frame_get_up(target_x)
        elif self.is_hit:
            self.update_frame_hit(target_x)
        elif self.state == "WALK":
            if self.x < target_x:
                self.update_frame_left()
            else:
                self.update_frame_right()
        else:
            if self.x < target_x:
                self.update_frame_left()
            else:
                self.update_frame_right()

    def draw(self, screen):
        screen.blit(self.current_frame, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.SPRITE_WIDTH_WALKING, self.SPRITE_HEIGHT_WALKING)

    def check_collision(self, player_rect):
        villain_rect = self.get_rect()
        return villain_rect.colliderect(player_rect)

    def random_behavior(self):
        """Randomly switch between states."""
        self.state = random.choice(["IDLE", "WALK"])

# Set a timer event to change behavior every 1 seconds
pygame.time.set_timer(pygame.USEREVENT + 1, 1000)