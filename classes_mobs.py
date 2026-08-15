import pygame
import random  # for crit chance
import os
import math
pygame.init()
pygame.mixer.init()
import sys

WIDTH= 600
HEIGHT = 1000


def load_image(sprite_path, size):
    """Load and scale an image from the given sprite_path."""
    try:
        image = pygame.image.load(sprite_path)
        image = pygame.transform.scale(image, size)
        return image
    except (FileNotFoundError, pygame.error) as e:
        print(f"Warning: Could not load image from {sprite_path}: {e}")
        # Return a default placeholder surface
        placeholder = pygame.Surface(size)
        placeholder.fill((128, 128, 128))
        return placeholder

def load_spritesheet(path, frame_width, frame_height, num_frames, row=0, scale=None):
    """Slice num_frames horizontally from a given row of a spritesheet."""
    try:
        sheet = pygame.image.load(path).convert_alpha()
    except (FileNotFoundError, pygame.error) as e:
        print(f"Warning: could not load spritesheet {path}: {e}")
        placeholder = pygame.Surface(scale if scale else (frame_width, frame_height))
        placeholder.fill((128, 128, 128))
        return [placeholder]

    frames = []
    for i in range(num_frames):
        rect = pygame.Rect(i * frame_width, row * frame_height, frame_width, frame_height)
        frame = sheet.subsurface(rect).copy()
        if scale:
            frame = pygame.transform.scale(frame, scale)
        frames.append(frame)
    return frames
# ---------------------------------------------------------------------------
# Shared summon stat table -- moved to module level so any class can see it
# ---------------------------------------------------------------------------
SUMMON_TYPE = {
    "tengu":       {"hp": 120, "attack": 26, "defense": 12, "speed": 16, "magicpower": 24},
    "kitsune":     {"hp": 90,  "attack": 12, "defense": 8,  "speed": 12, "magicpower": 34},
    "crow_tengu":  {"hp": 100, "attack": 18, "defense": 8,  "speed": 30, "magicpower": 14},
}

ULT_SUMMON_TYPE = {
    "Titan": {"hp": 320, "attack": 50, "defense": 25, "speed": 40, "magicpower": 50}
}
#Mobs stat table#
MOBS_TYPE = {
    "goblin": {
        "hp": 40, "attack": 12, "magicpower": 4, "defense": 6, "speed": 8,
        "mana": 20, "mana_regen": 2, "can_poison": False,
        "sprite_sheet": "Goblin_Sheet.png", "frame_size": (64, 64),
        "animations": {
            "idle":   {"row": 0, "frames": 4, "fps": 6},
            "walk":   {"row": 1, "frames": 6, "fps": 10},
            "attack": {"row": 2, "frames": 5, "fps": 12},
            "hurt":   {"row": 3, "frames": 2, "fps": 8},
            "death":  {"row": 4, "frames": 6, "fps": 8},
        },
    },
    "poison_snake": {
        "hp": 60, "attack": 8, "magicpower": 10, "defense": 4, "speed": 14,
        "mana": 30, "mana_regen": 3, "can_poison": True,
        "sprite_sheet": "Spider_Sheet.png", "frame_size": (48, 48),
        "animations": {
            "idle":   {"row": 0, "frames": 4, "fps": 6},
            "walk":   {"row": 1, "frames": 6, "fps": 12},
            "attack": {"row": 2, "frames": 4, "fps": 14},
            "hurt":   {"row": 3, "frames": 2, "fps": 8},
            "death":  {"row": 4, "frames": 5, "fps": 8},
        },
    },
    "crow": {
        "hp": 180, "attack": 22, "magicpower": 2, "defense": 14, "speed": 5,
        "mana": 0, "mana_regen": 0, "can_poison": False,
        "sprite_sheet": "OrcBrute_Sheet.png", "frame_size": (80, 80),
        "animations": {
            "idle":   {"row": 0, "frames": 4, "fps": 5},
            "walk":   {"row": 1, "frames": 6, "fps": 8},
            "attack": {"row": 2, "frames": 6, "fps": 10},
            "hurt":   {"row": 3, "frames": 2, "fps": 6},
            "death":  {"row": 4, "frames": 7, "fps": 7},
        },
    },
    "healthy_mushroom": {
        "hp": 20, "attack": 2, "magicpower": 2, "defense": 4, "speed": 5,
        "mana": 0, "mana_regen": 0, "can_poison": False,
        "sprite_sheet": "OrcBrute_Sheet.png", "frame_size": (80, 80),
        "animations": {
            "idle":   {"row": 0, "frames": 4, "fps": 5},
            "walk":   {"row": 1, "frames": 6, "fps": 8},
            "attack": {"row": 2, "frames": 6, "fps": 10},
            "hurt":   {"row": 3, "frames": 2, "fps": 6},
            "death":  {"row": 4, "frames": 7, "fps": 7},
        },
    },
    "dead_mushroom": {
        "hp": 20, "attack": 2, "magicpower": 2, "defense": 4, "speed": 5,
        "mana": 0, "mana_regen": 0, "can_poison": True,
        "sprite_sheet": "OrcBrute_Sheet.png", "frame_size": (80, 80),
        "animations": {
            "idle":   {"row": 0, "frames": 4, "fps": 5},
            "walk":   {"row": 1, "frames": 6, "fps": 8},
            "attack": {"row": 2, "frames": 6, "fps": 10},
            "hurt":   {"row": 3, "frames": 2, "fps": 6},
            "death":  {"row": 4, "frames": 7, "fps": 7},
        },
    },
    "flying_eye": {                              #vampire dungeon
        "hp": 20, "attack": 2, "magicpower": 2, "defense": 4, "speed": 12,
        "mana": 0, "mana_regen": 0, "can_poison": False,
        "sprite_sheet": "OrcBrute_Sheet.png", "frame_size": (80, 80),
        "animations": {
            "idle":   {"row": 0, "frames": 4, "fps": 5},
            "walk":   {"row": 1, "frames": 6, "fps": 8},
            "attack": {"row": 2, "frames": 6, "fps": 10},
            "hurt":   {"row": 3, "frames": 2, "fps": 6},
            "death":  {"row": 4, "frames": 7, "fps": 7},
        },
    },
    "giant_fly": {
        "hp": 20, "attack": 2, "magicpower": 2, "defense": 4, "speed": 8,
        "mana": 0, "mana_regen": 0, "can_poison": True,
        "sprite_sheet": "OrcBrute_Sheet.png", "frame_size": (80, 80),
        "animations": {
            "idle":   {"row": 0, "frames": 4, "fps": 5},
            "walk":   {"row": 1, "frames": 6, "fps": 8},
            "attack": {"row": 2, "frames": 6, "fps": 10},
            "hurt":   {"row": 3, "frames": 2, "fps": 6},
            "death":  {"row": 4, "frames": 7, "fps": 7},
        },
    },
    "skeleton": {
        "hp": 80, "attack": 12, "magicpower": 2, "defense": 4, "speed": 8,
        "mana": 0, "mana_regen": 0, "can_poison": False,
        "sprite_sheet": "OrcBrute_Sheet.png", "frame_size": (80, 80),
        "animations": {
            "idle":   {"row": 0, "frames": 4, "fps": 5},
            "walk":   {"row": 1, "frames": 6, "fps": 8},
            "attack": {"row": 2, "frames": 6, "fps": 10},
            "hurt":   {"row": 3, "frames": 2, "fps": 6},
            "death":  {"row": 4, "frames": 7, "fps": 7},
        },
    },
}   

