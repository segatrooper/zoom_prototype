import pygame, logging, tile

class Rigid(tile.Tile):
    '''
    all rigid bodies that have physics simulations
    we will apply euler integration
    '''

    def __init__(self, img, dimensions, tile, logging, spawn_loc, allF=True):
        self.log = logging
        self.log.info(f"seting up Rigid for {img}")
        super().__init__(img, dimensions, tile, logging)
        self.prev = spawn_loc
        self.loc = spawn_loc
        self.allF = allF

    def define_physics(self, v0, dt):
        self.loc = [self.loc[i] + (v0[i] * dt) for i in range(2)]

    def update_position(self, force, dt, collidables, jumpable, ground=None):
        temp = self.loc.copy()
        if self.allF:
            self.loc = [(2 * self.loc[i]) - self.prev[i] + (force[i] * dt * dt) for i in range(2)]
        else:
            self.loc[1] = (2 * self.loc[1]) - self.prev[1] + (force[1] * dt * dt)
        self.prev = temp
        # collision
        # dummy position for collision detection
        rect = self.shown_tile.get_rect()
        loc = [round(a) for a in self.loc]
        rect.update(loc, rect.size)
        for i in rect.collidelistall(collidables):
            rect.update((rect.x, collidables[i].y - rect.h), rect.size)
            self.loc = [rect.x, rect.y]
            self.prev = self.loc.copy()
        jump_reset= False
        if jumpable and rect.colliderect(ground):
            rect.update((rect.x, ground.y - rect.h), rect.size)
            self.loc = [rect.x, rect.y]
            self.prev = self.loc.copy()
            jump_reset= True
        return (rect,jump_reset)
    def blitted(self, surface, rect):
        surface.blit(self.shown_tile, rect)







