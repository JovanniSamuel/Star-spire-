import pygame

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1000, 600 #Size of window

screen = pygame.display.set_mode((WIDTH, HEIGHT)) #Makes window
pygame.display.set_caption("Dark Spire")  #Names window
clock = pygame.time.Clock() #Set the fps

BLACK = (0, 0, 0) #Background color
Screen = 0
Stats = 0
Sound = -1

sound_one = pygame.mixer.Sound("main_menu_sound.mp3")
sound_two = pygame.mixer.Sound("ButtonClick.mp3")

sound_one.set_volume(0.1)
sound_two.set_volume(0.5)

sound_one.play(Sound)
    
def load_image(filename, size):
    surf = pygame.image.load(filename).convert_alpha()
    return pygame.transform.smoothscale(surf, size)

class Menu_Background(pygame.sprite.Sprite): #Menu background class
    def __init__(self):
        super().__init__()
        self.image = load_image("Dark_Spire_Background.png", (WIDTH, HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

class Quit_button(pygame.sprite.Sprite): #Quit button class
    def __init__(self):
        super().__init__()
        self.image = load_image("QuitButton.png", (275, 205))
        self.rect = self.image.get_rect()
        self.rect.x = 680
        self.rect.y = 300
    def on_click(self):
        print("Quit Pressed!")
        sound_two.play(0)
        pygame.time.wait(1000)
        global running
        running = False

class Start_button(pygame.sprite.Sprite): #Character button class
    def __init__(self):
        super().__init__()
        self.image = load_image("StartButton.png", (240, 110))
        self.rect = self.image.get_rect()
        self.rect.x = 75
        self.rect.y = 350
    def on_click(self):
        print("Start Pressed!")
        sound_two.play(0) 
        global Screen
        Screen = 1
  
class Play_button(pygame.sprite.Sprite): #Start button class
    def __init__(self):
        super().__init__()
        self.image = load_image("PlayButton.png", (240, 110))
        self.rect = self.image.get_rect()
        self.rect.x = 625
        self.rect.y = 485
    def on_click(self):
        print("Play Button Pressed!")
        sound_two.play(0) 
        sound_one.stop()
        global Screen
        Screen = 2

class Left_Button(pygame.sprite.Sprite): 
    def __init__(self):
        super().__init__()
        self.image = load_image("Left_Button.png", (65, 75))
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 265
    def on_click(self):
        print("Left Button Pressed!")
        sound_two.play(0) 
        global Stats
        Stats -= 1
        if Stats < 0:
            Stats = 3
        print(Stats)

class Right_Button(pygame.sprite.Sprite): 
    def __init__(self):
        super().__init__()
        self.image = load_image("Right_Button.png", (65, 75))
        self.rect = self.image.get_rect()
        self.rect.x = 925
        self.rect.y = 265
    def on_click(self):
        print("Right Button Pressed!")
        sound_two.play(0) 
        global Stats
        Stats += 1
        if Stats > 3:
            Stats = 0
        print(Stats)

class Assassin_Stats(pygame.sprite.Sprite): 
    def __init__(self):
        super().__init__()
        self.image = load_image("Assassin_Stats.png", (WIDTH, HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

class Gladiator_Stats(pygame.sprite.Sprite): 
    def __init__(self):
        super().__init__()
        self.image = load_image("Gladiator_Stats.png", (WIDTH, HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

class Summoner_Stats(pygame.sprite.Sprite): 
    def __init__(self):
        super().__init__()
        self.image = load_image("Summoner_Stats.png", (WIDTH, HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

class MagicKnight_Stats(pygame.sprite.Sprite): 
    def __init__(self):
        super().__init__()
        self.image = load_image("MagicKnight_Stats.png", (WIDTH, HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

backgrounds = [
    Assassin_Stats(),
    Gladiator_Stats(),
    Summoner_Stats(),
    MagicKnight_Stats()
]
bg_group = pygame.sprite.Group(backgrounds[Stats])

def check_button_clicks(sprite_group, pos):
    for sprite in sprite_group:
        if sprite.rect.collidepoint(pos):
            sprite.on_click()

def Character_Selector():
    menu_sprites.empty()
    buttons.empty()
    character_selected_sprites.update()
    character_selected_sprites.draw(screen)
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        check_button_clicks(character_buttons, event.pos)
        if Stats ==0:
            bg_group = pygame.sprite.Group(backgrounds[0])
        elif Stats ==1:
            bg_group = pygame.sprite.Group(backgrounds[1])
        elif Stats ==2:
            bg_group = pygame.sprite.Group(backgrounds[2])
        elif Stats ==3:
            bg_group = pygame.sprite.Group(backgrounds[3])
        bg_group.draw(screen)
        character_selected_sprites.draw(screen)

menu_sprites = pygame.sprite.Group()
menu_sprites.add(Menu_Background())
menu_sprites.add(Start_button())
menu_sprites.add(Quit_button())

character_selected_sprites = pygame.sprite.Group()
character_selected_sprites.add(Left_Button())
character_selected_sprites.add(Right_Button())
character_selected_sprites.add(Play_button())

buttons = pygame.sprite.Group()
buttons.add(Start_button())
buttons.add(Quit_button())

character_buttons = pygame.sprite.Group()
character_buttons.add(Left_Button())
character_buttons.add(Right_Button())
character_buttons.add(Play_button())

running = True
while running:
    for event in pygame.event.get(): #starts the game
        if event.type == pygame.QUIT:
            running = False
        menu_sprites.update()
        menu_sprites.draw(screen)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            check_button_clicks(buttons, event.pos)
        if Screen == 1:
            Character_Selector()
        if Screen == 2:
            import RandomMap
    pygame.display.flip()
    clock.tick(60)    
pygame.quit()