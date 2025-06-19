# Ismael Chavez and Josh Nguyen
# June 18 2025
# Carnival Game Jam

#This imports some of the basic stuff needed for a pygame game.
import pygame as pg
import sys
from pygame.locals import *
import random
import time

#Basic Set Up
pg.init()
DISPLAYSURF = pg.display.set_mode((1000, 600))
font = pg.font.FontType("AtariClassic-gry3.ttf")

images = {
    "background": "Wild West.jpg",
    "target": "imagepath.png",
    "explosion": "imagepath.png",
    "characters": "imagepath.png"

}

sounds = {
    "shoot": "soundpath.mp3",
    "music": "soundpath.mp3",
    "explosion": "soundpath.mp3",
    "win_sound": "soundpath.mp3",
    "lose_sound": "soundpath.mp3"
}

#Setup
#Global Constants

class f():
    """
    Just important functions, especially GUI or IO functions
    The class name is very short (stands for "functions")
    so that calling its methods isn't a hassle
    """
    
    @staticmethod
    def ievents(list=0):
            """
            This is an... unconventional method, to say the least.
            But it is easier to remember than pg.get_getmorestuff.whatever.mouthful


            Params/Returns:
                    - 0: Returns a list of all Pygame events (this is the default).
                    - 1: Returns the state of all keyboard keys.
                    - 2: Returns the mouse's x position. 
                    - 3: Returns the mouse's y position.
                    - 4: Returns both mouse coords.
            """

            all_events = pg.event.get()
            keys_pressed = pg.key.get_pressed()
            mouse_x, mouse_y = pg.mouse.get_pos()
            if list == 0:
                return all_events
            if list == 1:
                return keys_pressed
            if list == 2:
                return mouse_x
            if list == 3:
                return mouse_y
            if list == 4:
                return pg.mouse.get_pos()
    #This draws the text and codes for it
    @staticmethod
    def draw_text(text, color, x, y, size):
        rendered_text = font.render(text, True, color)
        rendered_text = pg.transform.scale(rendered_text, (rendered_text.get_width() * size // 10, rendered_text.get_height() * size // 10))
        DISPLAYSURF.blit(rendered_text, (x, y))

    @staticmethod
    def draw_textbox(text, color, x, y, background_color, frame):
        # Draw a rectangle as the textbox background
        rendered_text = font.render(text, True, color)
        text_rect = rendered_text.get_rect(topleft=(x, y))
        padding = 10
        box_rect = pg.Rect(
            text_rect.left - padding,
            text_rect.top - padding,
            text_rect.width + 2 * padding,
            text_rect.height + 2 * padding
        )
        pg.draw.rect(DISPLAYSURF, background_color, box_rect)
        # Typewriter effect: show text up to current frame
        num_letters = min(len(text), frame)
        partial_text = text[:num_letters]
        rendered_partial = font.render(partial_text, True, color)
        DISPLAYSURF.blit(rendered_partial, (x, y))

    
        
        
        

        
class Menu:
    # All methods in the Game class will be static as game represents the global game state, not an object
    game_state = 0

    '''
    Game States:
    0: Menu
    1: Game
    2: Game over
    '''


    @staticmethod
    def menu():
        # This draws a red rectangle at (100,100) with width 200 and height 100
        while True:
            mouse_x, mouse_y = f.ievents(4) #these are the variables
            buttons = []
            buttons.append(pg.Rect(100, 100, 200, 100))
            for i in range (len(buttons)):
                pg.draw.rect(DISPLAYSURF, pg.Color("cyan"), buttons[i])
            f.draw_text("Start Game", pg.Color("black"), 110, 110, 10)
            DISPLAYSURF.fill(pg.Color("black"))
        
        
            #img = pg.image.load(images["background"])
            #DISPLAYSURF.blit(img, (0,0))
            for e in f.ievents():
                if e.type == QUIT:
                    pg.quit()
                    sys.exit()
            pg.display.update()
        

            for event in f.ievents():
                pass #for now

           
                    
        
                    



#Main game loop starts right here.
Menu.menu()

while True:
    DISPLAYSURF.fill(pg.Color("black"))
    
    
    #img = pg.image.load(images["background"])
    #DISPLAYSURF.blit(img, (0,0))
    for e in f.ievents():
        if e.type == QUIT:
            pg.quit()
            sys.exit()
    pg.display.update()