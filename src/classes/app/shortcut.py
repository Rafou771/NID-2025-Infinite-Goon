import pygame
from classes.App import App

class Shortcut_app(App):
    TITLE_SIZE = 0.075
    TITLE_TOP = 0.1
    MARGIN_ = (0.2, 0.001)
    PADDING = 0.1
    TEXT_SIZE = 0.055
    def __init__(
            self, 
            icons : dict[str, pygame.Surface], 
            wn_size : tuple[int, int], 
            data : dict[str, str]
        ):
        super().__init__(
            "Raccourcis", # Name
            wn_size, # Screen resolution
            (0, 0, 0, 200), # Bg color
            (0, 0, 0, 250), # Header color
            icons,
            "./assets/xp.otf", # Text font
            (255, 255, 255) # Text color
        )
        self.data = data

    def draw(self, wn : pygame.Surface, mouse_pos : tuple[int, int]):
        super().draw(wn, mouse_pos)

        if not self.toggle:
            return

        font = pygame.font.Font(self.text_font, int(self.rect.w*self.TITLE_SIZE))
        text = font.render("Racourcis", False, self.text_color)
        rect = pygame.Rect(
            self.rect.x+self.rect.width//2-text.get_size()[0]//2,
            self.rect.y+self.TITLE_TOP*self.rect.h,
            text.get_size()[0],
            text.get_size()[1]
        )
        wn.blit(text, rect)

        font = pygame.font.Font(self.text_font, int(self.rect.h*self.TEXT_SIZE))
        text_color = [255-self.text_color[i] for i in range(3)]
        for i in range(len(self.data)):
            text = font.render(list(self.data.keys())[i], False, text_color) # Key text
            rect = pygame.Rect(
                self.rect.x+self.rect.width*self.MARGIN_[0],
                self.rect.y+self.rect.h//2-(len(self.data)*(text.get_size()[1]+self.rect.height*self.MARGIN_[1]))//2+i*text.get_size()[1]+i*self.rect.height*self.MARGIN_[1],
                text.get_size()[0],
                text.get_size()[1]
            )
            pygame.draw.rect(wn, text_color, pygame.Rect( # Key bg display
                    rect.x-((int(text.get_size()[0]*self.PADDING))//2),
                    rect.y-((text.get_size()[1]*self.PADDING)//2),
                    rect.w+int(text.get_size()[0]*self.PADDING),
                    rect.h+text.get_size()[1]*self.PADDING
                )
            )

            wn.blit(font.render(list(self.data.keys())[i], False, self.text_color), rect) # Key display

            text = font.render(": " + list(self.data.values())[i], False, self.text_color) # Description display
            wn.blit(text, pygame.Rect(
                    rect.x+self.PADDING*self.rect.w,
                    rect.y,
                    text.get_size()[0],
                    text.get_size()[1]
                )
            )