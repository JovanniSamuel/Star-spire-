import pygame

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1000, 600 #Size of window

screen = pygame.display.set_mode((WIDTH, HEIGHT)) #Makes window
pygame.display.set_caption("Trinity of one")  #Names window
clock = pygame.time.Clock() #Set the fps


# Sound effects ####################################
pygame.mixer.music.load("main_menu_sound.mp3")
pygame.mixer.music.set_volume(0.5) #volume of sound
pygame.mixer.music.play(-1)# ensues that it loops forever





# Classes 

# class Character(pygame.sprite.Sprite): # starts the charcter class
#     def __init__(self, name, load_sprite,  size, x, y, hp=100,attack=10, speed=10, mana=100,defense=5):
#         super().__init__()
#         self.name = name
#         self.image= load_image(load_sprite, size)
#         self.rect = self.image.get_rect()
#         self.x = x
#         self.y = y
#         self.hp = hp
#         self.attack = attack
#         self.speed = speed
#         self.max_hp = hp
#         self.mana = mana
#         self.defense = defense
        
#     def take_damage(self, amount):
#         reduced = max(amount - self.defense, 1)
#         self.hp -= reduced
#         if self.hp < 0:
#             self.hp = 0
#         return reduced
    
#     def is_alive(self):
#         return self.hp > 0
    
#     def attack_target(self, target):
#         target.take_damage(self.attack)
        
        
# class Player(Character):
#     def __init__(self, name, load_sprite, size, x, y, hp=200, attack=10, speed=10, mana=250, defense=5,mana_regen=5):
#         super().__init__(name, load_sprite, size, x, y, hp, attack, speed, mana, defense)
#         self.name = name
        
# class Summoner(Character):
#     def __init__(self, name, player_sprite, size, x, y, hp=200, attack=10, speed=10, mana=250, defense=5, mana_regen=6):
#         super().__init__(name, player_sprite, size, x, y, hp, attack, speed, mana, defense)
#         self.familliar = []
#         self.mana = mana
#         self.max_mana = mana
#         self.mans_regen = mana_regen
      
#     def summon_familliar(self, familiar_group, load_sprite, size, x, y, mana_cost=30):
#         self.familliar = [f for f in self.familiars if f.is_alive()]
        
#         if self.mana < mana_cost:
#             return None
        
#         self.mana -= mana_cost
#         familiar = Familiar(self, familiar_type, load_sprite
    

BLACK = (0, 0, 0) #Background color

def load_image(filename, size):
    surf = pygame.image.load(filename).convert_alpha()
    return pygame.transform.smoothscale(surf, size)

class Start_Button(pygame.sprite.Sprite): #Start button class
    def __init__(self):
        super().__init__()
        self.image = load_image("Start_button2.png", (400, 175))
        self.rect = self.image.get_rect()
        self.rect.x = 500
        self.rect.y = 350
        pygame.Rect(0, 0, 240, 240)


class Character_button(pygame.sprite.Sprite): #Character button class
    def __init__(self):
        super().__init__()
        self.image = load_image("Select_character_button2.png", (400, 200))
        self.rect = self.image.get_rect()
        self.rect.x = 500
        self.rect.y = 100

class Menu_Background(pygame.sprite.Sprite): #Menu background class
    def __init__(self):
        super().__init__()
        self.image = load_image("Menu_Background.png", (WIDTH, HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

class Character_display(pygame.sprite.Sprite): #Character display class
    def __init__(self):
        super().__init__()
        self.image = load_image("Character Border.png", (250, 300))
        self.rect = self.image.get_rect()
        self.rect.x = 60
        self.rect.y = 90

menu_sprites = pygame.sprite.Group()
menu_sprites.add(Menu_Background())
menu_sprites.add(Start_Button())
menu_sprites.add(Character_button())
menu_sprites.add(Character_display())

running = True
while running:
    for event in pygame.event.get(): #starts the game
        if event.type == pygame.QUIT:
            running = False
    menu_sprites.update()
    menu_sprites.draw(screen)
    pygame.display.flip() #Update the display
    clock.tick(60)
    
pygame.quit()