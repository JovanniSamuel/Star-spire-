
import pygame

pygame.init()

WIDTH, HEIGHT = 1000, 600 

screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
pygame.display.set_caption("Trinity of one")  
clock = pygame.time.Clock() 

BLACK = (0, 0, 0)


fattack_sprites = [
    pygame.image.load("Attack2.png").convert_alpha(),
    pygame.image.load("Attack3.png").convert_alpha()
]

frame_index = 0.0
animation_speed = 0.05

character_x = 350
character_y = 250


def animate_sprite(sprites, current_frame, speed):
    current_frame += speed
    if current_frame >= len(sprites):
        current_frame = 0
    active_image = sprites[int(current_frame)]
    return active_image, current_frame

attack_sprites = [
    pygame.image.load("Attack21.png").convert_alpha(),
    pygame.image.load("Attack31.png").convert_alpha()
]

running = True
while running:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = False
    current_image, frame_index = animate_sprite(attack_sprites, frame_index, animation_speed)

  
 
    if character_x > 800:  
        character_x = -current_image.get_width()

    screen.fill(BLACK) 
    
    screen.blit(current_image, (character_x, character_y))

    pygame.display.flip() 
    clock.tick(60)
    
pygame.quit()



