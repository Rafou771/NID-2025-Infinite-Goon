import pygame
from classes.App import App
from platform import window

class Credit_app(App):
    FAVICON_SIZE = 0.10
    FAVICON_BOT = 0.1
    TITLE_SIZE = 0.075
    DESC_SIZE = 0.055
    DESC_MARGIN = 0.001
    TITLE_TOP = 0.1
    def __init__(
        self, 
        icons : dict[str, pygame.Surface], 
        wn_size : tuple[int, int]
    ):
        super().__init__(
            "Crédits", # Name
            wn_size, # Screen resolution
            (0, 0, 0, 200), # Bg color
            (0, 0, 0, 250), # Header color
            icons,
            "./assets/xp.otf", # Text font
            (255, 255, 255) # Text color
        )

        self.icon = pygame.transform.smoothscale(self.icons["favicon"], (self.rect.w*self.FAVICON_SIZE,)*2)
        self.icon_rect = pygame.Rect(
            self.rect.x+self.rect.width//2-self.icon.get_width()//2,
            self.rect.y+self.rect.h-int(self.rect.h*self.FAVICON_BOT)-self.icon.get_height(),
            self.icon.get_width(),
            self.icon.get_height()
        )

    def update(self, event : pygame.event.Event, bg_imgs : list[pygame.Surface], apps : dict[str, App]):
        super().update(event)

        if not event.type == pygame.MOUSEBUTTONDOWN:
            return

        self.icon = pygame.transform.smoothscale(self.icons["favicon"], (self.rect.w*self.FAVICON_SIZE,)*2)
        self.icon_rect = pygame.Rect(
            self.rect.x+self.rect.width//2-self.icon.get_width()//2,
            self.rect.y+self.rect.h-int(self.rect.h*self.FAVICON_BOT)-self.icon.get_height(),
            self.icon.get_width(),
            self.icon.get_height()
        )

        x, y = event.pos
        if x >= self.icon_rect.x and x <= self.icon_rect.x + self.icon_rect.w and y >= self.icon_rect.y and y <= self.icon_rect.y + self.icon_rect.h:
            window.localStorage.setItem("bg_img", "./assets/bg/linux3.jpg")
            apps["option"].selected = "./assets/bg/linux3.jpg"
            return bg_imgs["./assets/bg/linux3.jpg"]
        return bg_imgs[window.localStorage.getItem("bg_img")]

    def draw(self, wn : pygame.Surface, mouse_pos : tuple[int, int]):
        super().draw(wn, mouse_pos)

        if not self.toggle:
            return

        font = pygame.font.Font(self.text_font, int(self.rect.w*self.TITLE_SIZE)) # Title
        text = font.render("INFINITE GOON", False, self.text_color)
        rect = pygame.Rect(
            self.rect.x+self.rect.width//2-text.get_size()[0]//2,
            self.rect.y+self.TITLE_TOP*self.rect.h,
            text.get_size()[0],
            text.get_size()[1]
        )
        wn.blit(text, rect)

        names = [
            "Naffrechoux Hélior",
            "Rosier Yann",
            "Rosier Mathieu",
            "Chevallier Gabriel",
            "Dumont Clément",
            "Agadi Adam",
            "Fuseau-Eugène Théophane",
            "Girard-Viénot Rafaël",
            "Lemeunier Benoit",
            "Billot Tony"
        ]
        font = pygame.font.Font(self.text_font, int(self.rect.h*self.DESC_SIZE))
        for i in range(len(names)):
            text = font.render(names[i], False, self.text_color)
            wn.blit(text, pygame.Rect(
                    self.rect.x+self.rect.width//2-text.get_size()[0]//2,
                    self.rect.y+self.rect.h//2-(len(names)*(text.get_size()[1]+self.rect.height*self.DESC_MARGIN))//2+i*text.get_size()[1]+i*self.rect.height*self.DESC_MARGIN,
                    text.get_size()[0],
                    text.get_size()[1]
                )
            )
        wn.blit(self.icon, self.icon_rect)