Boss_Type = {
    "Stone Golem":       {"hp": 300, "attack": 10, "defense": 32, "speed": 3, "magicpower": 24},
    "Vampire":     {"hp": 300,  "attack": 12, "defense": 8,  "speed": 12, "magicpower": 34},
    "WereWolf":  {"hp": 300, "attack": 18, "defense": 8,  "speed": 30, "magicpower": 14},
    "keon_boss": {"hp": 320, "attack": 26, "defense": 12, "speed": 10, "magicpower": 10},
}
# ---------------------------------------------------------------------------
# Classes
# ---------------------------------------------------------------------------
class Characters(pygame.sprite.Sprite):
    def __init__(self, name, load_sprite, size, x, y, hp=100, attack=10, magicpower=10,
                 speed=10, mana=100, defense=5, mana_regen=5,
                 poison=False, poison_damage=0, poison_ticks_left=5, poison_tick_timer=0,
                 ult_cooldown=60000, ult_ready_timer=0, image=None):
        super().__init__()
        self.name = name
        self.image = image if image is not None else load_image(load_sprite, size)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hp = hp
        self.max_hp = hp
        self.atk = attack
        self.speed = speed
        self.mana = mana
        self.defense = defense
        self.magicpower = magicpower
        self.mana_regen = mana_regen
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

    def move(self, keys):  # move
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed

    def attack_target(self, target):
        damage = max(self.atk - target.defense, 0)
        target.hp -= damage
        target.hp = max(target.hp, 0)
        print(f"{self.name} dealt {damage} damage to {target.name}")


