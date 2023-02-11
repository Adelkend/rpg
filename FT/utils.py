import pygame
import engine, textures
import math

pygame.init()

font = pygame.font.Font("fonts\\KellySlab-Regular.ttf", 20)

class generate_window():
    def __init__(self):
        self.size = self.width, self.height = 1000, 600
        self.window_title = "\tTBD"
        pygame.display.set_caption(self.window_title)
        self.screen = pygame.display.set_mode(self.size)
        self.font = font
        self.surface = pygame.display.get_surface()

# --- CONSTANTS ---

colors  =   {"red": (255, 0, 0),
            "green": (0, 255, 0),
            "white": (255, 255, 255),
            "black": (0, 0, 0),
            "grey": (61, 59, 52),
            "bright_red": (155, 0, 56),
            "purple" : (205, 48, 238),
            "green" : (175, 251, 205)
            }

def drawText(screen, t, x, y, size, color):
    font = pygame.font.Font("fonts\\KellySlab-Regular.ttf", size)
    text = font.render(t, True, color)
    text_rectangle = text.get_rect()
    text_rectangle.topleft = (x, y)
    screen.blit(text, text_rectangle)

def movement(player, camera):
    keys = pygame.key.get_pressed()

    (posX, posY) = (player.positionX, player.positionY)

    # a=left
    if keys[pygame.K_a]:
        camera.camera_move = 4
        player.side = 'left'
    # d=right
    if keys[pygame.K_d]:
        camera.camera_move = 3
        player.side = 'right'
    # w=up
    if keys[pygame.K_w]:
        camera.camera_move = 2
    # s=down
    if keys[pygame.K_s]:
        camera.camera_move = 1
    if keys[pygame.K_w] and keys[pygame.K_d]:
        camera.camera_move = 5
        player.side = 'right'
    if keys[pygame.K_w] and keys[pygame.K_a]:
        camera.camera_move = 6
        player.side = 'left'
    if keys[pygame.K_s] and keys[pygame.K_d]:
        camera.camera_move = 7
        player.side = 'right'
    if keys[pygame.K_s] and keys[pygame.K_a]:
        camera.camera_move = 8
        player.side = 'left'

def spell(player):
    keys = pygame.key.get_pressed()
    
    # f=fireball
    if keys[pygame.K_f]:
        f = fireball(player, (player.positionX + 40, player.positionY + 15))
        player.can_cast = False
        return f

    return None

# --- IMAGES ---

walking1 = pygame.image.load('Graphics/playerwalking1.png')
walking2 = pygame.image.load('Graphics/playerwalking2.png')
walking3 = pygame.image.load('Graphics/playerwalking3.png')
walking4 = pygame.image.load('Graphics/playerwalking4.png')
walking5 = pygame.image.load('Graphics/playerwalking5.png')
coin1 = pygame.image.load('Graphics/coin1.png')
hq = pygame.image.load('Graphics/ft_hq.png')
hq2 = pygame.image.load('Graphics/ft_hq2.png')
natsu_fireball = pygame.image.load('Graphics/fireball.png')
fireball_icon = pygame.image.load('Graphics/fireball_icon.png')
fireball_icon1 = pygame.image.load('Graphics/fireball_icon1.png')
fireball_icon2 = pygame.image.load('Graphics/fireball_icon2.png')
fireball_icon3 = pygame.image.load('Graphics/fireball_icon3.png')
fireball_icon4 = pygame.image.load('Graphics/fireball_icon4.png')

class portal(pygame.sprite.Sprite):
    def __init__(self, surface, camera, width, height, x, y):
        super().__init__()
        self.surface = surface
        self.position  = (self.x, self.y) = (x, y)
        self.size = (self.width, self.height) = (width, height)
        self.image = pygame.Surface(self.size)
        self.image.set_alpha(0)
        self.rect = pygame.Rect((self.position), self.size)
        self.cash = 0
        self.camera = camera

    def update(self):
        self.surface.blit(hq2, (self.x + self.camera.camera_x, self.y + self.camera.camera_y))
        self.rect = pygame.Rect((self.x + self.camera.camera_x, self.y + self.camera.camera_y), self.size)

# --- CHARACTERS ---

