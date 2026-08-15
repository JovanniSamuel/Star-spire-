import pygame
import math
from classes_mobs import Assain, Summoner, Gladiator, MagicKnight, Mobs

pygame.init()


class GameStateManager:
    """Tiny state machine so gameplay.py can track its own menu/character_select/
    playing states. main-menu.py tracks its screens with a separate integer
    (Screen 0/1/2) -- the two aren't merged, this file just owns its own states
    once main-menu.py hands control over via run()."""
    def __init__(self, start_state="character_select"):
        self._state = start_state

    def get_state(self):
        return self._state

    def set_state(self, new_state):
        self._state = new_state


def get_nearest_target(source_rect, group):
    """Return the closest living sprite in group to source_rect, or None."""
    nearest = None
    nearest_distance = float("inf")
    for entity in group:
        if hasattr(entity, "is_alive") and not entity.is_alive():
            continue
        dx = entity.rect.centerx - source_rect.centerx
        dy = entity.rect.centery - source_rect.centery
        distance = math.hypot(dx, dy)
        if distance < nearest_distance:
            nearest_distance = distance
            nearest = entity
    return nearest


def run(screen, clock):
    """Runs the gameplay loop using the screen/clock main-menu.py already created,
    so this doesn't open a second window. Returns once the player quits (closes
    the window during play) -- the caller is expected to stop its own loop too."""

    BLACK = (0, 0, 0)
    game_state_manager = GameStateManager("character_select")

    # Player setup -- one instance of each playable class. Swap the sprite filenames
    # for real art whenever it's ready; load_image falls back to a gray placeholder
    # if a file is missing, so this won't crash in the meantime.
    assassin = Assain("Shadow", "assassin_sprite.png", (64, 64), 400, 300)
    summoner = Summoner("Caller", "summoner_sprite.png", (64, 64), 400, 300)
    gladiator = Gladiator("Titanguard", "gladiator_sprite.png", (64, 64), 400, 300)
    magicknight = MagicKnight("Spellblade", "magicknight_sprite.png", (64, 64), 400, 300)

    # whichever of the four is currently being controlled -- defaults to the Assassin
    # so pressing Start immediately works; the character-select screen (keys 1-4) lets
    # you swap before entering "playing"
    active_player = assassin

    # updated to the current three summon types (tengu/kitsune/crow_tengu) --
    # rabbit/lion/crow/butterfly were replaced earlier in this project
    sprite_paths = {"tengu": "tengu.png", "kitsune": "kitsune.png", "crow_tengu": "crow_tengu.png"}

    mobs_group = pygame.sprite.Group()
    mobs_group.add(Mobs("goblin", 700, 300))  # demo target -- add more/replace as needed

    # placeholders: the real main menu lives in main-menu.py. These stay empty so
    # the "menu" state here doesn't crash if it's ever reached, but menu button
    # clicks are handled by main-menu.py itself, not by this file.
    menu_sprites = pygame.sprite.Group()
    buttons = pygame.sprite.Group()

    # placeholder: wire in a real map/background sprite group here (see the
    # Forest1/Desert1/etc classes in RandomMap.py for the pattern) once floor
    # art is ready. Empty for now so playing state doesn't crash.
    floor1_group = pygame.sprite.Group()

    running = True
    while running:
        current_time = pygame.time.get_ticks()
        state = game_state_manager.get_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if state == "menu":
                    for sprite in buttons:
                        if sprite.rect.collidepoint(event.pos):
                            sprite.on_click()
                elif state == "character_select":
                    pass  # character select uses the number keys below, not clicks
                elif state == "playing":
                    # left click = basic attack for every character class
                    clicked_target = None
                    for mob in mobs_group:
                        if mob.is_alive() and mob.rect.collidepoint(event.pos):
                            clicked_target = mob
                            break
                    if clicked_target is None:
                        clicked_target = get_nearest_target(active_player.rect, mobs_group)
                    if clicked_target is not None:
                        active_player.basic_attack(clicked_target)

            if event.type == pygame.KEYDOWN:
                if state == "character_select":
                    # pick which class to play, then jump straight into the dungeon
                    if event.key == pygame.K_1:
                        active_player = assassin
                        game_state_manager.set_state("playing")
                    elif event.key == pygame.K_2:
                        active_player = summoner
                        game_state_manager.set_state("playing")
                    elif event.key == pygame.K_3:
                        active_player = gladiator
                        game_state_manager.set_state("playing")
                    elif event.key == pygame.K_4:
                        active_player = magicknight
                        game_state_manager.set_state("playing")

                elif state == "playing":
                    skill_target = get_nearest_target(active_player.rect, mobs_group)

                    if isinstance(active_player, Assain):
                        # 1: Poison Strike, 2: Double Strike, 3: Invisibility (toggle), 4: Annihilation Strike (ult)
                        if event.key == pygame.K_1 and skill_target is not None:
                            active_player.apply_poison(skill_target, duration=5)
                        elif event.key == pygame.K_2 and skill_target is not None:
                            active_player.double_strike(skill_target)
                        elif event.key == pygame.K_3:
                            active_player.toggle_invisibility()
                        elif event.key == pygame.K_4 and skill_target is not None:
                            active_player.annihilation_strike(skill_target, current_time)

                    elif isinstance(active_player, Summoner):
                        # 1: Magic Bullet, 2: Spell Shield, 3: Blink, 4: Summon Titan (ult)
                        # h/j/k: summon tengu/kitsune/crow_tengu familiars
                        if event.key == pygame.K_1 and skill_target is not None:
                            active_player.magic_bullet(skill_target)
                        elif event.key == pygame.K_2:
                            active_player.spell_shield(current_time)
                        elif event.key == pygame.K_3:
                            active_player.blink(pygame.mouse.get_pos())
                        elif event.key == pygame.K_4:
                            active_player.summon_titan("titan.png", (96, 96), active_player.rect.x,
                                                        active_player.rect.y, current_time)
                        elif event.key == pygame.K_h:
                            active_player.summon_familiar("tengu", sprite_paths, (48, 48),
                                                           active_player.rect.x - 40, active_player.rect.y)
                        elif event.key == pygame.K_j:
                            active_player.summon_familiar("kitsune", sprite_paths, (48, 48),
                                                           active_player.rect.x - 40, active_player.rect.y)
                        elif event.key == pygame.K_k:
                            active_player.summon_familiar("crow_tengu", sprite_paths, (48, 48),
                                                           active_player.rect.x - 40, active_player.rect.y)

                    elif isinstance(active_player, Gladiator):
                        # 1: Thrust, 2: Rejuvenate, 3: Charge (toggle), 4: Last Stand (ult)
                        # Valor is passive -- it has no key of its own; it fires automatically
                        # from thrust()/basic_attack() whenever a target dies.
                        if event.key == pygame.K_1 and skill_target is not None:
                            active_player.thrust(skill_target)
                        elif event.key == pygame.K_2:
                            active_player.rejuvenate()
                        elif event.key == pygame.K_3:
                            active_player.toggle_charge()
                        elif event.key == pygame.K_4:
                            active_player.last_stand(current_time)

                    elif isinstance(active_player, MagicKnight):
                        # 1: Sword Slash, 2: Magic Slash, 3: Mana Heart (passive-style regen), 4: Mana Surge (ult)
                        if event.key == pygame.K_1 and skill_target is not None:
                            active_player.sword_slash(skill_target)
                        elif event.key == pygame.K_2 and skill_target is not None:
                            active_player.magic_slash(skill_target)
                        elif event.key == pygame.K_3:
                            active_player.mana_heart(current_time)
                        elif event.key == pygame.K_4:
                            active_player.Mana_Surge(current_time)

        screen.fill(BLACK)

        if state == "menu":
            menu_sprites.update()
            menu_sprites.draw(screen)

        elif state == "character_select":
            pass  # character select screen sprites/logic go here

        elif state == "playing":
            floor1_group.update()
            floor1_group.draw(screen)

            keys = pygame.key.get_pressed()
            active_player.move(keys)  # WASD movement for whichever class is active

            # per-class passive/buff upkeep, run every frame
            if isinstance(active_player, Assain):
                active_player.update_invisibility(current_time)
                for mob in mobs_group:
                    active_player.update_poison(mob, current_time)

            elif isinstance(active_player, Summoner):
                active_player.update_titan(current_time)
                active_player.update_spell_shield(current_time)
                for summon in list(active_player.summons):
                    summon.summon_ai(mobs_group, current_time)

            elif isinstance(active_player, Gladiator):
                active_player.update_charge(current_time)
                active_player.update_last_stand(current_time)

            elif isinstance(active_player, MagicKnight):
                active_player.update_mana_surge(current_time)

            for mob in mobs_group:
                mob.update_ai(active_player, current_time)

            screen.blit(active_player.image, active_player.rect)
            mobs_group.draw(screen)
            if isinstance(active_player, Summoner):
                for summon in active_player.summons:
                    screen.blit(summon.image, summon.rect)

        pygame.display.flip()  # Update the display
        clock.tick(60)

    # no pygame.quit() here -- the caller (main-menu.py) owns the pygame lifecycle