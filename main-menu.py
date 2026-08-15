import pygame
import random
import classes_mobs
import gameplay

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1000, 600  # Size of window

screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Makes window
pygame.display.set_caption("Dark Spire")  # Names window
clock = pygame.time.Clock()  # Set the fps

BLACK = (0, 0, 0)  # Background color
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


class Menu_Background(pygame.sprite.Sprite):  # Menu background class
    def __init__(self):
        super().__init__()
        self.image = load_image("Dark_Spire_Background.png", (WIDTH, HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


class Quit_button(pygame.sprite.Sprite):  # Quit button class
    def __init__(self):
        super().__init__()
        self.image = load_image("QuitButton.png", (275, 205))
        self.rect = self.image.get_rect()
        self.rect.x = 680
        self.rect.y = 300

    def on_click(self):
        print("Quit Pressed!")
        global running
        running = False


class Start_button(pygame.sprite.Sprite):  # Character button class
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


class Play_button(pygame.sprite.Sprite):  # Start button class
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
        # gameplay.run() owns its own loop (character select, combat, everything)
        # and only returns once the player quits, reusing this same window/clock
        # rather than opening a second one.
        gameplay.run(screen, clock)
        global running
        running = False


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


def check_button_clicks(sprite_group, pos):
    for sprite in sprite_group:
        if hasattr(sprite, "on_click") and sprite.rect.collidepoint(pos):
            sprite.on_click()


# BUG FIX: previously there were two separate sets of button sprites -- one
# group only ever drawn (menu_sprites/character_selected_sprites) and a second,
# completely separate set of freshly-constructed objects only used for click
# detection (buttons/character_buttons). They happened to sit at the same
# coordinates so clicking "worked", but every button's image was loaded twice
# for no reason, and any future change to one set silently wouldn't affect the
# other. Now there's exactly one group per screen, used for both drawing and
# click detection.
menu_sprites = pygame.sprite.Group()
menu_sprites.add(Menu_Background())
menu_sprites.add(Start_button())
menu_sprites.add(Quit_button())

character_selected_sprites = pygame.sprite.Group()
character_selected_sprites.add(Left_Button())
character_selected_sprites.add(Right_Button())
character_selected_sprites.add(Play_button())

running = True
while running:
    for event in pygame.event.get():  # starts the game
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if Screen == 0:
                check_button_clicks(menu_sprites, event.pos)
            elif Screen == 1:
                check_button_clicks(character_selected_sprites, event.pos)

    # BUG FIX: drawing/updating used to happen INSIDE the "for event in
    # pygame.event.get()" loop, so on any frame with zero events (very common
    # at 60fps when the mouse/keyboard is idle) nothing got drawn at all,
    # causing flicker. Drawing now happens once per frame, after events are
    # processed, regardless of how many events fired.
    screen.fill(BLACK)

    if Screen == 0:
        menu_sprites.update()
        menu_sprites.draw(screen)
    elif Screen == 1:
        # BUG FIX: this used to only rebuild/draw the stats background inside
        # the MOUSEBUTTONDOWN branch, so the character-select background only
        # flashed onscreen for the single frame you clicked. It's rebuilt from
        # the current Stats index and drawn every frame now.
        bg_group = pygame.sprite.Group(backgrounds[Stats])
        bg_group.draw(screen)
        character_selected_sprites.update()
        character_selected_sprites.draw(screen)

    pygame.display.flip()  # Update the display
    clock.tick(60)

pygame.quit()