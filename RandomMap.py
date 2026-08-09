import pygame
import random

pygame.init()
pygame.mixer.init()


WIDTH, HEIGHT = 1000, 600 #Size of window

screen = pygame.display.set_mode((WIDTH, HEIGHT)) #Makes window
pygame.display.set_caption("Trinity of one")  #Names window
clock = pygame.time.Clock() #Set the fps

BLACK = (0, 0, 0) #Background color

def load_image(filename, size):
    surf = pygame.image.load(filename).convert_alpha()
    return pygame.transform.smoothscale(surf, size)

class Assassin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image("Assassin.png", (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = 450  
        self.rect.y = 250
        self.speed = 3

    def move(self, keys):
        if keys[pygame.K_UP]:    
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:  
            self.rect.y += self.speed
        if keys[pygame.K_LEFT]:  
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]: 
            self.rect.x += self.speed
    
class Background1(pygame.sprite.Sprite): 
    def __init__(self):
        super().__init__()
        self.image = load_image("Mockup1.png", (WIDTH, HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

class Background2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image("Mockup2.png", (WIDTH, HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

class Background3(pygame.sprite.Sprite): 
    def __init__(self):
        super().__init__()
        self.image = load_image("Mockup3.png", (WIDTH, HEIGHT ))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

player = Assassin()
character_sprites = pygame.sprite.Group()
character_sprites.add(player)

backgrounds = pygame.sprite.Group()
def Selector():
    back = random.randint(1, 3)
    if back == 1:
        backgrounds.add(Background1())
    elif back == 2:
        backgrounds.add(Background2())
    else:
        backgrounds.add(Background3())

game_over = False
you_win = False
Selector()
running = True
while running:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = False

    if not game_over and not you_win:
        keys = pygame.key.get_pressed()
        player.move(keys)
        player.rect.clamp_ip(screen.get_rect())
        character_sprites.update()
    backgrounds.draw(screen)
    backgrounds.update()
    character_sprites.draw(screen)
    pygame.display.flip() 
    clock.tick(60)

pygame.quit()
    