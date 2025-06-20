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
#This sets up the screen coordinates.
SCREEN_H = 600
SCREEN_W = 1000

pg.init()
DISPLAYSURF = pg.display.set_mode((SCREEN_W, SCREEN_H))
font = pg.font.FontType("AtariClassic-gry3.ttf")

images = {
    "background": "Wild West.png", #This sets the Wild West-esque background.
    "target": "Target.png", #This uploads the targets the players have to shoot to get points.
    "explosion": "Explosion.png", #This uploads the explosion!
    "bullets": "bullet(1).png" # use a laser/plasma blast-looking bullet image to keep it kid friendly 


}
image = pg.image.load(images["background"])
#Setup
#Global Constants

#This
class highScores():
    try:
        highscores = open("highscores.txt", "r")
        n = int(highscores.readline())
        for i in range(n):
            score = highscores.readline().split()
            #read the second part of the line and int it
            score[1] = int(score[1])
        highscores.close()
    except:
        # If the file is broken or doesn't exist, create a new one
        with open("highscores.txt", "w") as f:
            f.write("0\n")

    @staticmethod
    def get_highscores():
        scores = []
        try:
            with open("highscores.txt", "r") as f:
                n = int(f.readline())
                for _ in range(n):
                    line = f.readline()
                    if not line:
                        break
                    name, score = line.strip().split()
                    scores.append((name, int(score)))
        except Exception:
            print('da file is vroken i guess so skill issue ')
        return scores

    @staticmethod
    def save_highscores(scores):
        with open("highscores.txt", "w") as f:
            f.write(f"{len(scores)}\n")
            for name, score in scores:
                f.write(f"{name} {score}\n")

    @staticmethod
    def add_score(name, score):
        scores = highScores.get_highscores()
        scores.append((name, score))
        # Sort descending by score, keep top 10
        scores = sorted(scores, key=lambda x: x[1], reverse=True)[:10] #I learned about lambda functions from Mimo, the coding learning app. It's like a duolingo for coding.
        # Save the updated scores
        highScores.save_highscores(scores)
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

    def input_textbox(prompt, x, y, width, height):
        """
        Displays a textbox for user input and returns the input text.
        """
        input_text = ""
        
        clock = pg.time.Clock()
        
        while True:
            DISPLAYSURF.fill(pg.Color("white"))
            text_length = len(input_text)*30
            if width + text_length > SCREEN_W - 30:
                box_width = SCREEN_W - x - 10  # Prevent box from going off screen
                input_text = input_text[:-1]
            else:
                box_width = width + text_length
                
            pg.draw.rect(DISPLAYSURF, pg.Color("black"), (x, y-1, box_width - 30, height+1), 2)
            f.draw_text(prompt, pg.Color("black"), x - 20, y - 200, 30)
            f.draw_text(input_text, pg.Color("black"), x , y + 5, 30)

            for event in f.ievents():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        return input_text
                    elif event.key == K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode
            #This is the clock here.
            pg.display.update()
            clock.tick(30)

class Targets:
    targets = []  # This is a list of all targets in the game.
    def __init__(self, x, y, type):
        """
        Type:

            - 0: Static/Immobile Target. Doesn't move.
            - 1: Moving Target. Moves horizontally across the screen.
            - 2: Vertical moving target.
            - 3: Diagonal Moving target.
            - 4: The horror from your nightmares; will go literally anywhere within boundaries with random speed.
        """

        #This part includes all the variables needed for the targets.
        self.x = x
        self.y = y
        self.image = pg.image.load(images["target"])
        self.image = pg.transform.scale(self.image, (100, 100))  # Resize the target image
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.hit = False
        self.type = type
        if self.type == 0:
            self.dx = 0 # These are the stationary targets.
            self.dy = 0
        elif self.type == 1:
            self.dx = 1 # These are the horizontally moving targets.
            self.dy = 0
        elif self.type == 2:
            self.dx = 0 # These are the vertically moving targets.
            self.dy = 1
        elif self.type == 3:
            self.dx = 1 # These are the diagonally moving targets.
            self.dy = 1
        else:
            self.dx, self.dy = random.randint(-3, 3), random.randint(-3, 3)  # Random speed for the horror target.
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
#This tells the bullets what to do: bounce off the targets and hit it!            
class bullets:
    bullets = []
    def __init__(self, x, y):
        self.x = x
        self.mouse_x = x
        self.mouse_y = y
        self.y = SCREEN_H + 50  # Bullets bounce off the bottom of the screen
        self.ygoal = y  # The y-coordinate of the target
        self.image = pg.image.load(images["bullets"])  # Load the bullet image
        self.image = pg.transform.scale(self.image, (50, 50))  # Resize the bullet image
        self.hit = False
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.reached = False  # This is to check if the bullet has reached the target.
    def draw(self):
        #This is where the bullet is drawn.
        
        DISPLAYSURF.blit(self.image, (self.x, self.y))
        
    def move(self):
        #This is where the bullet moves.
        if not self.reached:
            for i in range(0,5):
                if self.y == self.ygoal:
                   
                    self.reached = True
                    bullets.bullets.remove(self)
                    return True, self.mouse_x, self.mouse_y  # Remove the bullet if it has reached the target

                self.y -= 1 
