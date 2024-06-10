import pygame as pg

class Button():
    def __init__(self, x, y, image: pg.Surface, single_click: bool) -> None:
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.single_click = single_click

    def draw(self, surface: pg.Surface):
        action = False
        # Get mouse position.
        pos = pg.mouse.get_pos()
        # Check mouse over and clicked.
        if self.rect.collidepoint(pos):
            left_mouse_button_pressed = pg.mouse.get_pressed()[0]
            if left_mouse_button_pressed and not self.clicked:
                action = True
                # If single click type, set clicked.
                if self.single_click: 
                    self.clicked = True

        # Check let go.
        left_mouse_button_pressed = pg.mouse.get_pressed()[0]
        if not left_mouse_button_pressed:
            self.clicked = False
        # Draw button on screen.
        surface.blit(self.image, self.rect)

        return action
