import pygame
from platform import window

from asyncio import run, sleep
from os import listdir

from classes import OptionList, Icon
from classes.app import Option_app, Credit_app, Shortcut_app

### CUSTOM GLOBAL VAR
MAX_FPS = 60

### IMAGE LOADING
app_icons = {} 

for text in listdir("./assets/icon"):
    text = text.replace(".png", "")
    img = pygame.PixelArray(pygame.image.load("./assets/icon/" + text + ".png").convert_alpha())
    img.replace((0, 0, 0), (255, 255, 255))

    app_icons.update({text: img.surface})

bg_imgs = {
    "./assets/bg/" + text: pygame.image.load("./assets/bg/" + text).convert()
    for text in listdir("./assets/bg")
}

bg_img_tmp = window.localStorage.getItem("bg_img")
worked = False
if bg_img_tmp:
    try:
        bg_img = bg_imgs[bg_img_tmp]
        worked = True
    except:
        pass

if not worked:
    default_bg = "./assets/bg/linux1.jpg"
    bg_img = bg_imgs[default_bg]
    window.localStorage.setItem("bg_img", default_bg)

async def main():
    ### INIT
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption('InfiniteDistro')
    
    wn = pygame.display.set_mode((0, 0))
    wn_size = wn.get_size()

    ### COMPONENTS
    apps = {
        "option": Option_app(
            app_icons, # Header icons
            wn_size, # Resolution
            bg_imgs # Bg images
        ),
        "credit": Credit_app(
            app_icons, # Header icons
            wn_size # Resolution
        ),
        "shortcut" : Shortcut_app(
            app_icons, # Header icons
            wn_size, # Resolution
            {
                "F11" : "Plein écran",
                "echap" : "Réduire une fenêtre",
                "o": "Ouvrir les options",
                "r" : "Ouvrir les raccourcis",
                "c" : "Ouvrir les crédits",
            }
        )
    }

    ol = OptionList(
        [ # Options
            {"label": "options", "icon": app_icons["option"], "function": lambda : apps["option"].open(apps)}, 
            {"label": "raccourcis", "icon": app_icons["clock"], "function": lambda : apps["shortcut"].open(apps)},
            {"label": "crédits", "icon": app_icons["info"], "function": lambda : apps["credit"].open(apps)}
        ],
        (12, 11, 56), # Option color
        (42, 41, 114), # On hover color
        "./assets/xp.otf", # Text font
        (255, 255, 255), # Text color
        wn_size # Window size
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
            wn_size,
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
            wn_size,
            1
        )
    ]

    ### MAIN
    running = True
    while running:
        ### EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # System
                running = False
            if event.type == pygame.VIDEORESIZE:
                wn_size = event.size

            if event.type == pygame.MOUSEBUTTONDOWN: # Apps and icons
                ol.update(event)
                bg_img = apps["option"].update(event)
                bg_img = apps["credit"].update(event, bg_imgs, apps)
                apps["shortcut"].update(event)
                for icon in icons:
                    icon.update(event)

            if event.type == pygame.KEYDOWN: # Sortcuts
                if event.key == pygame.K_o:
                    apps["option"].open(apps)
                if event.key == pygame.K_r:
                    apps["shortcut"].open(apps)
                if event.key == pygame.K_c:
                    apps["credit"].open(apps)
                if event.key == pygame.K_ESCAPE:
                    for app in apps.values():
                        if app.toggle:
                            app.suspend()
                if event.key == pygame.K_F11:
                    if not window.document.fullscreenElement:
                        canvas = window.document.getElementById("canvas")
                        canvas.requestFullscreen()
                    else:
                        window.document.exitFullscreen()

        ### DRAWING
        wn.blit(pygame.transform.smoothscale(bg_img, wn_size), (0, 0)) # Bg img
        for el in icons + [ol] + list(apps.values()): # Components
            el.draw(wn, pygame.mouse.get_pos())

        ### SCREEN UPDATE
        pygame.display.flip()
        await sleep(0)

run(main())