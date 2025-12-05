import pygame
from classes.App import App
from platform import window

class Option_app(App):
    def __init__(
            self, 
            icons : dict[str : pygame.Surface], 
            wn_size : tuple[2], 
            bg_imgs : list[pygame.Surface]
        ):
        super().__init__(
            "Options", # Name
            wn_size, # Screen resolution
            (0, 0, 0, 200), # Bg color
            (0, 0, 0, 250), # Header color
            icons,
            "./assets/xp.otf", # Text font
            (255, 255, 255) # Text color
        )
        self.bg_imgs = bg_imgs

        self.button_rect1 = pygame.Rect(
            self.rect.x+self.rect.w-int(0.18*self.rect.w)-int(self.HEADER*self.rect.w),
            self.rect.y+self.rect.h-self.HEADER*self.rect.h-int(self.rect.h*0.06),
            int(self.rect.w*0.18),
            int(self.rect.h*0.06)
        )
        self.button_rect2 = pygame.Rect(
            self.button_rect1.x-self.button_rect1.w-int(self.MARGIN*self.rect.w),
            self.button_rect1.y,
            self.button_rect1.w,
            self.button_rect1.h
        )
        margin = 0.035*self.rect.w
        self.bg_rect = pygame.Rect(
            self.rect.x+self.rect.w//2-margin-0.35*self.rect.w,
            self.rect.y+self.rect.h//2-(0.25*self.rect.h)//2,
            0.35*self.rect.w,
            0.25*self.rect.h
        )
        self.bg_rect2 = pygame.Rect(
            self.rect.x+self.rect.w//2+margin,
            self.bg_rect.y,
            self.bg_rect.w,
            self.bg_rect.h
        )
        self.selected = window.localStorage.getItem("bg_img")
        self.last_selected = self.selected
        self.on_hover = lambda x, y, rect : x >= rect.x and x <= rect.x + rect.w and y >= rect.y and y <= rect.y+rect.h

    def update(self, event : pygame.event.Event):
        if not event.type == pygame.MOUSEBUTTONDOWN:
            return self.bg_imgs[self.selected]
        super().update(event)

        if event.button == 1:
            x, y = pygame.mouse.get_pos()
            if self.on_hover(x, y, self.button_rect1):
                self.last_selected = self.selected
                window.localStorage.setItem("bg_img", self.selected)
                self.close()
            elif self.on_hover(x, y, self.button_rect2):
                self.last_selected = self.selected
                window.localStorage.setItem("bg_img", self.selected)
            elif self.on_hover(x, y, self.bg_rect):
                self.last_selected = self.selected
                self.selected = "./img/bg/linux1.jpg"
            elif self.on_hover(x, y, self.bg_rect2):
                self.last_selected = self.selected
                self.selected = "./img/bg/linux2.jpg"

        return self.bg_imgs[window.localStorage.getItem("bg_img")]

    def draw(self, wn : pygame.Surface):
        super().draw(wn)

        if not self.toggle:
            return

        self.button_rect1 = pygame.Rect(
            self.rect.x+self.rect.w-int(0.18*self.rect.w)-int(self.HEADER*self.rect.w),
            self.rect.y+self.rect.h-self.HEADER*self.rect.h-int(self.rect.h*0.06),
            int(self.rect.w*0.18),
            int(self.rect.h*0.06)
        )
        self.button_rect2 = pygame.Rect(
            self.button_rect1.x-self.button_rect1.w-int(self.MARGIN*self.rect.w),
            self.button_rect1.y,
            self.button_rect1.w,
            self.button_rect1.h
        )
        margin = 0.025*self.rect.w
        self.bg_rect = pygame.Rect(
            self.rect.x+self.rect.w//2-margin-0.35*self.rect.w,
            self.rect.y+self.rect.h//2-(0.25*self.rect.h)//2,
            0.35*self.rect.w,
            0.25*self.rect.h
        )
        self.bg_rect2 = pygame.Rect(
            self.rect.x+self.rect.w//2+margin,
            self.bg_rect.y,
            self.bg_rect.w,
            self.bg_rect.h
        )
        text = pygame.font.Font("./assets/xp.otf", int(0.07*self.rect.w)).render("Fond d'écran", False, self.text_color) # Label draw
        wn.blit(text, pygame.Rect(
                self.rect.x+self.rect.width//2-text.get_size()[0]//2,
                self.rect.y+int(0.1*self.rect.h),
                text.get_size()[0],
                text.get_size()[1]
            )
        )

        x, y = pygame.mouse.get_pos()
        if self.on_hover(x, y, self.button_rect1):
            color = (190, 190, 190)
        elif self.selected != self.last_selected:
            color = (255, 255, 255)
        else:
            color = (54, 54, 54)
        pygame.draw.rect(wn, color, self.button_rect1)
        if self.on_hover(x, y, self.button_rect2):
            color = (190, 190, 190)
        elif self.selected != self.last_selected:
            color = (255, 255, 255)
        else:
            color = (54, 54, 54)
        pygame.draw.rect(wn, color, self.button_rect2)

        font = pygame.font.Font("./assets/xp.otf", int(self.button_rect1.h*0.95))
        text = font.render("Appliquer", False, (0, 0, 0))
        wn.blit(text, pygame.Rect(
                self.button_rect1.x-text.get_size()[0]//2+self.button_rect1.w//2,
                self.button_rect1.y,
                self.button_rect1.w,
                self.button_rect1.h
            )
        )

        text = font.render("Sauvegarder", False, (0, 0, 0))
        wn.blit(text, pygame.Rect(
                self.button_rect2.x-text.get_size()[0]//2+self.button_rect2.w//2,
                self.button_rect2.y,
                self.button_rect2.w,
                self.button_rect2.h
            )
        )

        rect = pygame.Rect(
            self.rect.x+self.rect.w//2-margin-0.35*self.rect.w,
            self.rect.y+self.rect.h//2-(0.25*self.rect.h)//2,
            0.35*self.rect.w,
            0.25*self.rect.h
        )
        if self.selected == "./img/bg/linux1.jpg":
            pygame.draw.rect(wn, (255, 255, 255), pygame.Rect(
                    self.bg_rect.x-margin//2,
                    self.bg_rect.y-margin//2,
                    self.bg_rect.w+margin,
                    self.bg_rect.h+margin
                )
            )
        wn.blit(pygame.transform.smoothscale(self.bg_imgs["./img/bg/linux1.jpg"], self.bg_rect.size),  self.bg_rect)

        if self.selected == "./img/bg/linux2.jpg":
            pygame.draw.rect(wn, (255, 255, 255), pygame.Rect(
                    self.bg_rect2.x-margin//2,
                    self.bg_rect2.y-margin//2,
                    self.bg_rect2.w+margin,
                    self.bg_rect2.h+margin
                )
            )
        wn.blit(pygame.transform.smoothscale(self.bg_imgs["./img/bg/linux2.jpg"], self.bg_rect2.size), self.bg_rect2)