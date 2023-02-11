import pygame, math
import utils

pygame.init()
# --- IMAGES PATH ---

dragon1 = pygame.image.load('Graphics/dragon.png')

# --- SPRITE CLASSES ---

class dragon(pygame.sprite.Sprite):
    def __init__(self, surface, camera, position):
        super().__init__()
        self.surface = surface
        self.position = (self.x, self.y) = position
        self.camera = camera
        self.size = (self.width, self.height) = (100, 100)
        self.rect = pygame.Rect((self.position), (self.size))
        self.combat_radius_start = pygame.Rect((self.x - 200, self.y - 200), (self.width + 200, self.height + 200))
        self.combat_radius_end = pygame.Rect((self.x - 400, self.y - 400), (self.width + 200, self.height + 200))
        self.combat = False
        self.casting = False
        self.encounter = False
        self.cooldown = pygame.time.Clock()
        self.cooldown_tracker = 0

        # --- STATS ---
        self.hp_max = 500
        self.hp = 500

        self.casts = []

    def cast(self):
        # f = fireball(self, self.position, "down")
        f = dragon_fire_ring(self, self.position)
        return f

    def update(self):
        self.surface.blit(dragon1, (self.x + self.camera.camera_x, self.y + self.camera.camera_y))
        self.rect = pygame.Rect( (self.x + self.camera.camera_x + 15, self.y + self.camera.camera_y + 15), (self.size))
        pygame.draw.rect(self.surface, utils.colors["red"], pygame.Rect((self.x + self.camera.camera_x + 15, self.y + self.camera.camera_y - 10), (100*(self.hp/self.hp_max), 5)))
        self.combat_radius_start = pygame.Rect((self.x + self.camera.camera_x  - 200, self.y + self.camera.camera_y - 200), (self.width + 400, self.height + 400))
        self.combat_radius_end = pygame.Rect((self.x + self.camera.camera_x  - 400, self.y + self.camera.camera_y - 400), (self.width + 800, self.height + 800))
        if self.casting == True:
            if self.combat == True:
                self.cooldown_tracker += self.cooldown.get_time()
                if self.cooldown_tracker >= 1000:
                    self.cooldown_tracker = 0
                if self.cooldown_tracker == 0:
                    self.casts.append(self.cast())
            for c in self.casts:
                c.update()

# --- ENEMIES' SPELLS ---

class fireball():
    def __init__(self, mob, position, dir):
        self.mob = mob
        if dir == "up":
            self.direction = self.dirX, self.dirY = (self.mob.camera.camera_x + 0, self.mob.camera.camera_y - 100)
            self.speed = (self.speedX, self.speedY) = (0, -5); self.angle = -90
        elif dir == "down":
            self.direction = self.dirX, self.dirY = (self.mob.camera.camera_x + 0, self.mob.camera.camera_y + 100)
            self.speed = (self.speedX, self.speedY) = (0, 5); self.angle = 90
        elif dir == "right":
            self.direction = self.dirX, self.dirY = (self.mob.camera.camera_x + 100, self.mob.camera.camera_y + 0)
            self.speed = (self.speedX, self.speedY) = (5, 0); self.angle = 180
        elif dir == "left":
            self.direction = self.dirX, self.dirY = (self.mob.camera.camera_x - 100, self.mob.camera.camera_y + 0)
            self.speed = (self.speedX, self.speedY) = (-5, 0); self.angle = 0
        self.position = self.mob.position = (self.x, self.y) = position
        self.side = math.copysign(5, (self.dirX - self.x))
        self.rect = pygame.Rect((self.position), (32, 32))
        self.damage = 20

    def update(self):
        if self.side == -5:
            image = pygame.transform.flip(utils.natsu_fireball, flip_x=True, flip_y=False)
        else:
            image = utils.natsu_fireball
        (self.posX, self.posY) = (self.x + self.mob.camera.camera_x, self.y + self.mob.camera.camera_y)
        self.rect = pygame.Rect(((self.posX, self.posY + 25)), (32, 32))
        self.mob.surface.blit(pygame.transform.rotate(image, self.angle), (self.posX + 50, self.posY + 80))
        self.x += self.speedX; self.y += self.speedY

class dragon_fire_ring():
    def __init__(self, mob, position): 
        self.mob = mob
        self.position = position

        self.fireball_up = fireball(self.mob, self.position, "up")
        self.fireball_down = fireball(self.mob, self.position, "down")
        self.fireball_right = fireball(self.mob, self.position, "right")
        self.fireball_left = fireball(self.mob, self.position, "left")
        self.fireballs = [self.fireball_left, self.fireball_down, self.fireball_right, self.fireball_up]

        self.rect = [self.fireball_left.rect, self.fireball_down.rect, self.fireball_right.rect, self.fireball_up.rect]

        self.damage = self.fireball_down.damage
    def update(self):
        for f in self.fireballs:
            f.update()
        self.rect = [self.fireball_left.rect, self.fireball_down.rect, self.fireball_right.rect, self.fireball_up.rect]

        # Posição da Fireball para baixo como refência para o desaparecimento da fireball
        (self.posX, self.posY) = (self.fireball_down.posX, self.fireball_down.posY)