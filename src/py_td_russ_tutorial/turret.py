import pygame as pg

import constants as c

class Turret(pg.sprite.Sprite):
    def __init__(self, image: pg.Surface, tile_x, tile_y):
        pg.sprite.Sprite.__init__(self)
        self.tile_x = tile_x
        self.tile_y = tile_y
        # Calculate center coordinate.
        CENTER_UX = 0.5
        self.x = (self.tile_x + CENTER_UX) * c.TILE_SIZE
        self.y = (self.tile_y + CENTER_UX) * c.TILE_SIZE
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
