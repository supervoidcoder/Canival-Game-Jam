# Ismael Chavez and Josh Nguyen
# June 18 2025
# Carnival Game Jam

#This imports some of the basic stuff needed for a pygame game.
import pygame as pg
import sys
from pygame.locals import *
import random
import time
# Note: hardcoding things: nono (apparently)



#Basic Set Up

SCREEN_H = 600
SCREEN_W = 1000
pg.init()
DISPLAYSURF = pg.display.set_mode((SCREEN_W, SCREEN_H))
font = pg.font.FontType("AtariClassic-gry3.ttf")


images = {
    "background": "Wild West.png",
    "target": "Target.png",
    "explosion": "Explosion.png",
    "characters": "imagepath.png"

}
image = pg.image.load(images["background"])
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
    def ievents(list = 0):
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
            m_x, m_y = pg.mouse.get_pos()
            if list == 0:
                return all_events
            if list == 1:
                return keys_pressed
            if list == 2:
                return m_x
            if list == 3:
                return m_y
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
        num_letters = min((text), frame)
        partial_text = text[:num_letters]
        rendered_partial = font.render(partial_text, True, color)
        DISPLAYSURF.blit(rendered_partial, (x, y))

class Targets:
    def __init__(self, x, y, type):
        """
        Type:

            - 0: Static/Immobile Target. Doesn't move.
            - 1: Moving Target. Moves horizontally across the screen.
            - 2: Vertical moving target.
            - 3: Diagonal Moving target.
            - 4: The horror from your nightmares; will go literally anywhere within boundaries with random speed.
        """

        self.x = x
        self.y = y
        self.image = pg.image.load(images["target"])
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.hit = False
        self.type = type
        if self.type == 0:
            self.dx = 0 # These are the immobile targets; they don't move.
            self.dy = 0
        elif self.type == 1:
            self.dx = 1 # These are the horizontal moving targets.
            self.dy = 0
        elif self.type == 2:
            self.dx = 0 # These are the vertical moving targets.
            self.dy = 1
        elif self.type == 3:
            self.dx = 1 # These are the diagonal moving targets.
            self.dy = 1
    def draw(self):
        DISPLAYSURF.blit(self.image, (self.x, self.y))
    def move(self):
        self.x += self.dx
        self.y += self.dy
        if self.type == 4:
            self.dx = random.randint(-3, 3)
            self.dy = random.randint(-3, 3)
        if self.x > SCREEN_W or self.x < 0:
            #Checking boundaries
            self.dx = -self.dx
        if self.y > SCREEN_H or self.y < 0:
            self.dy = -self.dy
        
class Game:
    @staticmethod
    def __init__():  
        global img      
        #Start the game; initialize new variables, backgrounds, etc. here
        DISPLAYSURF.fill(pg.Color("white"))
        DISPLAYSURF.blit(img, (0,0))
        
class Menu:

    @staticmethod
    def menu():
        
        #these are the buttons for the game.
        buttons = []
        buttons.append(pg.Rect(100, 100, 500, 100))
        buttons.append(pg.Rect(100, 250, 800, 100))
        buttons.append(pg.Rect(100, 400, 580, 100))
        while True:
            DISPLAYSURF.fill(pg.Color("white"))
            #these are the variables
            DISPLAYSURF.blit(image, (0,0))
            for i in range (len(buttons)):
                pg.draw.rect(DISPLAYSURF, pg.Color("cyan"), buttons[i])
            f.draw_text("Start Game", pg.Color("red"), 100, 120, 40) #first button
            f.draw_text("Show High Scores", pg.Color ("red"), 100, 270, 40) #second button
            f.draw_text("Quit Playing", pg.Color ("red"), 100, 430, 40) #third button
            

            #If you want to stop playing the game.
            for e in f.ievents():
                if e.type == QUIT:
                    pg.quit()
                    sys.exit()
            pg.display.update()
        
            
            #This tells the computer what to do if you press a certain button, wanting to play the game.
            for event in f.ievents():
                if event.type == MOUSEBUTTONDOWN:
                    m_x, m_y = f.ievents(4) 
                    print(m_x, m_y, "in click")
                    if  buttons[0].collidepoint(m_x, m_y):
                        print("Game Start")
                       
                    elif buttons[1].collidepoint(m_x, m_y):
                        print("Your High Scores")
                        
                    elif buttons[2].collidepoint(m_x, m_y):
                        print("Quit Playing")
                        pg.quit()
                        sys.exit()

           



#Main game loop starts right here.

Menu.menu()

while True:

    DISPLAYSURF.fill(pg.Color("white"))
    
    
    #
    for e in f.ievents():
        if e.type == QUIT:
            pg.quit()
            sys.exit()
    pg.display.update()