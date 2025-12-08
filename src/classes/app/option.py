import pygame
from classes.App import App
from platform import window

class Option_app(App):
    BUTTON_SIZE = (0.18, 0.06)
    SELECT_COLOR = (255, 255, 255)
    BUTTON_ON_HOVER = (190, 190, 190)
    BUTTON_ON_CLICK = (255, 255, 255)
    BUTTON_COLOR = (54, 54, 54)
    BG_MARGIN = 0.035
    BG_SIZE = (1.75, 0.25) # W depends on H
    BORDER = 0.015
    BUTTON_TEXT = 0.95
    def __init__(
            self, 
            icons : dict[str, pygame.Surface], 
            wn_size : tuple[int, int], 
            bg_imgs : list[pygame.Surface]
        ) -> None:
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
            self.rect.x+self.rect.w-int(self.BUTTON_SIZE[0]*self.rect.w)-int(self.HEADER*self.rect.w),
            self.rect.y+self.rect.h-self.HEADER*self.rect.h-int(self.rect.h*self.BUTTON_SIZE[1]),
            int(self.rect.w*self.BUTTON_SIZE[0]),
            int(self.rect.h*self.BUTTON_SIZE[1])
        )
        self.button_rect2 = pygame.Rect(
            self.button_rect1.x-self.button_rect1.w-int(self.MARGIN*self.rect.w),
            self.button_rect1.y,
            self.button_rect1.w,
            self.button_rect1.h
        )

        self.bg_rect = pygame.Rect(
            self.rect.x+self.rect.w//2-self.BG_MARGIN*self.rect.w-(self.BG_SIZE[1]*self.rect.h)*self.BG_SIZE[0],
            self.rect.y+self.rect.h//2-self.BG_SIZE[1]*self.rect.h//2,
            (self.BG_SIZE[1]*self.rect.h)*self.BG_SIZE[0],
            self.BG_SIZE[1]*self.rect.h
        )
        self.bg_rect2 = pygame.Rect(
            self.rect.x+self.rect.w//2+self.BG_MARGIN*self.rect.w,
            self.bg_rect.y,
            self.bg_rect.w,
            self.bg_rect.h
        )
        self.selected = window.localStorage.getItem("bg_img")
        self.on_hover = lambda x, y, rect : x >= rect.x and x <= rect.x + rect.w and y >= rect.y and y <= rect.y+rect.h

    def update(self, event : pygame.event.Event) -> pygame.Surface:
        super().update(event)
        if not event.type == pygame.MOUSEBUTTONDOWN or not self.toggle:
            return self.bg_imgs[self.selected]

        if event.button == 1:
            x, y = event.pos
            if self.on_hover(x, y, self.button_rect1):
                window.localStorage.setItem("bg_img", self.selected)
            elif self.on_hover(x, y, self.button_rect2):
                window.localStorage.setItem("bg_img", self.selected)
                self.close()
            elif self.on_hover(x, y, self.bg_rect):
                self.selected = "./assets/bg/linux1.jpg"
            elif self.on_hover(x, y, self.bg_rect2):
                self.selected = "./assets/bg/linux2.jpg"

        return self.bg_imgs[self.selected]

    def reset(self) -> None:
        super().reset()

        self.selected = window.localStorage.getItem("bg_img")

    def draw(self, wn : pygame.Surface, mouse_pos : tuple[int, int]) -> None:
        super().draw(wn, mouse_pos)

        if not self.toggle:
            return

        ## Updates
        self.button_rect1 = pygame.Rect(
            self.rect.x+self.rect.w-int(self.BUTTON_SIZE[0]*self.rect.w)-int(self.HEADER*self.rect.w),
            self.rect.y+self.rect.h-self.HEADER*self.rect.h-int(self.rect.h*self.BUTTON_SIZE[1]),
            int(self.rect.w*self.BUTTON_SIZE[0]),
            int(self.rect.h*self.BUTTON_SIZE[1])
        )
        self.button_rect2 = pygame.Rect(
            self.button_rect1.x-self.button_rect1.w-int(self.MARGIN*self.rect.w),
            self.button_rect1.y,
            self.button_rect1.w,
            self.button_rect1.h
        )

        self.bg_rect = pygame.Rect(
            self.rect.x+self.rect.w//2-self.BG_MARGIN*self.rect.w-(self.BG_SIZE[1]*self.rect.h)*self.BG_SIZE[0],
            self.rect.y+self.rect.h//2-self.BG_SIZE[1]*self.rect.h//2,
            (self.BG_SIZE[1]*self.rect.h)*self.BG_SIZE[0],
            self.BG_SIZE[1]*self.rect.h
        )
        self.bg_rect2 = pygame.Rect(
            self.rect.x+self.rect.w//2+self.BG_MARGIN*self.rect.w,
            self.bg_rect.y,
            self.bg_rect.w,
            self.bg_rect.h
        )

        ## Label draw
        text = pygame.font.Font("./assets/xp.otf", int(0.07*self.rect.w)).render("Fond d'écran", False, self.text_color)
        wn.blit(text, pygame.Rect(
                self.rect.x+self.rect.width//2-text.get_size()[0]//2,
                self.rect.y+int(0.1*self.rect.h),
                text.get_size()[0],
                text.get_size()[1]
            )
        )

        ## Button draw
        for rect in [self.button_rect1, self.button_rect2]:
            if self.on_hover(mouse_pos[0], mouse_pos[1], rect):
                color = self.BUTTON_ON_HOVER
            elif self.selected != window.localStorage.getItem("bg_img") or rect == self.button_rect2:
                color = self.BUTTON_ON_CLICK
            else:
                color = self.BUTTON_COLOR
            pygame.draw.rect(wn, color, rect)

        text_color = [255-self.text_color[i] for i in range(len(self.text_color))]
        font = pygame.font.Font("./assets/xp.otf", int(self.button_rect1.h*self.BUTTON_TEXT))

        text = font.render("Appliquer", False, text_color)
        wn.blit(text, pygame.Rect(
                self.button_rect1.x-text.get_size()[0]//2+self.button_rect1.w//2,
                self.button_rect1.y,
                self.button_rect1.w,
                self.button_rect1.h
            )
        )

        text = font.render("Ok", False, text_color)
        wn.blit(text, pygame.Rect(
                self.button_rect2.x-text.get_size()[0]//2+self.button_rect2.w//2,
                self.button_rect2.y,
                self.button_rect2.w,
                self.button_rect2.h
            )
        )

        # Vignette draw
        for path, rect in {
            "./assets/bg/linux1.jpg" : self.bg_rect,
            "./assets/bg/linux2.jpg" : self.bg_rect2
        }.items():
            if self.selected == path:
                pygame.draw.rect(wn, self.SELECT_COLOR, pygame.Rect(
                        rect.x-self.BORDER*self.rect.w//2,
                        rect.y-self.BORDER*self.rect.w//2,
                        rect.w+self.BORDER*self.rect.w,
                        rect.h+self.BORDER*self.rect.w
                    )
                )
            wn.blit(pygame.transform.smoothscale(self.bg_imgs[path], rect.size), rect)