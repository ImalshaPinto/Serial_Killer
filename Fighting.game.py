import pygame
from main_character import MainCharacter  # Import the MainCharacter class
from vilan import Villain  # Import the Villain class

# Initialize pygame
pygame.init()

# Screen dimensions
screen = pygame.display.set_mode((1250, 700))

# Title and Icon
pygame.display.set_caption("Skull Killer")
icon = pygame.image.load('backgroundLevel1.jpg')
pygame.display.set_icon(icon)

# Background
background = pygame.image.load('palacegrounds.png')
background = pygame.transform.scale(background, (1250, 700))

# Load the sprite sheet
sprite_sheet = pygame.image.load('Scorpian/last.png')
sprite_sheet2 = pygame.image.load('Scorpian/Srunning.png')
sprite_sheet3 = pygame.image.load('Scorpian/duck&up.png')
sprite_sheet4 = pygame.image.load('Scorpian/jumpfront3.png')
sprite_sheet5 = pygame.image.load('Scorpian/jump.png')
sprite_sheet6 = pygame.image.load('Scorpian/Dpunch.png')
sprite_sheet7 = pygame.image.load('Scorpian/punch.png')
sprite_sheet8 = pygame.image.load('Scorpian/bBkick.png')

# Game loop
running = True
clock = pygame.time.Clock()
player = MainCharacter(370, 345) # Initialize the main character
villain = Villain(800, 350)  # Initialize the villain at a different position

while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    keys = pygame.key.get_pressed()
    current_time = pygame.time.get_ticks()

    if keys[pygame.K_UP]:
        player.last_up_press_time = current_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.x_change = -3
            if event.key == pygame.K_RIGHT:
                player.x_change = 3
            if event.key == pygame.K_DOWN:
                player.is_ducking = True
                player.is_getting_up = False
                player.frame_index = 0
            if event.key == pygame.K_UP:
                if player.x_change != 0:  # Directional jump
                    player.is_jumping_directional = True
                else:  # Vertical jump
                    player.is_jumping_vertical = True
                player.frame_index = 0
            if event.key == pygame.K_a:
                if current_time - player.last_a_press_time < 500:  # Double press within 500ms
                    player.is_double_punching = True
                    player.frame_index = 0
                else:
                    player.is_punching = True
                    player.frame_index = 0
                player.last_a_press_time = current_time
            if event.key == pygame.K_d:
                player.is_kicking = True
                player.frame_index = 0
            
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                player.x_change = 0
            if event.key == pygame.K_DOWN:
                player.is_ducking = False
                player.is_getting_up = True
                player.frame_index = 0

    player.update_position()
    player.update_frame()
    player.draw()

    villain.update_position(player.x)  # Update villain's position towards the main character
    villain.update_frame(player.x)  # Pass the main character's x position to update_frame
    villain.draw()

    pygame.display.update()
    clock.tick(60)

pygame.quit()