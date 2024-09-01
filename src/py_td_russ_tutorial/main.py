"""Main module for Tower Defense utilizing pygame-ce."""

import json
from pathlib import Path

import pygame as pg

import constants as c
from enemy import Enemy
from world import World
from turret import Turret
from button import Button


# Initialize Pygame.
pg.init()

# Create clock.
clock = pg.time.Clock()

# Create game window.
screen = pg.display.set_mode((c.SCREEN_WIDTH + c.SIDE_PANEL, c.SCREEN_HEIGHT))
pg.display.set_caption("Tower Defense")

# Game Variables.
placing_turrets = False
selected_turret = None

# Load images.
assets_images = Path('assets/images')
# Map.
map = pg.image.load('levels/level.png').convert_alpha()
# Turret spritesheets.
turrets = assets_images / 'turrets'
turret_sheet = pg.image.load(turrets / 'turret_1.png').convert_alpha()
# Individual turret for mouse cursor.
cursor_turret = pg.image.load(turrets / 'cursor_turret.png').convert_alpha()
# Enemies.
enemies = assets_images / 'enemies'
enemy_image = pg.image.load(enemies / 'enemy_1.png').convert_alpha()
# Buttons.
buttons = assets_images / 'buttons'
buy_turret_image = pg.image.load(buttons / 'buy_turret.png').convert_alpha()
cancel_image = pg.image.load(buttons / 'cancel.png').convert_alpha()

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
            new_turret = Turret(turret_sheet,
                            mouse_tile_x,
                            mouse_tile_y)
            turret_group.add(new_turret)

def select_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
    for turret in turret_group:
        if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
            return turret

# Create world.
world = World(world_data, map_image=map)
world.process_data()

# Create groups.
enemy_group = pg.sprite.Group()
turret_group : set[Turret] = pg.sprite.Group()

enemy = Enemy(world.waypoints, enemy_image)
enemy_group.add(enemy)

# Create buttons.
turret_button = Button(c.SCREEN_WIDTH + 30, 120, buy_turret_image,
                       single_click=True)
cancel_button = Button(c.SCREEN_WIDTH + 50, 180, cancel_image,
                       single_click=True)

# Game loop.
run = True
while run:

    clock.tick(c.FPS)

    ######################
    #region: Updating

    # Update groups.
    enemy_group.update()
    turret_group.update()

    # Highlight selected turret.
    if selected_turret:
        selected_turret.selected = True

    #endregion: Updating
    ######################

    ######################
    #region: Drawing

    screen.fill("grey100")

    # Draw level.
    world.draw(screen)

    # Draw groups.
    enemy_group.draw(screen)
    for turret in turret_group:
        turret.draw(screen)

    # Draw buttons.
    if turret_button.draw(screen):
        placing_turrets = True
    if placing_turrets:
        # Draw cursor turret.
        cursor_rect = cursor_turret.get_rect()
        cursor_pos = pg.mouse.get_pos()
        cursor_rect.center = cursor_pos
        if cursor_pos[0] <= c.SCREEN_WIDTH:
            screen.blit(cursor_turret, cursor_rect)
        if cancel_button.draw(screen):
            placing_turrets = False

    #endregion: Drawing
    ######################

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
                if placing_turrets:
                    create_turret(mouse_pos)
                else:
                    selected_turret = select_turret(mouse_pos)

    # Update display.
    pg.display.flip()

pg.quit()
