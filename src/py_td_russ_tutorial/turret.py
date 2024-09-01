import pygame as pg

import constants as c

class Turret(pg.sprite.Sprite):
    def __init__(self, sprite_sheet: pg.Surface, tile_x, tile_y):
        pg.sprite.Sprite.__init__(self)
        self.range = 90
        self.cooldown = 1500
        self.last_shot = pg.time.get_ticks()
        self.selected = False

        # Position variables.
        self.tile_x = tile_x
        self.tile_y = tile_y
        # Calculate center coordinate.
        CENTER_UX = 0.5
        self.x = (self.tile_x + CENTER_UX) * c.TILE_SIZE
        self.y = (self.tile_y + CENTER_UX) * c.TILE_SIZE

        # Animation variables.
        self.sprite_sheet = sprite_sheet
        self.animation_list = self.load_images()
        self.frame_index = 0
        self.update_time = pg.time.get_ticks()

        # Update image.
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        # Create transparent circle showing range.
        self.range_image = pg.Surface((self.range * 2, self.range *2))
        black = (0, 0, 0)
        self.range_image.fill(black)
        self.range_image.set_colorkey(black)
        pg.draw.circle(
            surface=self.range_image,
            color="grey100",
            center=(self.range, self.range),
            radius=self.range
        )
        self.range_image.set_alpha(100) # Transparency.
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

    def load_images(self) -> list[pg.Surface]:
        # Extract images from sprite sheet.
        size = self.sprite_sheet.get_height()

        # If the sprite sheet is made of perfect squares,
        # we can determine the number of 'slides' at run time.
        perfect_division = self.sprite_sheet.get_width() % size
        assert perfect_division == 0
        ANIMATION_STEPS = self.sprite_sheet.get_width() // size
        # The tutorial creates a constant for this,
        # So I'll check that I got the same result.
        # assert ANIMATION_STEPS == 8
        # That passed :)
        # Is this good game dev?
        # Anticipating that the number of slides in an animation
        # could change?

        animation_list = []
        for i in range(ANIMATION_STEPS):
            temp_image = self.sprite_sheet.subsurface(
                i * size,   # left
                0,          # right
                size,       # width
                size        # height
            )
            animation_list.append(temp_image)
        assert len(animation_list) > 1
        assert isinstance(animation_list[1], pg.Surface)
        return animation_list

    def update(self):
        # Search for new target once turret has cooled down.
        if pg.time.get_ticks() - self.last_shot > self.cooldown:
            self.play_animation()

    def play_animation(self):
        # Update image.
        self.image = self.animation_list[self.frame_index]
        # Check if enough time has passed since last update.
        if pg.time.get_ticks() - self.update_time > c.ANIMATION_DELAY:
            self.update_time = pg.time.get_ticks()
            self.frame_index += 1
            # Check if animation has finished.
            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0
                # Record completed time and clear target so cooldown
                # can begin.
                self.last_shot = pg.time.get_ticks()

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if self.selected:
            surface.blit(self.range_image, self.range_rect)
