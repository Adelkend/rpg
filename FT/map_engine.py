import pygame
import textures

class map:

    def add_tile(tile,pos,addTo):
        addTo.blit(tile,(pos[0]*textures.tiles.size,pos[1]*textures.tiles.size))

    def load_map(file):
        with open(file,"r") as mapfile:
            map_data=mapfile.read()

        # Read Tile Data
        map_data=map_data.split("-")  #Split into list of tiles

        map_size=map_data[len(map_data)-1] #Get Map Dimensions

        map_data.remove(map_size)
        map_size=map_size.split(",")
        map_size[0]=int(map_size[0]) * textures.tiles.size
        map_size[1]=int(map_size[1]) * textures.tiles.size

        tiles=[]
        tiles_blocked=[]

        for tile in range(len(map_data)):
            map_data[tile] = map_data[tile].replace("\n","")
            tiles.append(map_data[tile].split(":")) #Split pos from texture
        for tile in tiles:
            tile[0]=tile[0].split(",") #Split pos into list
            pos=tile[0]
            for blocked in textures.tiles.Blocked_Types:
                if blocked == textures.tiles.Texture_Tags[tile[1]]:
                    tiles_blocked.append((int(pos[0]), int(pos[1])))
            for p in pos:
                pos[pos.index(p)]=int(p) #convert to integer

            tiles[tiles.index(tile)]= (pos,tile[1])   #Save to tile list

        # Create Terrain

        terrain=pygame.Surface(map_size,pygame.HWSURFACE)

        for tile in tiles:
            if tile[1] in textures.tiles.Texture_Tags:
                map.add_tile(textures.tiles.Texture_Tags[tile[1]],tile[0],terrain)

            if tile[1] in textures.tiles.Blocked_Types:
                textures.tiles.Blocked.append(tile[0])

            # if tile[1] in textures.tiles.itens_types:
            #     textures.tiles.itens_2.append(tile[0])

            # if tile[1] in textures.tiles.portal_types:
            #     textures.tiles.portais.append(tile[0])

        return terrain, tiles_blocked