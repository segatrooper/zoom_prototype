import pygame, logging
class Tile:
    '''
    This is the class that takes image with multiple tiles and parses them into array of Surfaces
    '''
    def __init__(self, img_location, dimensions, frame_coords, logger):
        '''
        # input
            str img_location: directory in str form
            (int, int) dimensions: pixel dimensions of the entire img
                - can use OpenCV later to get these values independently
            (int, int) frame_coords: tile dimensions of the image, what are the layout of the tiles?

        # returns
            self.master_surface: surface of all the tiles
            self.tiles: list of all possible tiles from the image
        '''
        self.log = logger
        tile_resolution = (dimensions[0] / frame_coords[0], dimensions[1] / frame_coords[1])
        self.tile_center = [i  // 2 for i in tile_resolution ]
        self.log.info(f"tile resolution for {img_location} is {tile_resolution}")
        # this will give us the 32 * 32 that we will need, no guesswork
        # idle tile is tile 0 * 1
        self.master_surface = pygame.image.load(img_location).convert_alpha()
        # array of surfaces
        self.tiles = list()
        for y in range(frame_coords[1]):
            for x in range(frame_coords[0]):
                temp_surface = pygame.Surface(tile_resolution, pygame.SRCALPHA)
                temp_surface.blit(self.master_surface, (0,0),\
                        (x * tile_resolution[0],\
                        y * tile_resolution[1],\
                        tile_resolution[0],\
                        tile_resolution[1])\
                        )
                self.tiles.append(temp_surface)
        self.shown_tile = self.tiles[0]

    def configure_tile(self, idle, up, right, down, left, animation_speed):
        '''
        remember that all are lists for indices
        '''
        self.ani_speed = animation_speed
        self.idle = [self.tiles[i] for i in idle]
        self.left = [self.tiles[i] for i in left]
        self.right = [self.tiles[i] for i in right]
        self.up = [self.tiles[i] for i in up]
        self.down = [self.tiles[i] for i in down]
        self.orientation = 0
        self.frame = 0
        self.time = 0
        self.orient_dict = {
                    0 : self.idle,
                    1 : self.up,
                    2 : self.right,
                    3 : self.down,
                    4 : self.left,
                }
    def change_orientation(self, orient):
        '''
        oreint key:
        0: idle
        1: up
        2: right
        3: down
        4: left
        '''
        self.frame = 0
        self.orientation = orient
        self.time = 0
        self.shown_tile = self.orient_dict[self.orientation][self.frame]

    def animate(self, dt):
        self.time += dt
        if (self.time // self.ani_speed != 0):
            self.frame = int(self.frame + (self.time // self.ani_speed)) % len(self.orient_dict[self.orientation])
            self.shown_tile = self.orient_dict[self.orientation][self.frame]
            self.time = self.time % self.ani_speed
        
        

        


