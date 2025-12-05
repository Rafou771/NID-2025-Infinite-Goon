import pygame
from platform import window

class Icon():
    MARGIN = 0.01
    TEXT = 0.2
    def __init__(
        self,
        name : str,
        font : str,
        icon : pygame.Surface,
        on_hover : tuple[3],
        on_click : tuple[3],
        text_color : tuple[3],
        url : str,
        wn_size : tuple[2],
        icon_i : int
    ):
        self.name = name
        self.text_font = font
        self.on_hover_c = on_hover
        self.on_click_c = on_click
        self.text_color = text_color
        self.url = url
        self.wn_size = wn_size
        self.icon_i = icon_i
        self.clicked = False

        self.rect = pygame.Rect(
            self.MARGIN*self.wn_size[0]*(self.icon_i+1)+self.icon_i*int(self.wn_size[0]/14),
            (self.icon_i//14)*(self.wn_size[1]//9)+(self.MARGIN*self.wn_size[1])*(self.icon_i//14+1),
            self.wn_size[0]//14,
            self.wn_size[1]//9
        )

        self.text = pygame.font.Font(self.text_font, int(self.rect.w*self.TEXT)).render(self.name, False, self.text_color)
        self.text_rect = pygame.Rect(
            self.rect.x+self.rect.w//2-self.text.get_width()//2,
            self.rect.y+self.rect.w+self.rect.h*self.MARGIN,
            self.text.get_size()[0],
            self.text.get_size()[1]
        )
        self.on_hover = lambda x, y : x >= self.rect.x and x <= self.rect.x + self.rect.w and y >= self.rect.y and y <= self.text_rect.h+self.text_rect.y
        self.icon = pygame.transform.smoothscale(icon, self.rect.size)

    def update(self, event : pygame.event.Event):
        if not event.type == pygame.MOUSEBUTTONDOWN:
            return

        x, y = pygame.mouse.get_pos()
        if event.button == 1:
            if self.on_hover(x, y):
                if self.clicked:
                    window.open(self.url, "_blank")
                self.clicked = True
            else:
                self.clicked = False
        elif self.on_hover(x, y) and event.button == 2:
            window.open(self.url, "_blank")
        else:
            self.clicked = False

    def draw(self, wn : pygame.Surface):
        wn.blit(self.icon, self.rect) # Icon draw
        wn.blit(self.text, self.text_rect) # Text draw

        x, y = pygame.mouse.get_pos()
        if self.clicked or self.on_hover(x, y):
            surface = pygame.Surface((self.rect.w, self.rect.h+self.text_rect.h+0.1*self.rect.h))
            surface.set_alpha(self.on_click_c[3] if self.clicked else self.on_hover_c[3])
            surface.fill(self.on_click_c[:3] if self.clicked else self.on_hover_c[:3])
            wn.blit(surface, self.rect.topleft)