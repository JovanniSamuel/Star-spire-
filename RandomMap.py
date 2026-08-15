import pygame
import random

pygame.init()
pygame.mixer.init()


WIDTH, HEIGHT = 1000, 600 #Size of window

screen = pygame.display.set_mode((WIDTH, HEIGHT)) #Makes window
pygame.display.set_caption("Trinity of one")  #Names window
clock = pygame.time.Clock() #Set the fps

level = 0

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
    
class Forest1(pygame.sprite.Sprite): 
    def __init__(self):
        super().__init__()
        self.image = load_image("ForestMap1.png", (WIDTH, HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

class Forest2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image("ForestMap2.png", (WIDTH, HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

class ForestBoss(pygame.sprite.Sprite): 
    def __init__(self):
        super().__init__()
        self.image = load_image("ForestBossMap.png", (WIDTH, HEIGHT ))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

class Castle1(pygame.sprite.Sprite): 
    def __init__(self):
        super().__init__()
        self.image = load_image("CastleMap1.png", (WIDTH, HEIGHT ))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

class Castle2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image("CastleMap2.png", (WIDTH, HEIGHT ))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

class CastleBoss(pygame.sprite.Sprite): 
    def __init__(self):
        super().__init__()
        self.image = load_image("CastleBossMap.png", (WIDTH, HEIGHT ))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

class Swamp1(pygame.sprite.Sprite): 
    def __init__(self):
        super().__init__()
        self.image = load_image("SwampMap1.png", (WIDTH, HEIGHT ))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

class Swamp2(pygame.sprite.Sprite): 
    def __init__(self):
        super().__init__()
        self.image = load_image("SwampMap2.png", (WIDTH, HEIGHT ))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

class SwampBoss(pygame.sprite.Sprite): 
    def __init__(self):
        super().__init__()
        self.image = load_image("SwampBossMap.png", (WIDTH, HEIGHT ))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

class Desert1(pygame.sprite.Sprite): 
    def __init__(self):
        super().__init__()
        self.image = load_image("DesertMap1.jpg", (WIDTH, HEIGHT ))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

class Desert2(pygame.sprite.Sprite): 
    def __init__(self):
        super().__init__()
        self.image = load_image("DesertMap2.jpg", (WIDTH, HEIGHT ))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

class DesertBoss(pygame.sprite.Sprite): 
    def __init__(self):
        super().__init__()
        self.image = load_image("DesertBossMap.png", (WIDTH, HEIGHT ))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

Desertbgs =[
    Desert1(),
    Desert2(),
    DesertBoss()
]

Swampbgs = [
    Swamp1(),
    Swamp2(),
    SwampBoss()
]

Forestbgs = [
    Forest1(),
    Forest2(),
    ForestBoss()
]

Castlebgs = [
    Castle1(),
    Castle2(),
    CastleBoss()
]

player = Assassin()
character_sprites = pygame.sprite.Group()
character_sprites.add(player)
backgrounds = pygame.sprite.Group()

Map = random.randint(1, 4)
def Selector():
    global level
    backgrounds.empty()
    if Map == 1:
        return backgrounds.add(Desertbgs[level]) 
    elif Map == 2:
        return backgrounds.add(Swampbgs[level])
    elif Map == 3:
        return backgrounds.add(Forestbgs[level])
    else:
        return backgrounds.add(Castlebgs[level])

game_over = False
you_win = False
running = True
Selector()
while running:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                level += 1
                if level <= 3:
                         
                    print (level)
                    Selector()
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
