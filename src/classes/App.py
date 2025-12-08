import pygame
from typing import Dict, Literal, Any

class App():
    SIZE = (0.45, 0.60)
    HEADER = 0.03
    MARGIN = 0.02
    LABEL = 0.8
    ICON_X = (255, 0, 0, 50) # On hover icon bf color - X icon
    ICON_O = (190, 190, 190, 50) # - Other icons
    def __init__(
        self,
        name : str,
        wn_size : tuple[int, int], 
        bg_color : tuple[int, int, int, int],
        header_color : tuple[int, int, int, int],
        icons : Dict[Literal["quit", "reajust", "reduce"], pygame.Surface],
        font : str,
        text_color : tuple[int, int, int]
    ) -> None:
        self.name = name
        self.wn_size = wn_size
        self.bg_color = bg_color
        self.header_color = header_color
        self.icons = icons
        self.text_color = text_color
        self.text_font = font

        self.expanded = False
        self.toggle = False
        self.rect = pygame.Rect(
            self.wn_size[0]//2-(self.SIZE[0]*self.wn_size[0])//2, 
            self.wn_size[1]//2-((self.SIZE[1]-self.HEADER)*self.wn_size[1])//2+self.HEADER*self.wn_size[1], 
            self.SIZE[0]*self.wn_size[0],
            (self.SIZE[1]-self.HEADER)*self.wn_size[1]
        )

        self.font = pygame.font.Font(font, int(self.LABEL*self.HEADER*self.wn_size[1]))
        self.option_on_hover = lambda x, y, i: y >= self.rect.y-self.HEADER*self.wn_size[1] and y <= self.rect.y-self.HEADER*y+self.HEADER*y-self.MARGIN*self.HEADER*y and x >= self.rect.x+self.rect.width-self.rect.width*self.MARGIN*i-(self.HEADER*self.wn_size[1]-self.MARGIN*self.HEADER*self.wn_size[1])*i and x <= self.rect.x+self.rect.width-self.rect.width*self.MARGIN*i-(self.HEADER*self.wn_size[1]-self.MARGIN*self.HEADER*self.wn_size[1])*(i-1) 

    def open(self, apps : dict[str, Any]) -> None:
        for app in apps.values():
            app.suspend()
        self.toggle = True

    def reset(self) -> None:
        self.rect = pygame.Rect(
            self.wn_size[0]//2-(self.SIZE[0]*self.wn_size[0])//2, 
            self.wn_size[1]//2-((self.SIZE[1]-self.HEADER)*self.wn_size[1])//2+self.HEADER*self.wn_size[1], 
            self.SIZE[0]*self.wn_size[0],
            (self.SIZE[1]-self.HEADER)*self.wn_size[1]
        )

    def close(self) -> None:
        self.toggle = False
        self.reset()

    def suspend(self) -> None:
        self.toggle = False

    def expand(self):
        if not self.expanded:
            self.rect = pygame.Rect(
                0,
                self.HEADER*self.wn_size[1],
                self.wn_size[0],
                self.wn_size[1]-self.HEADER*self.wn_size[1]
            )
        else:
            self.reset()
        self.expanded = not self.expanded

    def update(self, event : pygame.event.Event) -> None:
        if not event.type == pygame.MOUSEBUTTONDOWN or not self.toggle:
            return

        if event.button == 1:
            if self.option_on_hover(event.pos[0], event.pos[1], 3):
                self.suspend()
            elif self.option_on_hover(event.pos[0], event.pos[1], 2):
                self.expand()
            elif self.option_on_hover(event.pos[0], event.pos[1], 1):
                self.close()

    def draw(self, wn : pygame.Surface, mouse_pos : tuple[int, int]) -> None:
        if not self.toggle: # App icon
            return

        ## Bg draw
        for color, rect in {
            self.header_color : pygame.Rect(
                self.rect.x,
                self.rect.y-self.HEADER*self.wn_size[1],
                self.rect.w,
                self.HEADER*self.wn_size[1]
            ), # Header
            self.bg_color : self.rect # Content
        }.items():
            surface = pygame.Surface(rect.size)  # Header bg draw
            surface.set_alpha(color[3])
            surface.fill(color[:3])
            wn.blit(surface, rect.topleft) 

        ## Header draw
        text = self.font.render(self.name, False, self.text_color) # Label
        text_size = text.get_size()
        wn.blit(text, pygame.Rect(
                self.rect.x+self.rect.w*self.MARGIN,
                self.rect.y-self.HEADER*self.wn_size[1],
                text_size[0],
                text_size[1]
            )
        )

        for i in range(1, 3+1): # Icons
            rect = pygame.Rect(
                self.rect.x+self.rect.width-self.rect.width*self.MARGIN*i-(self.HEADER*self.wn_size[1]-self.MARGIN*self.HEADER*self.wn_size[1])*i, 
                self.rect.y-self.HEADER*self.wn_size[1],
                self.HEADER*self.wn_size[1]-self.MARGIN*self.HEADER*self.wn_size[1],
                self.HEADER*self.wn_size[1]-self.MARGIN*self.HEADER*self.wn_size[1]
            )

            if self.option_on_hover(mouse_pos[0], mouse_pos[1], i):
                color = self.ICON_X if i == 1 else self.ICON_O
                rect2 = pygame.Rect(
                    rect.x-self.MARGIN*self.rect.w//2,
                    rect.y,
                    rect.w+self.MARGIN*self.rect.w,
                    rect.h
                )
                surface = pygame.Surface(rect2.size)  # Bg draw
                surface.set_alpha(color[3])
                surface.fill(color[:3])
                wn.blit(surface, rect2.topleft) 

            wn.blit(pygame.transform.smoothscale(
                    self.icons[["quit", "reajust", "reduce"][i-1]], 
                    rect.size
                ),
                (rect.x, rect.y)
            )