import pygame

pygame.init()

WIDTH, HEIGHT = 1000, 600 #Size of window

screen = pygame.display.set_mode((WIDTH, HEIGHT)) #Makes window
pygame.display.set_caption("Trinity of one")  #Names window
clock = pygame.time.Clock() #Set the fps

BLACK = (0, 0, 0) #Background color



def load_image(filename, size):
    surf = pygame.image.load(filename).convert_alpha()
    return pygame.transform.smoothscale(surf, size)

class Start_button(pygame.sprite.Sprite): #Start button class
    def __init__(self):
        super().__init__()
        self.image = load_image("Start_button2.png", (400, 175))
        self.rect = self.image.get_rect()
        self.rect.x = 500
        self.rect.y = 100
    def on_click(self):
        print("Start Pressed!")


class Character_button(pygame.sprite.Sprite): #Character button class
    def __init__(self):
        super().__init__()
        self.image = load_image("Select_character_button2.png", (450, 200))
        self.rect = self.image.get_rect()
        self.rect.x = 500
        self.rect.y = 350
    def on_click(self):
        print("Select Character Pressed!")

class Menu_Background(pygame.sprite.Sprite): #Menu background class
    def __init__(self):
        super().__init__()
        self.image = load_image("Menu_background.png", (WIDTH, HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

class Character_display(pygame.sprite.Sprite): #Character display class
    def __init__(self):
        super().__init__()
        self.image = load_image("Character Border.png", (450, 600))
        self.rect = self.image.get_rect()
        self.rect.x = 40
        self.rect.y = 10

def check_button_clicks(sprite_group, pos):
    for sprite in sprite_group:
        if sprite.rect.collidepoint(pos):
            sprite.on_click()

menu_sprites = pygame.sprite.Group()
menu_sprites.add(Menu_Background())
menu_sprites.add(Start_button())
menu_sprites.add(Character_button())
menu_sprites.add(Character_display())

buttons = pygame.sprite.Group()
start_button = Start_button()
character_button = Character_button()
buttons.add(start_button)
buttons.add(character_button)


running = True
while running:
    for event in pygame.event.get(): #starts the game
        if event.type == pygame.QUIT:
            running = False
        menu_sprites.update()
        menu_sprites.draw(screen)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            check_button_clicks(buttons, event.pos)
    pygame.display.flip() #Update the display
    clock.tick(60)
    
pygame.quit()