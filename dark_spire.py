import pygame
import random # for crit chance 

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

class Charcters(pygame.sprite.Sprite): # starts the charcter class
    def __init__(self, name, load_sprite,  size, x, y, hp=100,attack=10,magicpower=10, speed=10, mana=100,defense=5, poison = False, poison_damage=0, poison_ticks_left=5, poison_tick_timer=0, ult_cooldown=60000, ult_ready_timer=0):
        super().__init__()
        self.name = name
        self.image= load_image(load_sprite, size)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.hp = hp
        self.attack = attack
        self.speed = speed
        self.max_hp = hp
        self.mana = mana
        self.defense = defense
        self.magicpower = magicpower
        self.poison = poison
        self.poison_damage = poison_damage
        self.poison_ticks_left = poison_ticks_left
        self.poison_tick_timer = poison_tick_timer
        self.ult_cooldown = ult_cooldown
        self.ult_ready_timer = ult_ready_timer
        
    def take_damage(self, amount):
        reduced = max(amount - self.defense, 1)
        self.hp -= reduced
        if self.hp < 0:
            self.hp = 0
        return reduced
    
    def is_alive(self):
        return self.hp > 0
    
    def attack_target(self, target):
        target.take_damage(self.attack)
        
        
class Mobs(Charcters):
    def __init__(self, name, load_sprite, size, x, y, hp=100, attack=10, magicpower=10, speed=10, mana=50, defense=5, mana_regen=5, poison_ticks=0, poison_tick_timer=0, poison_damage=0, can_poison=False):
        super().__init__(name, load_sprite, size, x, y, hp, attack, magicpower, speed, mana, defense)
        self.name = name
        self.image = load_image(load_sprite, size)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y     
        self.hp = hp
        self.attack = attack
        self.magicpower = magicpower
        self.speed = speed
        self.defense = defense
        self.mana = mana
        self.max_hp = hp
        self.mana_regen = mana_regen
        self.poison_ticks_left = poison_ticks
        self.poison_tick_timer = poison_tick_timer
        self.poison_damage = poison_damage
        self.can_poison = can_poison
    
    def enemy_attack(self, target):
         if getattr(target, "invisibility", False):
             if random.random() < 1/10:  # 10% chance to hit an invisible target
                    damage = max(self.attack - target.defense, 0)
                    target.hp -= damage
                    target.hp = max(target.hp, 0)
                    target.invisibility = False  # Target becomes visible after being hit
                    print(f"{target.name} is no longer invisible!")
                    if self.can_poison:
                        target.poison = True
                        target.poison_damage = max(int(target.max_hp) // 32, 1) # DEALS  1/32 OF MAX HP AS POISON DAMAGE
                        target.poison_ticks_left = 5
                        target.poison_tick_timer = pygame.time.get_ticks()
                        print(f"{target.name} has been poisoned by {self.name}!")
             else:# miss entirely no damage taken
                    print(f"{self.name} missed {target.name} because they are invisible!")
        
        
# class Summoner(Charcters):
#     def __init__(self, name, player_sprite, size, x, y, hp=200, attack=10, magicpower=10, speed=10, mana=250, defense=5, mana_regen=6):
#         super().__init__(name, player_sprite, size, x, y, hp, attack, magicpower, speed, mana, defense)
#         self.familliar = []
#         self.mana = mana
#         self.max_mana = mana
#         self.mans_regen = mana_regen
      
#     def summon_familliar(self, familiar_group, load_sprite, size, x, y, mana_cost=30):
#         self.familliar = [f for f in self.familiars if f.is_alive()]
        
#         if self.mana < mana_cost:
#             return None
        
#         self.mana -= mana_cost
#         familiar = Familiar(self, load_sprite):
    
class Assain(Charcters):# Assain class and features
    def __init__(self, name, player_sprite, size, x, y, hp=150, attack=30, magicpower=10, speed=35, mana=150, defense=12, mana_regen=5,crit_chance=0.0625, crit_multiplier=1.5,
                 invisibility=False, invisible_cost=3, invisibility_timer= 0):
        super().__init__(name, player_sprite, size, x, y, hp, attack, magicpower, speed, mana, defense, mana_regen, poison=False, poison_damage=0, poison_ticks_left=0, poison_tick_timer=0, ult_cooldown=60000, ult_ready_timer=0)
        self.name = name
        self.image = load_image(player_sprite, size)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 
        self.name = name        
        self.mana = mana
        self.hp = hp    
        self.attack = attack
        self.magicpower = magicpower    
        self.speed = speed
        self.defense = defense
        self.max_hp = hp
        self.mana_regen = mana_regen
        self.crit_chance = crit_chance
        self.crit_multiplier = crit_multiplier
        self.invisibility = invisibility    
        self.invisible_cost = invisible_cost
        self.invisibility_timer = invisibility_timer
    

    def move(self, keys): # move
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
            
    def attack(self,target):#assain  unique crit attack mechanic it ignores defense an is a one in 16 proability
        if random.random() < self.crit_chance:
           damage = self.attack*self.crit_multiplier
           print(f"Critical hit! {self.name} dealt {damage} damage to {target.name}.")
        else:
            damage = max(self.attack - target.defense, 0)
        target.hp -= damage
        target.hp = max(target.hp, 0)
        if self.invisibility:
            self.invisibility = False
            print(f"{self.name} is no longer invisible after attacking!")
        
     # def enemy_attack(self, target):
    #     if getattr(target, "invisibility", False):
    #         if random.random() < 1/10:  # 10% chance to hit an invisible target
    #             damage = max(self.attack - target.defense, 0)
    #             target.hp -= damage
    #             target.hp = max(target.hp, 0)
    #             target.invisible = False  # Target becomes visible after being hit
    #             print(f"{target.name} is no longer invisible!")
    #         else:# miss entirely no damage taken
    #             print(f"{target.name} missed {self.name} because they are invisible!")
    #This code is for mobs attacking the assassin while invisible 
# invisibility skill for the assain class
    def update_invisbility(self, current_time):# this is supposed to drain 3 mana from the player every second while invisible and make them visible if they run out of mana or if they attack or get attacked
        if self.invisibility:
            if current_time - self.invisibility_timer >= 1000:  # 1second
                self.mana -= self.invisible_cost
                self.invisibility_timer = current_time
                if self.mana <= 0:
                    self.mana = 0
                    self.invisibility = False
                    print(f"{self.name} is no longer invisible due to lack of mana!")
            self.image.set_alpha(128)  # Set player character transparency to 50% whilst invisible
        else:
            self.image.set_alpha(255)  # Set player character transparency to 100%  whens invisibility ends
            
    def toggle_invisbility(self, current_time):
        if self.invisibility:
            self.invisibility = False
        else:
            if self.mana > 0:
                self.invisibility = True
                self.invisibility_timer = pygame.time.get_ticks()
              
# posion strike skill
    def apply_poison(self, target, ticks, duration, mana_cost=20): # this is the poison effect that will be applied to the target and will last for a certain amount of time
        if self.mana < mana_cost:
            print(f"{self.name} does not have enough mana to use Poison Strike!")
            return
        self.mana -= mana_cost
        target.poison = True
        target.poison_damage = max(int(target.max_hp) // 32, 1) # DEALS  1/32 OF MAX HP AS POISON DAMAGE
        target.poison_ticks_left = duration
        target.poison_tick_timer = pygame.time.get_ticks()
    
    def update_poison(self, target, current_time): # this is the poison effect that will be applied to the target and will last for a certain amount of time
        if target.poison:
            if current_time - target.poison_tick_timer >= 1000:  # 1 second
                target.hp -= target.poison_damage
                target.poison_ticks_left -= 1
                target.poison_tick_timer = current_time
                if target.poison_ticks_left <= 0:
                    target.poison = False
                    print(f"{target.name} is no longer poisoned!")
                    
        if self.invisibility:
            self.invisibility = False
            print(f"{self.name} is no longer invisible after attacking!")
            
# double strike skilll
            
    def double_strike(self, target, mana_cost=20): # this is the double strike ability that will be applied to the target 
        if self.mana < mana_cost:
            print(f"{self.name} does not have enough mana to use Double Strike!")
            return
        total_damage = 0
        for hit_number in range(1, 3):  # Two hits
            if random.random() < self.crit_chance:
                damage = self.attack * self.crit_multiplier
                print(f"Hit {hit_number}: Critical! {self.name} dealt {damage} damage to {target.name}.")
            else:
                damage = max(self.attack - target.defense, 0)
                print(f"Hit {hit_number}: {self.name} dealt {damage} damage to {target.name}.")
            
            target.hp -= damage
            target.hp = max(target.hp, 0)
            total_damage += damage
            
            if not target.is_alive():
                break  # Stop if the target is defeated
            
        if self.invisibility:
            self.invisibility = False
        # #  is no longer invisible after attacking!")
        
        print(f"{self.name} dealt a total of {total_damage} damage to {target.name} with Double Strike!")


    def annihilation_strike(self, target, current_time): # this is the annihilation strike ability that will be applied to the target
        if current_time < self.ult_ready_timer:
            remaining = (self.ult_ready_timer - current_time) // 1000
            print(f"Annihilation Strike is on cooldown! {remaining} seconds remaining.")
            
        if target.hp < target.max_hp * 0.10:
            target.hp = 0
            self.ult_ready_timer = current_time + self.ult_cooldown
            print(f"{self.name} used Annihilation Strike! {target.name} has been Slain!")
            if self.invisibility:
                self.invisibility = False
                print(f"{self.name} is no longer invisible after attacking!")
        else:
            print(f"{target.name} is not weak enough for Annihilation Strike! Target must be below 10% HP.")



BLACK = (0, 0, 0) #Background color



def load_image(filename, size):
    surf = pygame.image.load(filename).convert_alpha()
    return pygame.transform.smoothscale(surf, size)

class Start_button(pygame.sprite.Sprite): #Start button class
    def __init__(self):
        super().__init__()
        
        try:
           self.image = load_image("Start_button2.png", (400, 175))
           print("Start button file loaded successfully")
        except FileNotFoundError:
            print("Error: Start button file not found.")
        self.rect = self.image.get_rect()
        self.rect.x = 500
        self.rect.y = 100
    def on_click(self):
        print("Start Pressed!")


class Character_button(pygame.sprite.Sprite): #Character button class
    def __init__(self):
        super().__init__()
        
        try:
            self.image = load_image("Select_character_button2.png", (450, 200))
            print("Select Character file loaded successfully")
        except pygame.error as e:
            print(f"Error loading Select Character file: {e}")
        self.rect = self.image.get_rect()
        self.rect.x = 500
        self.rect.y = 350
    def on_click(self):
        print("Select Character Pressed!")

class Menu_Background(pygame.sprite.Sprite): #Menu background class
    def __init__(self):
        super().__init__()
        
        try:
            self.image = load_image("Menu_background.png", (WIDTH, HEIGHT))
            print("Menu background file loaded successfully")
        except pygame.error as e:
            print(f"Error loading Menu background file: {e}")
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

class Character_display(pygame.sprite.Sprite): #Character display class
    def __init__(self):
        super().__init__()
        
        try:
            self.image = load_image("Character Border.png", (450, 600))
            print("Character Border file loaded successfully")
        except pygame.error as e:
            print(f"Error loading Character Border file: {e}")
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
