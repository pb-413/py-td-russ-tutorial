"""Main module for Tower Defense utilizing pygame-ce."""

import json

import pygame as pg

import constants as c
from enemy import Enemy
from world import World


# Initialize Pygame.
pg.init()

# Create clock.
clock = pg.time.Clock()

# Create game window.
screen = pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
pg.display.set_caption("Tower Defense")

# Load images.
# Map.
map = pg.image.load('levels/level.png').convert_alpha()
# Enemies.
enemy_image = pg.image.load('assets/images/enemies/enemy_1.png').convert_alpha()

# Load json data for level.
with open('levels/level.tmj') as file:
    world_data = json.load(file)

# Create world.
world = World(world_data, map_image=map)
world.process_data()

# Create groups.
enemy_group = pg.sprite.Group()

enemy = Enemy(world.waypoints, enemy_image)
enemy_group.add(enemy)

# Game loop.
run = True
while run:

    clock.tick(c.FPS)

    screen.fill("grey100")

    # Draw level.
    world.draw(screen)

    # Draw enemy path.
    # pg.draw.lines(screen, "grey0",
    #               closed=False,
    #               points=world.waypoints)

    # Update groups.
    enemy_group.update()

    # Draw groups.
    enemy_group.draw(screen)

    # Event handler.
    for event in pg.event.get():
        # Quit program.
        if event.type == pg.QUIT:
            run = False

    # Update display.
    pg.display.flip()

pg.quit()
