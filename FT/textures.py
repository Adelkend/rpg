import pygame

pygame.init()

class tiles:
    size = 32

    itens = []
    portals = []
    Blocked = []

    def Blocked_At(pos):
        if list(pos) in tiles.Blocked:
            return True
        else:
            return False

    def w_items(pos):
        if list(pos) in tiles.itens_2:
            return True
        else:
            return False

    def portal_entrance(pos):
        if list(pos) in tiles.portais:
            return True
        else:
            return False

    def Load_Texture(file, Size):
        bitmap = pygame.image.load(file)
        bitmap = pygame.transform.scale(bitmap, (Size, Size))
        surface = pygame.Surface((Size, Size), pygame.HWSURFACE | pygame.SRCALPHA)
        surface.blit(bitmap, (0, 0))
        return surface

    Black = Load_Texture("graphics\\black.png", size)
    Caminho = Load_Texture("graphics\\stone_floor.png", size)
    Floor1 = Load_Texture("graphics\\floor1.png", size)
    Floor2 = Load_Texture("graphics\\floor2.png", size)
    Floor3 = Load_Texture("graphics\\floor3.png", size)
    Wall1 = Load_Texture("graphics\\wall1.png", size)
    Wall2 = Load_Texture("graphics\\wall2.png", size)
    Wall3 = Load_Texture("graphics\\wall3.png", size)

    Blocked_Types = [Wall1, Wall2, Wall3]

    Texture_Tags = {"1": Black, "2": Caminho, "3": Floor1, "4": Floor2, "5": Floor3, "6": Wall1, "7": Wall2, "8": Wall3}