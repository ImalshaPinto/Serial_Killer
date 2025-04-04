import pygame
from main_character import MainCharacter  # Import the MainCharacter class
from vilan import Villain  # Import the Villain class
from collision_handler import CollisionHandler  # Import the CollisionHandler class

# Initialize pygame
pygame.init()

# Screen dimensionsa
screen = pygame.display.set_mode((1250, 700))

# Title and Icon
pygame.display.set_caption("Skull Killer")
icon = pygame.image.load('backgroundLevel1.jpg')
pygame.display.set_icon(icon)

# Background
background = pygame.image.load('palacegrounds.png')
background = pygame.transform.scale(background, (1250, 700))

# Load the sprite sheet
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

# Game loop
running = True
clock = pygame.time.Clock()
player = MainCharacter(370, 350)
villain = Villain(800, 350)  # Initialize the villain at a different position
collision_handler = CollisionHandler()  # Initialize the collision handler

# Set a timer event to change behavior every 2 seconds
pygame.time.set_timer(pygame.USEREVENT + 1, 2000)

def handle_keydown(event, player, keys, current_time):
    if not player.is_movement_in_progress:
        if event.key == pygame.K_LEFT:
            player.x_change = -3
        elif event.key == pygame.K_RIGHT:
            player.x_change = 3
        elif event.key == pygame.K_DOWN:
            player.is_ducking = True
            player.is_getting_up = False
            player.frame_index = 0
        elif event.key == pygame.K_UP:
            player.is_jumping_directional = player.x_change != 0
            player.is_jumping_vertical = not player.is_jumping_directional
            player.frame_index = 0
            player.is_movement_in_progress = True
        elif event.key == pygame.K_a:
            if current_time - player.last_a_press_time < 500:
                player.is_double_punching = True
            else:
                player.is_punching = True
            player.frame_index = 0
            player.last_a_press_time = current_time
            player.is_movement_in_progress = True
        elif event.key == pygame.K_d:
            if current_time - player.last_down_press_time < 400 and keys[pygame.K_DOWN]:
                player.is_und_kicking = True
            else:
                player.is_kicking = True
            player.frame_index = 0
            player.is_movement_in_progress = True

def handle_villain_attack(collision_handler, player, villain, small_hit, falling):
    if collision_handler.is_collision(player, villain):
        if villain.is_double_punching:
            player.execute_hit_animation(small_hit, 3, 2)
        elif villain.is_kicking:
            player.execute_fall_animation(falling, 7, 2, villain.direction)

while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    keys = pygame.key.get_pressed()
    current_time = pygame.time.get_ticks()

    if keys[pygame.K_DOWN]:
        player.last_down_press_time = current_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            handle_keydown(event, player, keys, current_time)
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                player.x_change = 0
            elif event.key == pygame.K_DOWN:
                player.is_ducking = False
                player.is_getting_up = True
                player.frame_index = 0
        elif event.type == pygame.USEREVENT + 1:
            villain.random_behavior(player.x)

    player.update_position()
    player.update_frame(villain.x)
    player.draw()

    villain.update_position(player.x)  # Update villain's position towards the main character
    villain.update_frame(player.x)  # Pass the main character's x position to update_frame
    villain.draw(screen)

    # Handle collisions
    collision_handler.update(player, villain)
    handle_villain_attack(collision_handler, player, villain, small_hit, falling)

    pygame.display.update()
    clock.tick(60)

pygame.quit()