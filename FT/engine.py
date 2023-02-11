import pygame
import utils, textures

pygame.init()

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

# --- CAMERA ---

class camera():
    def __init__(self, blocked, pos):
        self.camera_x, self.camera_y = pos
        self.camera_move = 0
        self.scene = "phase1"
        self.deltatime = 0.0015
        self.speed = 500
        self.blocked = blocked

    def update(self):
        (camX, camY) = (self.camera_x, self.camera_y)

        if (self.camera_move == 1):
            self.camera_y -= 2
            if textures.tiles.Blocked_At((self.camera_x, self.camera_y)):
                self.camera_y += 2
        if (self.camera_move == 2):
            self.camera_y += 2
            if textures.tiles.Blocked_At((self.camera_x, self.camera_y)):
                self.camera_y -= 2
        if (self.camera_move == 3):
            self.camera_x -= 2
        if (self.camera_move == 4):
            self.camera_x += 2
        if (self.camera_move == 5):
            self.camera_y += 2
            self.camera_x -= 2
        if (self.camera_move == 6):
            self.camera_y += 2
            self.camera_x += 2
        if (self.camera_move == 7):
            self.camera_y -= 2
            self.camera_x -= 2
        if (self.camera_move == 8):
            self.camera_y -= 2
            self.camera_x += 2

class Animations():
    def __init__(self):
        self.animationList = {}

    def add(self, state, animation):
        self.animationList[state] = animation

class Animation():
    def __init__(self, imageList):
        self.imageList = imageList
        self.imageIndex = 0
        self.animationTimer = 0
        self.animationSpeed = 10

    def update(self):
        self.animationTimer += 1
        if self.animationTimer >= self.animationSpeed:
            self.animationTimer = 0
            self.imageIndex += 1
            if self.imageIndex > len(self.imageList) - 1:
                self.imageIndex = 0

    def draw(self, screen, x, y, flipX, flipY):
        image = self.imageList[self.imageIndex]
        newWidth = int(image.get_rect().w * 1)
        newHeight = int(image.get_rect().h * 1)
        screen.blit(pygame.transform.scale(pygame.transform.flip(image, flipX, flipY), (newWidth, newHeight)), (x, y))