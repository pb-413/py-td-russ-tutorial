"""Main module for Tower Defense utilizing pygame-ce."""

import pygame as pg

import constants as c


# Initialize Pygame.
pg.init()

# Create clock.
clock = pg.time.Clock()

# Create game window.
screen = pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
pg.display.set_caption("Tower Defense")

# Game loop.
run = True
while run:

    clock.tick(c.FPS)

    # Event handler.
    for event in pg.event.get():
        # Quit program.
        if event.type == pg.QUIT:
            run = False

pg.quit()
