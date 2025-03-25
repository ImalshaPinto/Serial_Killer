import pygame
import random
from sprite_utils import get_frame_Walking, get_frame_Stance, get_frame_Hit, get_frame_FallingDown, get_frame_GetUp, get_frame_DoublePunching, get_frame_kicking

# Initialize pygame
pygame.init()

# Load the sprite sheets
sprite_sheet = pygame.image.load('sonya/Swalking.png')
stance_sheet = pygame.image.load('sonya/stance1.png')
hit_sheet = pygame.image.load('sonya/smallhit.png')
falling_down_sheet = pygame.image.load('sonya/falingdown.png')
getup_sheet = pygame.image.load('sonya/getup.png')
double_punching_sheet = pygame.image.load('sonya/doublepunching.png')  # New sprite sheet
kicking_sheet = pygame.image.load('sonya/kick.png')  # New sprite sheet

class Villain:
    SPRITE_WIDTH_WALKING, SPRITE_HEIGHT_WALKING = 135, 290
    SPRITE_WIDTH_STANCE, SPRITE_HEIGHT_STANCE = 133, 290
    SPRITE_WIDTH_HIT, SPRITE_HEIGHT_HIT = 133, 290
    SPRITE_WIDTH_FALLINGDOWN, SPRITE_HEIGHT_FALLINGDOWN = 195, 290
    SPRITE_WIDTH_GETUP, SPRITE_HEIGHT_GETUP = 145, 290
    SPRITE_WIDTH_DOUBLEPUNCHING, SPRITE_HEIGHT_DOUBLEPUNCHING = 183, 290  # New dimensions
    SPRITE_WIDTH_KICKING, SPRITE_HEIGHT_KICKING = 190, 290  # New dimensions

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
        self.is_double_punching = False  # New state
        self.is_kicking = False  # New state
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

        # Load double punching frames
        self.double_punching_left = [get_frame_DoublePunching(double_punching_sheet, 0, i, self.SPRITE_WIDTH_DOUBLEPUNCHING, self.SPRITE_HEIGHT_DOUBLEPUNCHING) for i in range(7)]
        self.double_punching_right = [get_frame_DoublePunching(double_punching_sheet, 1, i, self.SPRITE_WIDTH_DOUBLEPUNCHING, self.SPRITE_HEIGHT_DOUBLEPUNCHING) for i in range(7)]
        self.double_punching_left = [frame for frame in self.double_punching_left if frame is not None]
        self.double_punching_right = [frame for frame in self.double_punching_right if frame is not None]

        # Load kicking frames
        self.kicking_left = [get_frame_kicking(kicking_sheet, 0, i, self.SPRITE_WIDTH_KICKING, self.SPRITE_HEIGHT_KICKING) for i in range(6)]
        self.kicking_right = [get_frame_kicking(kicking_sheet, 1, i, self.SPRITE_WIDTH_KICKING, self.SPRITE_HEIGHT_KICKING) for i in range(6)]
        self.kicking_left = [frame for frame in self.kicking_left if frame is not None]
        self.kicking_right = [frame for frame in self.kicking_right if frame is not None]
        
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
                self.state = "IDLE"
        if self.x < target_x:
            self.current_frame = self.falling_down_left[min(self.frame_index, len(self.falling_down_left) - 1)]
        else:
            self.current_frame = self.falling_down_right[min(self.frame_index, len(self.falling_down_right) - 1)]

    def update_frame_getting_up(self, target_x):
        self.frame_counter += 1
        if self.frame_counter % 6 == 0:
            self.frame_index = (self.frame_index + 1) % len(self.get_up_left)
            if self.frame_index == 0:
                self.is_getting_up = False
                self.state = "IDLE"
        if self.x < target_x:
            self.current_frame = self.get_up_left[min(self.frame_index, len(self.get_up_left) - 1)]
        else:
            self.current_frame = self.get_up_right[min(self.frame_index, len(self.get_up_right) - 1)]

    def update_frame_double_punching(self, target_x):
        self.frame_counter += 1
        if self.frame_counter % 6 == 0:
            self.frame_index = (self.frame_index + 1) % len(self.double_punching_left)
            if self.frame_index == 0:
                self.is_double_punching = False
                self.state = "IDLE"
        if self.x < target_x:
            self.current_frame = self.double_punching_left[min(self.frame_index, len(self.double_punching_left) - 1)]
        else:
            self.current_frame = self.double_punching_right[min(self.frame_index, len(self.double_punching_right) - 1)]

    def update_frame_kicking(self, target_x):
        self.frame_counter += 1
        if self.frame_counter % 6 == 0:
            self.frame_index = (self.frame_index + 1) % len(self.kicking_left)
            if self.frame_index == 0:
                self.is_kicking = False
                self.state = "IDLE"
        if self.x < target_x:
            self.current_frame = self.kicking_left[min(self.frame_index, len(self.kicking_left) - 1)]
        else:
            self.current_frame = self.kicking_right[min(self.frame_index, len(self.kicking_right) - 1)]

    def update_frame(self, target_x):
        if self.is_falling_down:
            self.update_frame_falling_down(target_x)
        elif self.is_getting_up:
            self.update_frame_getting_up(target_x)
        elif self.is_hit:
            self.update_frame_hit(target_x)
        elif self.is_double_punching:
            self.update_frame_double_punching(target_x)
        elif self.is_kicking:
            self.update_frame_kicking(target_x)
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

    def random_behavior(self, player_x):
        """Randomly switch between states."""
        if abs(self.x - player_x) < 100:  # Check if the player is within range
            self.state = random.choice(["IDLE", "WALK", "DOUBLE_PUNCHING", "KICKING"])
            if self.state == "DOUBLE_PUNCHING":
                self.is_double_punching = True
            elif self.state == "KICKING":
                self.is_kicking = True
        else:
            self.state = random.choice(["IDLE", "WALK"])
            self.is_double_punching = False
            self.is_kicking = False

# Main loop
def main():
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    villain = Villain(100, 100)
    player_x = 400  # Example player position

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.USEREVENT + 1:
                villain.random_behavior(player_x)

        villain.update_position(player_x)
        villain.update_frame(player_x)

        screen.fill((0, 0, 0))
        villain.draw(screen)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()

# Set a timer event to change behavior every 1 seconds
pygame.time.set_timer(pygame.USEREVENT + 1, 1000)