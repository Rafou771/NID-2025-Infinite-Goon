import pygame
from classes.App import App

class Shortcut_app(App):
    def __init__(self, icons : dict[str : pygame.Surface], wn_size : tuple[2], data : dict[str : str]):
        super().__init__(
            "Raccourcis", # Name
            wn_size, # Screen resolution
            (0, 0, 0, 200), # Bg color
            (0, 0, 0, 250), # Header color
            icons, # Icones
            "./assets/xp.otf", # Text font
            (255, 255, 255) # Text color
        )
        self.data = data

    def update(self, event : pygame.event.Event):
        super().update(event)

    def draw(self, wn : pygame.Surface):
        super().draw(wn)

        if not self.toggle:
            return

        font = pygame.font.Font(self.text_font, int(self.rect.w*0.075))
        text = font.render("Racourcis", False, (255, 255, 255))
        rect = pygame.Rect(
            self.rect.x+self.rect.width//2-text.get_size()[0]//2,
            self.rect.y+0.1*self.rect.h,
            text.get_size()[0],
            text.get_size()[1]
        )
        wn.blit(text, rect)

        font = pygame.font.Font(self.text_font, int(self.rect.h*0.055))
        for i in range(len(self.data)):
            text = font.render(list(self.data.keys())[i], False, (0, 0, 0))
            rect = pygame.Rect(
                self.rect.x+self.rect.width*0.2,
                self.rect.y+self.rect.h//2-(len(self.data)*(text.get_size()[1]+self.rect.height*0.001))//2+i*text.get_size()[1]+i*self.rect.height*0.001,
                text.get_size()[0],
                text.get_size()[1]
            )
            pygame.draw.rect(wn, (0, 0, 0), pygame.Rect(
                    rect.x-((int(text.get_size()[0]*0.1))//2),
                    rect.y-((text.get_size()[1]*0.1)//2),
                    rect.w+int(text.get_size()[0]*0.1),
                    rect.h+text.get_size()[1]*0.1
                )
            )

            text = font.render(list(self.data.keys())[i], False, (255, 255, 255))
            wn.blit(text, rect)

            text = font.render(": " + list(self.data.values())[i], False, (255, 255, 255))
            wn.blit(text, pygame.Rect(
                    rect.x+0.1*self.rect.w,
                    rect.y,
                    text.get_size()[0],
                    text.get_size()[1]
                )
            )


