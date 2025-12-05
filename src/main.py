import pygame
import asyncio
import os
from utils import get_config
from classes import OptionList, Icon
from classes.app import Option_app, Credit_app, Shortcut_app
from platform import window

### CUSTOM GLOBAL VAR
MAX_FPS = 60

### IMAGE LOADING
app_icons = {} 

for text in os.listdir("./img/icon"):
    text = text.replace(".png", "")
    img = pygame.PixelArray(pygame.image.load("./img/icon/" + text + ".png").convert_alpha())
    img.replace((0, 0, 0), (255, 255, 255))
    app_icons.update({text: img.surface})
app_icons.update({"favicon" : pygame.image.load("./img/favicon.png").convert_alpha()})

bg_imgs = {
    "./img/bg/" + text: pygame.image.load("./img/bg/" + text).convert()
    for text in os.listdir("./img/bg")
}

bg_img_tmp = window.localStorage.getItem("bg_img")
if bg_img_tmp:
    bg_img = bg_imgs[bg_img_tmp]
else:
    path = get_config("default_bg_path")
    bg_img = bg_imgs[path]
    window.localStorage.setItem("bg_img", path)

async def main():
    ### INIT
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption('InfiniteDistro')

    clock = pygame.time.Clock()
    wn = pygame.display.set_mode((0, 0))

    wn_width, wn_height = pygame.display.get_window_size()

    ### COMPONENTS
    apps = {
        "option": Option_app(
            app_icons, # Header icons
            (wn_width, wn_height), # Resolution
            bg_imgs # Bg images
        ),
        "credit": Credit_app(
            app_icons, # Header icons
            (wn_width, wn_height) # Resolution
        ),
        "shortcut" : Shortcut_app(
            app_icons, # Header icons
            (wn_width, wn_height), # Resolution
            {
                "F11" : "Plein écran",
                "echap" : "Réduire une fenêtre",
                "o": "options",
                "r" : "raccourcis",
                "c" : "crédits",
            }
        )
    }

    ol = OptionList(
        (wn_width*0.1, wn_height*0.032), # Option size
        [ # Options
            {"label": "options", "icon": app_icons["option"], "function": lambda : apps["option"].open(apps)}, 
            {"label": "raccourcis", "icon": app_icons["clock"], "function": lambda :  apps["shortcut"].open(apps)},
            {"label": "crédits", "icon": app_icons["info"], "function": lambda :  apps["credit"].open(apps)}
        ],
        (12, 11, 56), # Option color
        (42, 41, 114), # On hover color
        "./assets/xp.otf", # Text font
        (255, 255, 255), # Text color
        (wn_width, wn_height)
    )

    icons = [
        Icon(
            "Snake",
            "./assets/xp.otf",
            app_icons["snake"], 
            (255, 255, 255, 20),
            (147, 186, 237, 40),
            (255, 255, 255),
            "http://snake-nuit-info.web.app/",
            (wn_width, wn_height),
            0
        ),
        Icon(
            "ChatBot",
            "./assets/xp.otf",
            app_icons["chatbot"], 
            (255, 255, 255, 20),
            (147, 186, 237, 40),
            (255, 255, 255),
            "http://infinitegoon.alwaysdata.net/chatbotai/",
            (wn_width, wn_height),
            1
        )
    ]

    ### MAIN
    running = True
    dt = 0
    full_screen = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                wn_width = event.w 
                wn_height = event.h
            if event.type == pygame.MOUSEBUTTONDOWN:
                ol.update(event)
                bg_img = apps["option"].update(event)
                bg_img = apps["credit"].update(event, bg_imgs, apps)
                apps["shortcut"].update(event)
                for icon in icons:
                    icon.update(event)

        wn.blit(pygame.transform.smoothscale(bg_img, (wn_width, wn_height)), (0, 0))
        for icon in icons:
            icon.draw(wn)
        ol.draw(wn)
        for app in apps.values():
            app.draw(wn)

        ### SHORTCUTS
        keys = pygame.key.get_pressed()
        if keys[pygame.K_o]:
            apps["option"].open(apps)
        if keys[pygame.K_r]:
            apps["shortcut"].open(apps)
        if keys[pygame.K_c]:
            apps["credit"].open(apps)
        if keys[pygame.K_ESCAPE]:
            for app in apps.values():
                if app.toggle:
                    app.suspend()
        if keys[pygame.K_F11]:
            if full_screen:
                wn = pygame.display.set_mode((0, 0))
            else:
                wn = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.flip()
        dt = clock.tick(MAX_FPS) / 1000

        await asyncio.sleep(0)

asyncio.run(main())
