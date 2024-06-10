"""Main module for Tower Defense utilizing pygame-ce."""

import json
from pathlib import Path

import pygame as pg

import constants as c
from enemy import Enemy
from world import World
from turret import Turret


# Initialize Pygame.
pg.init()

# Create clock.
clock = pg.time.Clock()

# Create game window.
screen = pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
pg.display.set_caption("Tower Defense")

# Load images.
assets_images = Path('assets/images')
# Map.
map = pg.image.load('levels/level.png').convert_alpha()
# Individual turret for mouse cursor.
turrets = assets_images / 'turrets'
cursor_turret = pg.image.load(turrets / 'cursor_turret.png').convert_alpha()
# Enemies.
enemies = assets_images / 'enemies'
enemy_image = pg.image.load(enemies / 'enemy_1.png').convert_alpha()

# Load json data for level.
with open('levels/level.tmj') as file:
    world_data = json.load(file)

def create_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
    # Calculate the sequential tile number.
    mouse_tile_num = (mouse_tile_y * c.COLUMNS) + mouse_tile_x
    # Check if that tile is grass.
    if world.tilemap[mouse_tile_num] == 7:
        # Check that there isn't already a turret there.
        space_is_free = True
        for turret in turret_group:
            if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                space_is_free = False
        # If free, create turret.
        if space_is_free:
            new_turret = Turret(cursor_turret,
                            mouse_tile_x,
                            mouse_tile_y)
            turret_group.add(new_turret)

# Create world.
world = World(world_data, map_image=map)
world.process_data()

# Create groups.
enemy_group = pg.sprite.Group()
turret_group : set[Turret] = pg.sprite.Group()

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
    turret_group.draw(screen)

    # Event handler.
    for event in pg.event.get():
        # Quit program.
        if event.type == pg.QUIT:
            run = False
        # Mouse event.
        if (    event.type == pg.MOUSEBUTTONDOWN
                and event.button == 1   ):
            mouse_pos = pg.mouse.get_pos()
            # Check mouse position is on the map.
            if (    mouse_pos[0] < c.SCREEN_WIDTH
                    and mouse_pos[1] < c.SCREEN_HEIGHT  ):
                create_turret(mouse_pos)

    # Update display.
    pg.display.flip()

pg.quit()
