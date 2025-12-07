import pygame
from typing import Callable, List, Dict, Literal, Union

class OptionList():
    HEADER = 0.1
    LABEL = 0.6
    MARGIN = 0.075
    ICON = 0.6
    SIZE = (0.1, 0.032)
    def __init__(
        self,
        components : List[Dict[Literal["icon", "label", "function"], Union[pygame.Surface, str, Callable]]],
        bg_color : tuple[int, int, int],
        active_color : tuple[int, int, int], 
        text_font : str,
        text_color : tuple[int, int, int],
        wn_size : tuple[int, int]
    ) -> None: 
        self.components = components
        self.option_size = (int(self.SIZE[0]*wn_size[0]), int(self.SIZE[1]*wn_size[1]))
        self.color = bg_color
        self.active_color = active_color
        self.text_color = text_color
        self.wn_size = wn_size

        self.rect = pygame.Rect(
            0,
            0,
            self.option_size[0],
            self.HEADER*self.option_size[1]
        )

        self.font = pygame.font.Font(text_font, int(self.LABEL*self.option_size[1]))
        self.toggle = False

        self.on_hover = lambda p, i: p[0] > self.rect.x and p[0] < self.option_size[0]+self.rect.x and p[1] > self.rect.y+self.option_size[1]*i and p[1] < self.rect.y+self.option_size[1]*(i+1)
        self.get_function = lambda y: self.components[
            int((y-self.rect.y)//self.option_size[1])
        ]["function"]

    def draw(self, wn : pygame.Surface, mouse_pos : tuple[int, int]) -> None:
        if not self.toggle:
            return

        pygame.draw.rect(wn, self.color, self.rect) ## Header draw

        for i in range(len(self.components)): ## Options
            option = self.components[i] # Option

            pygame.draw.rect( # Bg draw
                wn,
                self.active_color if self.on_hover(mouse_pos, i) else self.color,
                pygame.Rect(
                    self.rect.x,
                    self.rect.y+self.rect.h+self.option_size[1]*i,
                    self.option_size[0],
                    self.option_size[1]
                )
            )

            if option["icon"] != None: # Icon draw
                img = pygame.transform.smoothscale(
                    option["icon"], 
                    (self.ICON*self.option_size[1], self.ICON*self.option_size[1])
                )
                wn.blit(
                    img,
                    (
                        self.rect.x+self.MARGIN*self.option_size[0],
                        self.rect.y+self.option_size[1]*i+self.rect.h+((1-self.ICON)*self.option_size[1])/2
                    )
                )

            text = self.font.render(option["label"], False, self.text_color) # Text draw
            wn.blit(
                text, 
                (
                    self.rect.x+self.MARGIN*self.option_size[0] + (
                        self.MARGIN*self.option_size[0]+self.ICON*self.option_size[1]
                    ), 
                    self.rect.y+self.option_size[1]*i+self.rect.h+self.option_size[1]//2-text.get_height()//2
                )
            )

        pygame.draw.rect(wn, self.color, pygame.Rect( # Footer draw
                self.rect.x,
                self.rect.y+len(self.components)*self.option_size[1],
                self.rect.w,
                self.rect.h
            )
        )

    def update(self, event : pygame.event.Event) -> None:
        if not event.type == pygame.MOUSEBUTTONDOWN:
            return

        if event.button == 3: 
        # On right click anywhere
            if not self.toggle:
                self.toggle = not self.toggle
            self.rect.x = event.pos[0]
            self.rect.y = event.pos[1]

            if self.wn_size[0] < self.rect.x+self.rect.w:
                self.rect.x -= self.rect.w
            if self.wn_size[1] < self.rect.y+len(self.components)*self.option_size[1]:
                self.rect.y -= len(self.components)*self.option_size[1]

        elif not sum([self.on_hover(event.pos, i) for i in range(len(self.components))]) and self.toggle:
        # On left click outside GUI
            self.toggle = not self.toggle

        elif self.toggle: 
        # On left click in GUI
            self.get_function(event.pos[1])()
            self.toggle = not self.toggle