from gc import collect
import pygame
import utils, engine, map_engine, entities, textures

pygame.init()

window = utils.generate_window()
music = pygame.mixer.music
music.load("score\\main.wav")
# SETAR O VOLUME NOVAMENTE PARA TESTES FUTUROS
music.set_volume(0)

# --- CONSTANTS ---

clock = pygame.time.Clock()

# --- VARIABLES ---

phase, blocked = map_engine.map.load_map("maps\\first.map")
running = True

main_sprites = pygame.sprite.Group()
player = utils.main_character(window.surface)
main_sprites.add(player)

spells = pygame.sprite.Group()

# --- CAMERA ---

camera = engine.camera(blocked, player.position)

# --- NPC, HUD and Enemies ---

hud = pygame.sprite.Group()
coin_count = utils.coin_count(window.surface)
encounter_detector = utils.encounter_detector(window.surface)
abilities_display = utils.abilities_display(window.surface)
hud.add(coin_count, encounter_detector, abilities_display)

collectibles = pygame.sprite.Group()
coin1 = utils.coin(window.surface, camera, 800, 600)
collectibles.add(coin1)

entities_sprites = pygame.sprite.Group()
dragon1 = entities.dragon(window.surface, camera, (800, 0))
dragon2 = entities.dragon(window.surface, camera, (1000, 0))
entities_sprites.add(dragon1, dragon2)

# --- SETUP ---

portals = pygame.sprite.Group()
hq = utils.portal(window.surface, camera, 1000, 500, 200, -500)
portals.add(hq)

player.positionX = (window.width/2 - player.width/2)
player.positionY = (window.height/2 - player.height/2)
music.play(-1)

# --- GAME-LOOP ---

while running:

    # --- INPUT ---

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    camera.camera_move = 0

    utils.movement(player, camera)

    player.positionX = (window.width/2 - player.width/2)
    player.positionY = (window.height/2 - player.height/2)

    # --- SPELLS ---

    spell = utils.spell(player)
    player.cooldown.tick(60)
    player.cooldown_tracker += player.cooldown.get_time()
    abilities_display.cooldown = True
    if player.cooldown_tracker >= 1000 and spell is not None:
        spells.add(spell)
        abilities_display.animationTimer = 0
        abilities_display.imageIndex = 0
        player.cooldown_tracker = 0
    elif player.cooldown_tracker < 1000:
        abilities_display.cooldown = False

    for cast in spells:
        if encounter_detector.state == True:
            for e in entities_sprites:
                if e.rect.colliderect(cast.rect):
                    e.hp -= cast.damage
                    spells.remove(cast)
                    break
        if (cast.x > (player.positionX + (window.width/2) + 10)) or (cast.x < player.positionX - (window.width/2) - 10) or (cast.y > (player.positionY + (window.height/2) + 10)) or (cast.y < player.positionY - (window.height/2) - 10):
                spells.remove(cast)
                del cast

    # --- COMBAT ---

    for e in entities_sprites:
        if e.hp <= 0:
            entities_sprites.remove(e)
            e.encounter = False
        encounter_detector.state = e.encounter
        if (e.encounter == False) and player.rect.colliderect(e.combat_radius_start):
            e.combat = True
            e.casting = True
            e.encounter = True
        elif (e.encounter == True):
            if (player.rect.colliderect(e.combat_radius_end)):
                e.combat = True
                e.casting = True
            elif (player.rect.colliderect(e.combat_radius_end)==False) and (len(e.casts)!=0):
                e.combat = False
                e.casting = True
            else:
                e.encounter = False
        else:
            e.combat = False
            e.casting = False
            e.encounter = False

        for c in e.casts:
            if player.rect.collidelist(c.rect) != -1:
                player.hp -= c.damage
                e.casts.remove(c)
                del c
                break
            if (c.posX > (player.positionX + (window.width/2) + 10)) or (c.posX < (player.positionX - (window.width/2) - (player.width) - 20)) or (c.posY > (player.positionX + (window.height/2) + 10)) or (c.posY < (player.positionY - (window.height/2) - (player.height) - 20)):
                e.casts.remove(c)
                del c
        e.cooldown.tick(60)
        
    if player.hp <= 0:
        running = False

    # --- COLLECTION ---

    for c in collectibles:
        if player.rect.colliderect(c.rect):
            collectibles.remove(c)
            coin_count.cash += 1
            player.cash += 1
            break

    # --- DRAW ---

    window.screen.fill(engine.colors["grey"])
    worldX = camera.camera_x
    worldY = camera.camera_y
    window.surface.blit(phase, (worldX, worldY))

    # --- UPDATE ---
    
    camera.update()

    main_sprites.update()
    entities_sprites.update()
    collectibles.update()
    portals.update()
    spells.update()
    hud.update()
    
    pygame.display.flip()

    clock.tick(60)

# --- QUIT ---

pygame.quit()