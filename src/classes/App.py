import pygame

class App():
    SIZE = (0.45, 0.60)
    HEADER = 0.03
    MARGIN = 0.02
    LABEL = 0.8
    def __init__(
        self,
        name : str,
        wn_size : tuple[2], 
        bg_color : tuple[4],
        header_color : tuple[4],
        icons : dict[("quit", "reajust", "reduce") : pygame.Surface],
        font : str,
        text_color : tuple[3]
    ):
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

    def open(self, apps):
        for app in apps.values():
            app.suspend()
        self.toggle = True

    def reset(self):
        self.rect = pygame.Rect(
            self.wn_size[0]//2-(self.SIZE[0]*self.wn_size[0])//2, 
            self.wn_size[1]//2-((self.SIZE[1]-self.HEADER)*self.wn_size[1])//2+self.HEADER*self.wn_size[1], 
            self.SIZE[0]*self.wn_size[0],
            (self.SIZE[1]-self.HEADER)*self.wn_size[1]
        )

    def close(self):
        self.toggle = False
        self.reset()

    def suspend(self):
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

    def update(self, event : pygame.event.Event):
        if not event.type == pygame.MOUSEBUTTONDOWN:
            return

        if event.button == 1:
            if self.option_on_hover(event.pos[0], event.pos[1], 3):
                self.suspend()
            elif self.option_on_hover(event.pos[0], event.pos[1], 2):
                self.expand()
            elif self.option_on_hover(event.pos[0], event.pos[1], 1):
                self.close()

    def draw(self, wn : pygame.Surface):
        if not self.toggle: # app icon
            return

        rect = pygame.Rect(
            self.rect.x,
            self.rect.y-self.HEADER*self.wn_size[1],
            self.rect.width,
            self.HEADER*self.wn_size[1]
        )

        surface = pygame.Surface(rect.size)  # Header bg draw
        surface.set_alpha(self.header_color[3])
        surface.fill(self.header_color[:3])
        wn.blit(surface, rect.topleft) 

        surface = pygame.Surface(self.rect.size)  # Bg draw
        surface.set_alpha(self.bg_color[3])
        surface.fill(self.bg_color[:3])
        wn.blit(surface, self.rect.topleft) 

        text = self.font.render(self.name, False, self.text_color) # Label draw
        text_size = text.get_size()
        wn.blit(text, pygame.Rect(
                self.rect.x+self.rect.width*self.MARGIN,
                self.rect.y-self.HEADER*self.wn_size[1],
                text_size[0],
                text_size[1]
            )
        )

        for i in range(1, 3+1): # Header icon draw
            rect = pygame.Rect(
                self.rect.x+self.rect.width-self.rect.width*self.MARGIN*i-(self.HEADER*self.wn_size[1]-self.MARGIN*self.HEADER*self.wn_size[1])*i, 
                self.rect.y-self.HEADER*self.wn_size[1],
                self.HEADER*self.wn_size[1]-self.MARGIN*self.HEADER*self.wn_size[1],
                self.HEADER*self.wn_size[1]-self.MARGIN*self.HEADER*self.wn_size[1]
            )
            x, y = pygame.mouse.get_pos()
            if self.option_on_hover(x, y, i):
                color = (255, 0, 0, 50) if i == 1 else (190, 190, 190, 50)

                surface = pygame.Surface(rect.size)  # Bg draw
                surface.set_alpha(color[3])
                surface.fill(color[:3])
                wn.blit(surface, rect.topleft) 

            wn.blit(pygame.transform.smoothscale(
                    self.icons[["quit", "reajust", "reduce"][i-1]], 
                    rect.size
                ),
                (rect.x, rect.y)
            )