class main_character(pygame.sprite.Sprite):
    def __init__(self, surface):
        super().__init__()
        self.surface = surface
        self.position = (self.positionX, self.positionY) = (50,50)
        self.size = (self.width, self.height) = (45, 50)
        self.rect = pygame.Rect((self.position), (self.size))
        self.camera = None  
        self.cash = 0
        self.side = 'right'
        self.state = "alive"
        self.cooldown = pygame.time.Clock()
        self.cooldown_tracker = 1000
        self.can_cast = True

        # --- STATS ---
        self.hp_max = 100
        self.hp = 100

    def update(self):
        if self.side == 'left':
            walk1 = pygame.transform.flip(walking1, flip_x=True, flip_y=False)
        else:
            walk1 = walking1
        self.rect = pygame.Rect((self.positionX - self.width, self.positionY - self.height), (self.size))
        self.surface.blit(walk1, (self.positionX, self.positionY))
        pygame.draw.rect(self.surface, colors["red"], pygame.Rect((self.positionX + 5, self.positionY - 10), (50*(self.hp/self.hp_max), 5)))

def path(x, posX, posY, dirX, dirY, y):
    if (posX - dirX) != 0:
        y = ((x * (posY - dirY)) + (dirY * posX) - (dirX * posY))/(posX - dirX)
        return y
    side = math.copysign(5, (dirY - posY))
    return (y + side)

def angle(posX, posY, dirX, dirY):
    if (posX - dirX) != 0:
        m = (posY - dirY)/(posX - dirX)
        if m > 1 or m < -1:
            return m
    return 1

def angle2(posX, posY, dirX, dirY):
    if (posX - dirX) != 0:
        m = (posY - dirY)/(posX - dirX)
        return m
    return 1

class fireball(pygame.sprite.Sprite):
    def __init__(self, player, position):
        super().__init__()
        self.direction = self.dirX, self.dirY = pygame.mouse.get_pos()
        self.player = player
        self.pos = self.posX, self.posY = position
        self.position = self.x, self.y = position
        self.side = math.copysign(5, (self.dirX - self.posX))
        self.speedX = math.copysign(5, (self.dirX - self.x))
        self.rect = pygame.Rect((self.position), (32, 32))
        self.reducer = math.copysign(angle(self.posX, self.posY, self.dirX, self.dirY), 1)
        self.angle = math.degrees(math.atan(angle2(self.posX, self.posY, self.dirX, self.dirY)))
        self.damage = 20

    def update(self):
        if self.side == -5:
            image = pygame.transform.flip(natsu_fireball, flip_x=True, flip_y=False)
        else:
            image = natsu_fireball
        self.rect = pygame.Rect((self.x, self.y), (32, 32))
        self.player.surface.blit(pygame.transform.rotate(image, -self.angle), (self.x, self.y))
        self.x += (self.speedX/self.reducer); self.y = path(self.x, self.posX, self.posY, self.dirX, self.dirY, self.y)

# --- HUD ---

class coin_count(pygame.sprite.Sprite):
    def __init__(self, surface):
        super().__init__()
        self.surface = surface
        self.position  = (10,10)
        self.image = pygame.Surface((self.position))
        self.image.set_alpha(0)
        self.cash = 0

    def update(self):
        self.surface.blit(coin1, self.position)
        drawText(self.surface, str(self.cash), 60, 10, 30, colors["white"])

class encounter_detector(pygame.sprite.Sprite):
    def __init__(self, surface):
        super().__init__()
        self.surface = surface
        self.state = False

    def update(self):
        drawText(self.surface, "Encounter: " + str(self.state), 400, 10, 30, colors["white"])

class abilities_display(pygame.sprite.Sprite):
    def __init__(self, surface):
        super().__init__()
        self.surface = surface
        self.position = (950, 10)
        self.imageList = [fireball_icon1, fireball_icon2, fireball_icon3, fireball_icon4]
        self.imageIndex = 0
        self.animationTimer = 0
        self.animationSpeed = 15
        self.surface = surface
        self.cooldown = True
    
    def update(self):
        self.surface.blit(fireball_icon, self.position)
        if self.cooldown == False:
            self.animationTimer += 1
            if self.animationTimer >= self.animationSpeed:
                self.animationTimer = 0
                self.imageIndex += 1
                if self.imageIndex > len(self.imageList) - 1:
                    self.imageIndex = 0
            self.surface.blit(self.imageList[self.imageIndex], self.position)

# -- COLLECTIBLES ---

class coin(pygame.sprite.Sprite):
    def __init__(self, surface, camera, x, y):
        super().__init__()
        self.surface = surface
        self.position  = (self.x, self.y) = (x, y)
        self.rect = pygame.Rect((self.position), (32,32))
        self.camera = camera
        
    def update(self):
        self.surface.blit(coin1, (self.x + self.camera.camera_x, self.y + self.camera.camera_y))
        self.rect = pygame.Rect((self.x + self.camera.camera_x - 32, self.y + self.camera.camera_y - 32), (32,32))