#This is where the code for the game itself is: times the game, makes the targets get hit and gives the player points.
class Game:
    SCORE = 0
    @staticmethod
    def __init__():
        global image
        # Start the game; initialize new variables, backgrounds, etc. here
        intro = True
        clock = pg.time.Clock()
        intro_start_time = pg.time.get_ticks()
        print("started intro")
        #This starts the game like a "On your mark, get set, go!" function!
        while intro:

            DISPLAYSURF.fill(pg.Color("white"))
            DISPLAYSURF.blit(image, (0, 0))
            f.draw_text("Get Ready!", pg.Color("red"), 100, 100, 40)
            events = f.ievents()
            for e in events:
                if e.type == QUIT:
                    pg.quit()
                    sys.exit()

            # Use total elapsed time since intro started
            if pg.time.get_ticks() - intro_start_time > 2000:
                intro = False
            pg.display.update()
            clock.tick(60)  # Limit the frame rate to 60 FPS
        # After the intro, start the main game loop
        print("started game loop")
        time = 0 # This is the timer for the game. After 120 seconds (2 minutes), the game ends.
        while time < 120:
            time += 1/120  # Increment time by 1/120 seconds (assuming 120 FPS)
            clock.tick(120)  # Limit the frame rate to 120 FPS
            DISPLAYSURF.fill(pg.Color("white"))
            DISPLAYSURF.blit(image, (0, 0))
            events = f.ievents()
            for e in events:
                if e.type == QUIT:
                    pg.quit()
                    sys.exit()
                if e.type == MOUSEBUTTONDOWN:
                    m_x, m_y = f.ievents(4)
                    if e.button == 1:  # Left mouse button
                        # Create a new bullet at the mouse position
                        new_bullet = bullets(m_x, m_y)
                        bullets.bullets.append(new_bullet)
                        # pg.mixer.Sound(sounds["shoot"]).play()
            if len(Targets.targets) < 1:
                
                # Spawn a new target
                if random.randint(0, 100) < 99:
                    target = Targets(random.randint(0, SCREEN_W), random.randint(0, SCREEN_H), random.randint(0, 4))
                    Targets.targets.append(target)
            elif len(Targets.targets) > 10:
                if random.randint(0, 100) < 5:
                    # add targets slower if there are more than 10 targets
                    target = Targets(random.randint(0, SCREEN_W), random.randint(0, SCREEN_H), random.randint(0, 4))
                    Targets.targets.append(target)
            elif 0 < len(Targets.targets) < 10:
                if random.randint(0, 700) <= 5:
                    target = Targets(random.randint(0, SCREEN_W), random.randint(0, SCREEN_H), random.randint(0, 4))
                    Targets.targets.append(target)

            #This says that targets should show how many points you earned from hitting the target: 1, 15, 30, or 50.
            for target in Targets.targets:
                target.move()
                target.draw()
            for bullet in bullets.bullets[:]:
                result = bullet.move()
                if result:
                    hit, x, y = result
                else:
                    hit = False
                bullet.draw()
                if hit:
                    # Handle bullet hitting the target
                    for target in Targets.targets:
                        # Check if bullet is within a radius of the target's width
                        distance = ((bullet.mouse_x - (target.x + target.image.get_width() // 2)) ** 2 + (bullet.mouse_y - (target.y + target.image.get_height() // 2)) ** 2) ** 0.5
                        if distance <= target.image.get_width():
                            target.hit = True
                            # Calculate score based on distance

                            #This says you get 50 POINTS if you get it exactly on the target!
                            if distance < 1:
                                Game.SCORE += 50
                                text = f"+50"

                            #This says you get 15 points if you get it close enough to the target.
                            elif 1 < distance < 15:
                                Game.SCORE += 15
                                text = f"+15"

                            #This says you get 5 points if you get it not that close to the target.
                            elif 15 < distance < 30:
                                Game.SCORE += 5
                                text = f"+5"
                            #If it's far from the target:
                            else:
                                Game.SCORE += 1
                                text = f"+1"
                               
                            # pg.mixer.Sound(sounds["explosion"]).play()
                            target.image = pg.image.load(images["explosion"])  # Loade the explosion image
                            target.image = pg.transform.scale(target.image, (150, 150))  # Resize the explosion image
                            f.draw_text(text, pg.Color("green"), target.x - 55, target.y - 50, 50)  # Display the score text
                            DISPLAYSURF.blit(target.image, (target.x - 25 , target.y - 25))  # This displays the explosion.
                            pg.display.update()
                            #This is the timer.
                            for i in range(0, 5):
                                pass
                                clock = pg.time.Clock()
                                clock.tick(60)
                            Targets.targets.remove(target)
                            break
                    if bullet in bullets.bullets:
                        bullets.bullets.remove(bullet)
            #Displays how much points you've earned.
            f.draw_text(f"Score: {Game.SCORE}", pg.Color("black"), 10, 10, 30)
            f.draw_text(f"Time: {int(120 - time)}", pg.Color("black"), 10, 50, 30)  # Display the timer
            
            pg.display.update()
        f.draw_text("Game Over!", pg.Color("red"), SCREEN_W // 2 - 100, SCREEN_H // 2 - 50, 50)
        f.draw_text(f"Final Score: {Game.SCORE}", pg.Color("black"), SCREEN_W // 2 - 100, SCREEN_H // 2 + 10, 40)
        
        name = f.input_textbox("Enter your name:", SCREEN_W // 2 - (15*30), SCREEN_H // 2 + 110, 200, 40)
        highScores.add_score(name, Game.SCORE)
        print (highScores.get_highscores())

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
            
            # Get all events once per loop
            events = f.ievents()
            #If you want to stop playing the game.
            for e in events:
                if e.type == QUIT:
                    pg.quit()
                    sys.exit()
            pg.display.update()
        
            # Handle button clicks for menu actions
            for event in events:
                if event.type == MOUSEBUTTONDOWN:
                    m_x, m_y = f.ievents(4)
                    if buttons[0].collidepoint(m_x, m_y):
                        Game()
                    elif buttons[1].collidepoint(m_x, m_y):
                        # Show High Scores
                        scores = highScores.get_highscores()
                        inMenu = True
                        while inMenu:
                            DISPLAYSURF.fill(pg.Color("white"))
                            DISPLAYSURF.blit(image, (0, 0))
                            f.draw_text("High Scores", pg.Color("black"), 100, 50, 40)
                            y_offset = 100
                            for name, score in scores:
                                f.draw_text(f"{name}: {score}", pg.Color("blue"), 100, y_offset, 30)
                                y_offset += 40
                            # Draw return button
                            return_btn = pg.Rect(100, y_offset + 30, 525, 75)
                            pg.draw.rect(DISPLAYSURF, pg.Color("cyan"), return_btn)
                            f.draw_text("Return to Menu", pg.Color("blue"), 110, y_offset + 45, 30)
                            pg.display.update()
                            for e in f.ievents():
                                if e.type == QUIT:
                                    pg.quit()
                                    sys.exit()
                                if e.type == MOUSEBUTTONDOWN:
                                    mx, my = f.ievents(4)
                                    if return_btn.collidepoint(mx, my):
                                        inMenu = False

                        
                    elif buttons[2].collidepoint(m_x, m_y):
                        print("Quit Playing")
                        pg.quit()
                         
                        sys.exit()

#Main game loop starts right here.
pg.display.set_caption("Carnival Game")
Menu.menu()

while True:

    DISPLAYSURF.fill(pg.Color("white"))
    
    
    #
    for e in f.ievents():
        if e.type == QUIT:
            pg.quit()
            sys.exit()
    pg.display.update()