class Mobs(Characters):
    def __init__(self, mob_type, x, y, size=None):
        if mob_type not in MOBS_TYPE:
            raise ValueError(f"'{mob_type}' is not a defined mob type in MOBS_TYPE.")
        stats = MOBS_TYPE[mob_type]
        frame_size = size if size is not None else stats["frame_size"]

        self.mob_type = mob_type
        self.animations = {
            anim_name: load_spritesheet(
                stats["sprite_sheet"], stats["frame_size"][0], stats["frame_size"][1],
                anim_data["frames"], row=anim_data["row"], scale=frame_size,
            )
            for anim_name, anim_data in stats["animations"].items()
        }
        self.animation_fps = {name: data["fps"] for name, data in stats["animations"].items()}
        self.current_animation = "idle"
        self.frame_index = 0
        self.animation_timer = 0
        self.facing_right = True
        self.dying = False

        super().__init__(
            name=mob_type, load_sprite=None, size=frame_size, x=x, y=y,
            hp=stats["hp"], attack=stats["attack"], magicpower=stats["magicpower"],
            speed=stats["speed"], mana=stats["mana"], defense=stats["defense"],
            mana_regen=stats["mana_regen"], image=self.animations["idle"][0],
        )

        self.can_poison = stats["can_poison"]

        # AI / aggro tracking
        self.aggro_range = 200
        self.attack_range = 50
        self.attack_cooldown = 1500
        self.last_attack_time = 0
        self.state = "idle"

    # --- animation ---------------------------------------------------
    def set_animation(self, name):
        if name == self.current_animation or name not in self.animations:
            return
        self.current_animation = name
        self.frame_index = 0
        self.animation_timer = pygame.time.get_ticks()

    def update_animation(self, current_time):
        frames = self.animations[self.current_animation]
        fps = self.animation_fps.get(self.current_animation, 8)
        frame_duration = 1000 / fps

        if current_time - self.animation_timer >= frame_duration:
            self.animation_timer = current_time
            if self.current_animation == "death":
                self.frame_index = min(self.frame_index + 1, len(frames) - 1)
            else:
                self.frame_index = (self.frame_index + 1) % len(frames)

        frame = frames[self.frame_index]
        self.image = frame if self.facing_right else pygame.transform.flip(frame, True, False)

    def take_damage(self, amount):
        reduced = super().take_damage(amount)
        if self.hp <= 0:
            self.dying = True
            self.set_animation("death")
        elif self.current_animation not in ("attack", "hurt"):
            self.set_animation("hurt")
        return reduced

    # --- combat -------------------------------------------------------
    def enemy_attack(self, target):
        if getattr(target, "invisibility", False):
            if random.random() < 1 / 10:  # 10% chance to hit an invisible target
                damage = max(self.atk - target.defense, 0)
                target.hp -= damage
                target.hp = max(target.hp, 0)
                target.invisibility = False
                print(f"{target.name} is no longer invisible!")
                self._try_poison(target)
            else:
                print(f"{self.name} missed {target.name} because they are invisible!")
        else:
            damage = max(self.atk - target.defense, 0)
            target.hp -= damage
            target.hp = max(target.hp, 0)
            self._try_poison(target)

    def _try_poison(self, target):
        if self.can_poison:
            target.poison = True
            target.poison_damage = max(int(target.max_hp) // 32, 1)
            target.poison_ticks_left = 5
            target.poison_tick_timer = pygame.time.get_ticks()
            print(f"{target.name} has been poisoned by {self.name}!")

    # --- AI -------------------------------------------------------------
    def update_ai(self, player, current_time):
        if self.dying:
            self.update_animation(current_time)
            return

        if getattr(player, "invisibility", False):
            if self.state == "attacking":
                if current_time - self.last_attack_time >= self.attack_cooldown:
                    self.enemy_attack(player)
                    self.last_attack_time = current_time
                self.state = "idle"
            else:
                self.state = "idle"
            self.set_animation("idle")
            self.update_animation(current_time)
            return

        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = math.hypot(dx, dy)

        if distance <= self.attack_range:
            self.state = "attacking"
        elif distance <= self.aggro_range:
            self.state = "chasing"
        else:
            self.state = "idle"

        if self.state == "chasing":
            if distance != 0:
                dx /= distance
                dy /= distance
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed
            self.facing_right = dx >= 0
            self.set_animation("walk")
        elif self.state == "attacking":
            self.set_animation("attack")
            if current_time - self.last_attack_time >= self.attack_cooldown:
                self.enemy_attack(player)
                self.last_attack_time = current_time
        else:
            self.set_animation("idle")

        self.update_animation(current_time)

class Vampire3boss(Mobs):
    def __init__(self, name, load_sprite, size, x, y, hp=500, attack=20, magicpower=20,
                 speed=15, mana=200, defense=10, mana_regen=10,
                 poison_ticks=0, poison_tick_timer=0, poison_damage=0, can_poison=False,
                 attack_animation=None, death_animation=None, idle_animation=None,
                 walk_animation=None, run_animation=None, hurt_animation=None):
        super().__init__(name=name, load_sprite=load_sprite, size=size, x=x, y=y, hp=hp,
                          attack=attack, magicpower=magicpower, speed=speed, mana=mana,
                          defense=defense, mana_regen=mana_regen, poison_ticks=poison_ticks,
                          poison_tick_timer=poison_tick_timer, poison_damage=poison_damage,
                          can_poison=can_poison)
        self.attack_animation = attack_animation if attack_animation is not None else []
        self.death_animation = death_animation if death_animation is not None else []
        self.idle_animation = idle_animation if idle_animation is not None else []
        self.walk_animation = walk_animation if walk_animation is not None else []
        self.run_animation = run_animation if run_animation is not None else []
        self.hurt_animation = hurt_animation if hurt_animation is not None else []

    def load_vampire3_grid(self, filename, cols=12, rows=4, scale=4):
        pass

    def animate(self):
        self.attack_animation = [load_image("Vampires3_Attack_full.png", (100, 100))]
        self.death_animation = [load_image("Vampires3_Death_full.png", (100, 100))]
        self.idle_animation = [load_image("Vampires3_Idle_full.png", (100, 100))]
        self.walk_animation = [load_image("Vampires3_Walk_full.png", (100, 100))]
        self.run_animation = [load_image("Vampires3_Run_full.png", (100, 100))]
        self.hurt_animation = [load_image("Vampires3_Hurt_full.png", (100, 100))]


class Assain(Characters):  # Assassin class, features and skills
    def __init__(self, name, player_sprite, size, x, y, hp=150, attack=30, magicpower=10,
                 speed=35, mana=150, defense=12, mana_regen=5,
                 crit_chance=0.0625, crit_multiplier=1.5,
                 invisibility=False, invisible_cost=3, invisibility_timer=0):
        super().__init__(name=name, load_sprite=player_sprite, size=size, x=x, y=y, hp=hp,
                          attack=attack, magicpower=magicpower, speed=speed, mana=mana,
                          defense=defense, mana_regen=mana_regen)
        self.crit_chance = crit_chance
        self.crit_multiplier = crit_multiplier
        self.invisibility = invisibility
        self.invisible_cost = invisible_cost
        self.invisibility_timer = invisibility_timer

    def basic_attack(self, target):  # left-click basic attack -- can crit, 1 in 16 by default
        base_damage = (self.atk * 0.30) + self.magicpower
        if random.random() < self.crit_chance:
            # crits ignore defense entirely
            damage = base_damage * self.crit_multiplier
            target.hp -= damage
            target.hp = max(target.hp, 0)
            damage_dealt = damage
            print(f"Critical hit! {self.name}'s basic attack dealt {damage_dealt:.1f} damage to {target.name}.")
        else:
            damage_dealt = target.take_damage(base_damage)
            print(f"{self.name}'s basic attack dealt {damage_dealt} damage to {target.name}.")

        if self.invisibility:
            self.invisibility = False
            print(f"{self.name} is no longer invisible after attacking!")

        return damage_dealt

    def update_invisibility(self, current_time):
        if self.invisibility:
            if current_time - self.invisibility_timer >= 1000:  # 1 second
                self.mana -= self.invisible_cost
                self.invisibility_timer = current_time
                if self.mana <= 0:
                    self.mana = 0
                    self.invisibility = False
                    print(f"{self.name} is no longer invisible due to lack of mana!")
            self.image.set_alpha(128)
        else:
            self.image.set_alpha(255)

    def toggle_invisibility(self):
        if self.invisibility:
            self.invisibility = False
        else:
            if self.mana > 0:
                self.invisibility = True
                self.invisibility_timer = pygame.time.get_ticks()

    def apply_poison(self, target, duration, mana_cost=20):
        if self.mana < mana_cost:
            print(f"{self.name} does not have enough mana to use Poison Strike!")
            return
        self.mana -= mana_cost
        target.poison = True
        target.poison_damage = max(int(target.max_hp) // 32, 1)
        target.poison_ticks_left = duration
        target.poison_tick_timer = pygame.time.get_ticks()
        print(f"{self.name} poisons {target.name}!")

    def update_poison(self, target, current_time):
        if target.poison:
            if current_time - target.poison_tick_timer >= 1000:
                target.hp -= target.poison_damage
                target.hp = max(target.hp, 0)
                target.poison_ticks_left -= 1
                target.poison_tick_timer = current_time
                if target.poison_ticks_left <= 0:
                    target.poison = False
                    print(f"{target.name} is no longer poisoned!")

    def double_strike(self, target, mana_cost=20):
        if self.mana < mana_cost:
            print(f"{self.name} does not have enough mana to use Double Strike!")
            return
        self.mana -= mana_cost
        total_damage = 0
        for hit_number in range(1, 3):
            if random.random() < self.crit_chance:
                damage = ((self.atk + self.magicpower) * 0.6) * self.crit_multiplier
                print(f"Hit {hit_number}: Critical! {self.name} dealt {damage} damage to {target.name}.")
            else:
                damage = max((self.atk * 0.6) - target.defense, 0)
                print(f"Hit {hit_number}: {self.name} dealt {damage} damage to {target.name}.")

            target.hp -= damage
            target.hp = max(target.hp, 0)
            total_damage += damage

            if not target.is_alive():
                break

        if self.invisibility:
            self.invisibility = False
            print(f"{self.name} is no longer invisible after attacking!")

        print(f"{self.name} dealt a total of {total_damage} damage to {target.name} with Double Strike!")

    def annihilation_strike(self, target, current_time):
        if current_time < self.ult_ready_timer:
            remaining = (self.ult_ready_timer - current_time) // 1000
            print(f"Annihilation Strike is on cooldown! {remaining} seconds remaining.")
            return

        if target.hp < target.max_hp * 0.10:
            target.hp = 0
            self.ult_ready_timer = current_time + self.ult_cooldown
            print(f"{self.name} used Annihilation Strike! {target.name} has been slain!")
            if self.invisibility:
                self.invisibility = False
                print(f"{self.name} is no longer invisible after attacking!")
        else:
            print(f"{target.name} is not weak enough for Annihilation Strike! Target must be below 10% HP.")


class Summoner(Characters):
    MAX_SUMMONS = 3

    def __init__(self, name, player_sprite, size, x, y, hp=150, attack=30, magicpower=10,
                 speed=35, mana=150, defense=12, mana_regen=5, ult_cooldown=40000):
        super().__init__(name=name, load_sprite=player_sprite, size=size, x=x, y=y, hp=hp,
                          attack=attack, magicpower=magicpower, speed=speed, mana=mana,
                          defense=defense, mana_regen=mana_regen, ult_cooldown=ult_cooldown)
        self.summons = []

        self.titan_active = False
        self.titan_expire_time = 0
        self.titan_duration = 50000
        self.titan_ref = None
        self.shielded =False
        self.shield_timer = 0

    def basic_attack(self, target):  # left-click basic attack
        damage = (self.magicpower * 0.30) + self.atk
        damage_dealt = target.take_damage(damage)
        print(f"{self.name}'s basic attack dealt {damage_dealt} damage to {target.name}")
        return damage_dealt

    def summon_familiar(self, summon_type, sprite_paths, size, x, y, mana_cost=60):
        if self.titan_active:
            print("Cannot summon familiars while the Titan is active!")
            return None

        if summon_type not in SUMMON_TYPE:
            print(f"'{summon_type}' is not a summon you have access to.")
            return None

        self.summons = [s for s in self.summons if s.is_alive()]

        if len(self.summons) >= self.MAX_SUMMONS:
            print(f"{self.name} already has a summon out! Only three familiar can be active at a time.")
            return None

        if self.mana < mana_cost:
            print(f"{self.name} doesn't have enough mana to summon a familiar.")
            return None

        self.mana -= mana_cost
        new_summon = Summons(summon_type, sprite_paths[summon_type], size, x, y)
        self.summons.append(new_summon)
        print(f"{self.name} summoned a {summon_type}!")
        return new_summon
# ultimaate ability to summon a titan 
    def summon_titan(self, sprite_path, size, x, y, current_time):
        # BUG FIX: this ult previously had no cooldown at all -- it could be recast
        # instantly every time the Titan died or expired. Now it uses the standard
        # ult_cooldown/ult_ready_timer pair (40 seconds by default).
        if current_time < self.ult_ready_timer:
            remaining = (self.ult_ready_timer - current_time) // 1000
            print(f"Summon Titan is on cooldown! {remaining} seconds remaining.")
            return None

        if self.titan_active:
            print("Titan is already summoned!")
            return None

        self.summons = [s for s in self.summons if s.is_alive()]

        if len(self.summons) < 1:
            print(f"{self.name} needs at least one familiar on the field to summon Titan!")
            return None

        sacrificed_names = [s.summon_type for s in self.summons]
        self.summons.clear()
        verb = "is" if len(sacrificed_names) == 1 else "are"
        print(f"{', '.join(sacrificed_names)} {verb} sacrificed to summon the Titan!")

        new_titan = Summons("Titan", sprite_path, size, x, y, stat_table=ULT_SUMMON_TYPE)
        self.summons.append(new_titan)
        self.titan_active = True
        self.titan_expire_time = current_time + self.titan_duration
        self.titan_ref = new_titan
        self.ult_ready_timer = current_time + self.ult_cooldown
        print(f"{self.name} summons the TITAN! It will last {self.titan_duration / 1000:.0f} seconds.")
        return new_titan

    def update_titan(self, current_time):
        if self.titan_active:
            titan_died = self.titan_ref is None or not self.titan_ref.is_alive()
            timer_expired = current_time >= self.titan_expire_time

            if titan_died or timer_expired:
                if self.titan_ref in self.summons:
                    self.summons.remove(self.titan_ref)
                if titan_died:
                    print("The Titan has fallen in battle!")
                else:
                    print("The Titan's power fades -- it returns to the void.")
                self.titan_active = False
                self.titan_ref = None
   # skill 2 spell sheild blocks damage for a specifc amount of time  
    def take_damage(self, amount):
        if self.shielded:
            print(f"{self.name}'s shield negated the incoming damage!")
            return 0
        return super().take_damage(amount)
        
    def spell_shield(self,current_time, duration=5000,mana_cost=65):
        if self.shielded:
            print(f"{self.name} already has a shield")
            return False
        
        if self.mana < mana_cost:
            print(f"{self.name} does not have enough mana")
            return False
        
        self.mana -= mana_cost
        self.shielded = True
        self.shield_timer = current_time + duration
        print(f"{self.name} cast Spell shield! Immune to damage for {duration/1000:.1f} seconds.")
        return True
    
    def update_spell_shield(self, current_time):
        # expire the shield when its timer runs out
        if self.shielded and current_time >= getattr(self, 'shield_timer', 0):
            self.shielded = False
            print(f"{self.name}'s shield has faded")
  # magic bullet skill-----          
    def magic_bullet(self, target, mana_cost=25):
        if self.mana < mana_cost:
            print(f"{self.name} has insufficient mana to cast the spell")
            return 0

        self.mana -= mana_cost

        # BUG FIX: was referencing self.magic_power / self.attack, which don't exist
        # on this class (the real attributes are self.magicpower / self.atk) -- this
        # raised an AttributeError every time magic_bullet was cast.
        magic_bullet_damage = (self.magicpower + self.atk) * 0.35

        damage_dealt = target.take_damage(magic_bullet_damage)
        print(f"{self.name} casts magic bullet on {target.name} for {damage_dealt} damage")
        return damage_dealt
    # teleport skill or blink--------
    def blink(self, target_position, max_radius=200, mana_cost=20, screen_boundary=(WIDTH,HEIGHT)):
        if self.mana < mana_cost:
            print(f"{self.name} does not have enough mana to cast the skill blink")
            return False
        
        start_x, start_y = self.rect.centerx, self.rect.centery
        target_x, target_y = target_position
        
        dx = target_x - start_x
        dy = target_y - start_y
        distance = math.hypot(dx,dy)
        
        if distance == 0:
            return True
      # prevents blink from moving further that teleport radius  
        if distance > max_radius:
            ratio = max_radius / distance
            dx *= ratio
            dy *= ratio
        
        self.mana -= mana_cost
        
        new_centre_x = start_x + dx
        new_centre_y = start_y + dy
        
        if screen_boundary:
            max_w, max_h = screen_boundary
            half_w = self.rect.width // 2
            half_h = self.rect.height // 2
            new_centre_x = max(half_w, min(new_centre_x, max_w - half_w))
            new_centre_y = max(half_h, min(new_centre_y, max_h - half_h))
            
        self.rect.center = (int(new_centre_x), int(new_centre_y))
        print(f"{self.name} teleported to  {self.rect.x}, {self.rect.y}")
        
#classs for all summones----
class Summons(pygame.sprite.Sprite):
    def __init__(self, summon_type, sprite_path, size, x, y, stat_table=None):
        super().__init__()
        stat_table = stat_table if stat_table is not None else SUMMON_TYPE
        stats = stat_table[summon_type]
        self.summon_type = summon_type
        self.image = load.image(sprite_path, size)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hp = stats["hp"]
        self.max_hp = stats["hp"]
        self.atk = stats["attack"]
        self.defense = stats["defense"]
        self.speed = stats["speed"]
        self.magicpower = stats["magicpower"]

        self.aggro_range = 200
        self.attack_range = 40
        self.attack_cooldown = 1200
        self.last_attack_time = 0
        self.state = "idle"

    def is_alive(self):
        return self.hp > 0

    def attack_target(self, target):
        damage = max(self.atk + self.magicpower - target.defense, 0)
        target.hp -= damage
        target.hp = max(target.hp, 0)
        print(f"{self.summon_type} dealt {damage} damage to {target.name}")

    def summon_ai(self, enemy_group, current_time):
        nearest_enemy = None
        nearest_distance = float("inf")
        for enemy in enemy_group:
            if not enemy.is_alive():
                continue
            dx = enemy.rect.centerx - self.rect.centerx
            dy = enemy.rect.centery - self.rect.centery
            distance = math.hypot(dx, dy)
            if distance < nearest_distance:
                nearest_distance = distance
                nearest_enemy = enemy

        if nearest_enemy is None:
            self.state = "idle"
            return

        if nearest_distance <= self.attack_range:
            self.state = "attacking"
            if current_time - self.last_attack_time >= self.attack_cooldown:
                self.attack_target(nearest_enemy)
                self.last_attack_time = current_time

        elif nearest_distance <= self.aggro_range:
            self.state = "chasing"
            dx = (nearest_enemy.rect.centerx - self.rect.centerx) / nearest_distance
            dy = (nearest_enemy.rect.centery - self.rect.centery) / nearest_distance
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed
        else:
            self.state = "idle"


class MagicKnight(Characters):
    def __init__(self, name, load_sprite, size, x, y, hp=300, attack=40, magicpower=30, speed=15, mana=150, defense=8, mana_regen=5, poison=False, poison_damage=0, poison_ticks_left=5, poison_tick_timer=0, ult_cooldown=60000, ult_ready_timer=0):
        super().__init__(name, load_sprite, size, x, y, hp, attack, magicpower, speed, mana, defense, mana_regen, poison, poison_damage, poison_ticks_left, poison_tick_timer, ult_cooldown, ult_ready_timer)
        self.max_mana = self.mana
        self.mana_heart_CD = 40000  # 40 secs
        self.mana_heart_ready = 0

        # "base" atk/magicpower that Mana Surge multiplies from, so the buff can be
        # cleanly removed afterwards without compounding on repeated casts
        self.base_atk = attack
        self.base_magicpower = magicpower

        # basic attack formula is: current_atk() + current_magic_power() * basic_attack_multiplier
        # Mana Surge temporarily raises this multiplier from 0.30 to 0.55
        self.basic_attack_multiplier = 0.30

        self.mana_surge_active = False
        self.mana_surge_expire_time = 0
        self.mana_surge_duration = 10000  # 10 secs

    # passive ability- increases stats based on hp---#
    
    # 
    def current_atk(self):
        if self.hp == 1:
            return self.atk * 2.0
        elif self.hp < (self.max_hp * 0.5):
            return self.atk * 1.5
        return self.atk

    def current_magic_power(self):
        if self.hp == 1:
            return self.magicpower * 2.0
        elif self.hp < (self.max_hp * 0.5):
            return self.magicpower * 1.5
        return self.magicpower

    def basic_attack(self, target):  # left-click basic attack
        damage = self.current_atk() + (self.current_magic_power() * self.basic_attack_multiplier)
        damage_dealt = target.take_damage(damage)
        print(f"{self.name}'s basic attack dealt {damage_dealt} damage to {target.name}")
        return damage_dealt

    # skills #
    # skill one attacks someone and reduces their defense stat
    def sword_slash(self, target, mana_cost=15):
        if self.mana < mana_cost:
            print(f"{self.name} does not have enough mana")
            return 0

        self.mana -= mana_cost
        raw_damage = (self.current_atk() * 0.6) + self.current_magic_power()
        damage_dealt = target.take_damage(raw_damage)
        target.defense = max(1, target.defense - 8)
        print(f"{self.name} used skill Slash on {target.name} for {damage_dealt} and lowered their defense")
        return damage_dealt

    # skill 2 uses an attack more magic scaling and reduces speed stat
    def magic_slash(self, target, mana_cost=18):
        if self.mana < mana_cost:
            print(f"{self.name} does not have enough mana")
            return 0

        self.mana -= mana_cost
        raw_damage = (self.current_magic_power() * 0.6) + self.current_atk()
        damage_dealt = target.take_damage(raw_damage)
        target.speed = max(1, target.speed - 8)
        print(f"{self.name} used skill Magic Slash on {target.name} for {damage_dealt} and lowered their speed")
        return damage_dealt

    def mana_heart(self, current_time, mana_recovery=50):
        if current_time < self.mana_heart_ready:
            remaining = (self.mana_heart_ready - current_time) // 1000
            print(f"The mana heart is absorbing mana; it is not ready. It will be ready in {remaining} secs")
            return 0

        old_mana = self.mana
        self.mana = min(self.max_mana, self.mana + mana_recovery)
        recovered_mana = self.mana - old_mana
        print(f"{self.name} recovered mana through their mana heart")

        self.mana_heart_ready = current_time + self.mana_heart_CD
        print(f"{self.name} mana heart has recovered {recovered_mana} mana "
              f"{self.mana}/{self.max_mana} mana")
        return recovered_mana

    # ultimate -- Mana Surge: self-buff that drains all remaining mana to activate,
    # boosts atk & magicpower by 2.5x, and pumps up the basic attack's magic scaling
    # for the duration.
    def Mana_Surge(self, current_time):
        if current_time < self.ult_ready_timer:
            remaining = (self.ult_ready_timer - current_time) // 1000
            print(f"Ultimate is on cooldown please wait {remaining} secs")
            return False

        if self.mana_surge_active:
            print(f"{self.name} is already in Mana Surge!")
            return False

        if self.mana <= 0:
            print(f"{self.name} has no mana to activate Mana Surge!")
            return False

        self.mana = 0  # drains all mana to activate
        self.atk = self.base_atk * 2.5
        self.magicpower = self.base_magicpower * 2.5
        self.basic_attack_multiplier = 0.55

        self.mana_surge_active = True
        self.mana_surge_expire_time = current_time + self.mana_surge_duration
        self.ult_ready_timer = current_time + self.ult_cooldown

        print(f"{self.name} unleashes MANA SURGE! Attack surges to {self.atk:.1f} and Magic "
              f"Power to {self.magicpower:.1f} for {self.mana_surge_duration / 1000:.0f} seconds!")
        return True

    def update_mana_surge(self, current_time):
        if self.mana_surge_active and current_time >= self.mana_surge_expire_time:
            self.atk = self.base_atk
            self.magicpower = self.base_magicpower
            self.basic_attack_multiplier = 0.30
            self.mana_surge_active = False
            print(f"{self.name}'s Mana Surge fades. Stats return to normal.")


class Gladiator(Characters):
    def __init__(self, name, load_sprite, size, x, y, hp=100, attack=10, magicpower=10,
                 speed=10, mana=100, defense=5, mana_regen=5,
                 poison=False, poison_damage=0, poison_ticks_left=5, poison_tick_timer=0,
                 ult_cooldown=40000, ult_ready_timer=0):
        super().__init__(name=name, load_sprite=load_sprite, size=size, x=x, y=y, hp=hp,
                          attack=attack, magicpower=magicpower, speed=speed, mana=mana,
                          defense=defense, mana_regen=mana_regen, poison=poison,
                          poison_damage=poison_damage, poison_ticks_left=poison_ticks_left,
                          poison_tick_timer=poison_tick_timer, ult_cooldown=ult_cooldown,
                          ult_ready_timer=ult_ready_timer)
        self.kill_count = 0
        self.valor_stacks = 0
        self.valor_max_stacks = 73   # max stacks of Valor

        # "base" stats Valor permanently grows -- effective self.atk/self.defense/self.speed
        # are derived from these so temporary buffs (Charge, Last Stand) don't get lost
        # or compounded when they expire.
        self.base_atk = attack
        self.base_defense = defense
        self.base_speed = speed

        # Charge (skill 3) tracking
        self.charge_active = False
        self.charge_speed_bonus = 20   # swap to 15 if you want the weaker version
        self.charge_mana_cost_per_sec = 1
        self.charge_timer = 0

        # Last Stand (ultimate) tracking
        self.last_stand_active = False
        self.last_stand_expire_time = 0
        self.last_stand_duration = 15000   # 15 seconds

    # passive -----------------------------------------------------------
    def valor(self, enemy_name="Enemy"):
        self.kill_count += 1
        if self.valor_stacks < self.valor_max_stacks:
            self.valor_stacks += 1
            self.base_atk += 1
            self.base_defense += 1
            self.atk = self.base_atk
            if not self.last_stand_active:
                self.defense = self.base_defense
            print(f"{self.name} has slain {enemy_name}. Valor activates -- attack and defense increase.")
            print(f"Attack: {self.atk} (+1) | Defense: {self.defense} (+1) | Valor stacks: {self.valor_stacks}/{self.valor_max_stacks}")
        else:
            print(f"{self.name} has slain {enemy_name}, but Valor is already at max stacks ({self.valor_max_stacks}).")

    def basic_attack(self, target):  # left-click basic attack
        was_alive = target.is_alive()
        base_damage = (self.atk * 0.30) + self.magicpower
        damage_dealt = target.take_damage(base_damage)
        print(f"{self.name}'s basic attack dealt {damage_dealt} damage to {target.name}")
        self._resolve_valor(target, was_alive)
        return damage_dealt

    def attack_target(self, target):
        # Characters.attack_target() is inherited by every class, so without this
        # override a Gladiator killing blow landed through it would silently skip
        # Valor. Overriding it here means Valor fires on ANY kill the Gladiator
        # lands, through this, thrust, or basic_attack -- not just some of them.
        was_alive = target.is_alive()
        damage = max(self.atk - target.defense, 0)
        target.hp -= damage
        target.hp = max(target.hp, 0)
        print(f"{self.name} dealt {damage} damage to {target.name}")
        self._resolve_valor(target, was_alive)
        return damage

    def _resolve_valor(self, target, was_alive_before):
        # Centralized kill-check: only fires if the target was alive right before
        # this hit and is dead right after, so re-hitting a corpse (e.g. AoE/clicks
        # that land on an already-dead target) can never double-trigger Valor.
        if was_alive_before and not target.is_alive():
            self.valor(target.name)

    # skill 1: Thrust -----------------------------------------------------
    def thrust(self, target, mana_cost=15):
        # BUG FIX: every other skill in the file costs mana -- Thrust was missing
        # a cost check entirely and could be spammed for free.
        if self.mana < mana_cost:
            print(f"{self.name} doesn't have enough mana to use Thrust!")
            return 0
        self.mana -= mana_cost
        was_alive = target.is_alive()
        damage = max((self.atk * 1.5 + self.magicpower) - target.defense, 0)
        target.hp -= damage
        target.hp = max(target.hp, 0)
        print(f"{self.name} uses Thrust! Dealt {damage} damage to {target.name}.")
        self._resolve_valor(target, was_alive)
        return damage

    # skill 2: Rejuvenate ---------------------------------------------------
    def rejuvenate(self, mana_cost=20, heal_amount=30):
        if self.mana < mana_cost:
            print(f"{self.name} doesn't have enough mana to use Rejuvenate!")
            return
        self.mana -= mana_cost
        self.hp = min(self.hp + heal_amount, self.max_hp)
        print(f"{self.name} uses Rejuvenate! Healed {heal_amount} HP. ({self.hp}/{self.max_hp})")

    # skill 3: Charge -------------------------------------------------------
    def toggle_charge(self):
        if self.charge_active:
            self.charge_active = False
            self.speed = self.base_speed
            print(f"{self.name} stops charging. Speed returns to {self.speed}.")
        else:
            if self.mana > 0:
                self.charge_active = True
                self.speed = self.base_speed + self.charge_speed_bonus
                self.charge_timer = pygame.time.get_ticks()
                print(f"{self.name} charges! Speed increased to {self.speed}.")
            else:
                print(f"{self.name} doesn't have enough mana to Charge!")

    def update_charge(self, current_time):
        if self.charge_active:
            if current_time - self.charge_timer >= 1000:
                self.mana -= self.charge_mana_cost_per_sec
                self.charge_timer = current_time
                if self.mana <= 0:
                    self.mana = 0
                    self.charge_active = False
                    self.speed = self.base_speed
                    print(f"{self.name} runs out of mana and stops charging!")

    # ultimate: Last Stand ----------------------------------------------
    def last_stand(self, current_time):
        if current_time < self.ult_ready_timer:
            remaining = (self.ult_ready_timer - current_time) // 1000
            print(f"Last Stand is on cooldown! {remaining} seconds remaining.")
            return
        if self.hp >= 100:
            print(f"{self.name} must be below 100 HP to use Last Stand!")
            return

        self.defense = self.base_defense * 7.3
        self.last_stand_active = True
        self.last_stand_expire_time = current_time + self.last_stand_duration
        self.ult_ready_timer = current_time + self.ult_cooldown
        print(f"{self.name} uses Last Stand! Defense surges to {self.defense:.1f} for 15 seconds!")

    def update_last_stand(self, current_time):
        if self.last_stand_active and current_time >= self.last_stand_expire_time:
            self.defense = self.base_defense
            self.last_stand_active = False
            print(f"{self.name}'s Last Stand fades. Defense returns to {self.defense}.")










