import pygame
from classes.App import App
from platform import window

class Credit_app(App):
    def __init__(self, icons : dict[str : pygame.Surface], wn_size : tuple[2]):
        super().__init__(
            "Crédits", # Name
            wn_size, # Screen resolution
            (0, 0, 0, 200), # Bg color
            (0, 0, 0, 250), # Header color
            icons,
            "./assets/xp.otf", # Text font
            (255, 255, 255) # Text color
        )

        self.icon = pygame.transform.smoothscale(self.icons["favicon"], (int(self.rect.w*0.10),)*2)
        self.icon_rect = pygame.Rect(
            self.rect.x+self.rect.width//2-self.icon.get_width()//2,
            self.rect.y+self.rect.h-int(self.rect.h*0.1)-self.icon.get_height(),
            self.icon.get_width(),
            self.icon.get_height()
        )

    def update(self, event : pygame.event.Event, bg_imgs : list[pygame.Surface], apps : dict[str : App]):
        super().update(event)

        x, y = pygame.mouse.get_pos()
        if x >= self.icon_rect.x and x <= self.icon_rect.x + self.icon_rect.w and y >= self.icon_rect.y and y <= self.icon_rect.y + self.icon_rect.h:
            window.localStorage.setItem("bg_img", "./img/bg/linux3.jpg")
            apps["option"].selected = "./img/bg/linux3.jpg"
            return bg_imgs["./img/bg/linux3.jpg"]
        return bg_imgs[window.localStorage.getItem("bg_img")]

    def draw(self, wn : pygame.Surface):
        super().draw(wn)

        if not self.toggle:
            return

        font = pygame.font.Font(self.text_font, int(self.rect.w*0.075))
        text = font.render("INFINITE GOON", False, (255, 255, 255))
        rect = pygame.Rect(
            self.rect.x+self.rect.width//2-text.get_size()[0]//2,
            self.rect.y+0.1*self.rect.h,
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
        font = pygame.font.Font(self.text_font, int(self.rect.h*0.055))
        for i in range(len(names)):
            text = font.render(names[i], False, (255, 255, 255))
            wn.blit(text, pygame.Rect(
                    self.rect.x+self.rect.width//2-text.get_size()[0]//2,
                    self.rect.y+self.rect.h//2-(len(names)*(text.get_size()[1]+self.rect.height*0.001))//2+i*text.get_size()[1]+i*self.rect.height*0.001,
                    text.get_size()[0],
                    text.get_size()[1]
                )
            )
        wn.blit(self.icon, self.icon_rect)