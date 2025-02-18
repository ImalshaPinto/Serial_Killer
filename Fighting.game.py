import pygame
from main_character import MainCharacter  # Import the MainCharacter class

# Initialize pygame
pygame.init()

# Screen dimensions
screen = pygame.display.set_mode((1250, 700))

# Title and Icon
pygame.display.set_caption("Skull Killer")
icon = pygame.image.load('backgroundLevel1.jpg')
pygame.display.set_icon(icon)

# Background
background = pygame.image.load('backgroundLevel1.jpg')
background = pygame.transform.scale(background, (1250, 700))

# Load the sprite sheets
sprite_sheet = pygame.image.load('SerialKiller.png')
sprite_sheet1 = pygame.image.load('jump1.png')
sprite_sheet2 = pygame.image.load('handpuch1.png')

# Extract frames from running sprite sheet
def get_frame_Running(row, col, width, height):
    return sprite_sheet.subsurface(pygame.Rect(col * width, row * height, width, height))

# Extract frames from jumping sprite sheet
def get_frame_jumping(row, col, width, height):
    sheet_width, sheet_height = sprite_sheet1.get_size()
    if col * width + width > sheet_width or row * height + height > sheet_height:
        return None  
    return sprite_sheet1.subsurface(pygame.Rect(col * width, row * height, width, height))

# Extract frames from jumping sprite sheet for left direction
def get_frame_jumping_left(row, col, width, height):
    sheet_width, sheet_height = sprite_sheet1.get_size()
    if col * width + width > sheet_width or row * height + height > sheet_height:
        return None  
    return sprite_sheet1.subsurface(pygame.Rect(col * width, row * height, width, height))

# Extract frames from punching
def get_frame_handpunch(row, col, width, height):
    sheet_width, sheet_height = sprite_sheet2.get_size()
    if col * width + width > sheet_width or row * height + height > sheet_height:
        return None  
    return sprite_sheet2.subsurface(pygame.Rect(col * width, row * height, width, height))

# Game loop
running = True
clock = pygame.time.Clock()
player = MainCharacter(370, 350)

while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.x_change = -3
            if event.key == pygame.K_RIGHT:
                player.x_change = 3
            if event.key == pygame.K_SPACE and not player.is_jumping:
                player.is_jumping = True
                player.velocity_y = player.JUMP_POWER
                player.frame_index = 0
            if event.key == pygame.K_a and not player.is_punching:
                player.is_punching = True
                player.frame_index = 0
            if event.key == pygame.K_w and not player.is_swing:
                player.is_swing = True
                player.frame_index = 0

        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                player.x_change = 0

    player.update_position()
    player.update_frame()
    player.draw()

    pygame.display.update()
    clock.tick(60)

pygame.quit()