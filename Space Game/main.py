
#Imports pygame, os, and random modules.

import pygame
pygame.init()
import os
import random
from random import randrange
pygame.font.init()
pygame.mixer.init()

#Sets width and height of display screen.
WIDTH, HEIGHT = 1400, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

#sets caption at left hand corner.
pygame.display.set_caption("Space Shooter Game!")

#List of powerups selected at random when ship colldies with satr.
powerups = ['speed', 'bullet_vel', 'bullet']

#Stores rbg values of colours into variables.
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (0, 255, 0)

#Sets dimensions of border.
BORDER = pygame.Rect(0, HEIGHT//2 - 5 , WIDTH, 10 )

#creaets sound objects for fire and hit sound efeftcs and stores these in associated variables.
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('assets', 'blast.mp3'))
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('assets', 'explosion.mp3'))

#Stores font of health bar and winenr emssage in respective variables.
HEALTH_FONT = pygame.font.SysFont('consolas', 50)
WINNER_FONT = pygame.font.SysFont('consolas ', 175 )

#Sets the default numerical values for bullet speed, maximum number of bullets, velocity of spaceships, and frames per second.
BULLET_VEL_RED = 7
BULLET_VEL_YELLOW = 7
MAX_BULLETS_YELLOW = 3
MAX_BULLETS_RED = 3
VEL_RED = 5
VEL_YELLOW = 5
FPS = 60

#Sets dimensions for witdth and height of spaceships.
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 200, 85

#Creates unqiue events for when either one of the spaceships are hit or when a powerup is obtained.
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2 
POWER_YELLOW = pygame.USEREVENT + 3
POWER_RED = pygame.USEREVENT + 4

#Creates image object to access spaceship png images and rescales and rotates this accordingly.
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('assets', 'destroyer.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),360)

#Creates  image object to access second spaceship png image and rescales and rotates this accordingly.
RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('assets', 'falcon.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 360)

#Creates image object to access powerup star png image and rescales and rotates this accordingly.
POWERUP_IMAGE = pygame.image.load(
    os.path.join('assets', 'star.png'))
POWERUP = pygame.transform.rotate(pygame.transform.scale(POWERUP_IMAGE, (50, 50)), 0)

#Sets the space background of the game.
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'space.png')), (WIDTH, HEIGHT))

#Function for drawing all objects to window.
def draw_window(red, yellow,  red_bullets, yellow_bullets, red_health, yellow_health, star):
    WIN.blit(SPACE, (0,0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    
    #Renders health bars for each spaceships in the top right and left corners.
    red_health_text = HEALTH_FONT.render(
        "Health Points: " + str(red_health), 1, GREEN)
    yellow_health_text = HEALTH_FONT.render(
        "Health Points: " + str(yellow_health), 1, GREEN)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

#Blits the spaceships adn powerup to screen.
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    WIN.blit(POWERUP, (star.x, star.y ))
    
    #Draws bullets to the screen when fired.
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in  yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    
    #Updates the display.
    pygame.display.update()

#Funciton for determining  which powerup is sleected and to whom it applies.
def buff_effect(buff, colour):
    global VEL_YELLOW
    global VEL_RED
    global MAX_BULLETS_RED
    global MAX_BULLETS_YELLOW
    global BULLET_VEL_YELLOW
    global BULLET_VEL_RED
    
    #Checks all possible cases for each ship and applies appropriate powerup.
    if colour == "yellow":
        if buff == "speed":
            VEL_YELLOW = 15
        elif buff == "bullet":
            MAX_BULLETS_YELLOW = 5
        elif buff == "bullet_vel":
            BULLET_VEL_YELLOW = 20

    elif colour == "red":
        if buff == "speed":
            VEL_RED = 15
        elif buff == "bullet":
            MAX_BULLETS_RED = 5
        elif buff == "bullet_vel":
            BULLET_VEL_RED = 20

#Checks and posts a powerup event if ship 1 is found to collide with the powerup.
def star_collide_yellow(yellow, star):
    if yellow.colliderect(star):
        pygame.event.post(pygame.event.Event(POWER_YELLOW))

#Defines movement keys for ship 1.
def yellow_handle_movement(keys_pressed, yellow, star):
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_s] and yellow.x - VEL_YELLOW > 0:#Change
        yellow.x -= VEL_YELLOW 
        star_collide_yellow(yellow, star)
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_f] and yellow.x + VEL_YELLOW + yellow.width < 1400:#Change
        yellow.x += VEL_YELLOW 
        star_collide_yellow(yellow, star)
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_e] and yellow.y - VEL_YELLOW + yellow.height < HEIGHT/2 - 15 :#Change
        yellow.y += VEL_YELLOW
        star_collide_yellow(yellow, star)
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_d] and yellow.y - VEL_YELLOW > -5 :#Change
        yellow.y -= VEL_YELLOW 
        star_collide_yellow(yellow, star)

#Checks and posts a powerup event if ship 1 is found to collide with the powerup.
def star_collide_red(red, star):
    if red.colliderect(star):
        pygame.event.post(pygame.event.Event(POWER_RED))

#Defines movement keys for ship 2.
def red_handle_movement(keys_pressed, red, star):
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_j] and red.x - VEL_RED > 0:#Change
        red.x -= VEL_RED
        star_collide_red(red, star)
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_l] and red.x + VEL_RED + red.width < 1400:#Change
        red.x += VEL_RED 
        star_collide_red(red, star)
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_k] and red.y + VEL_RED + red.height < 800:
        red.y += VEL_RED
        star_collide_red(red, star)
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_i] and red.y - VEL_RED > HEIGHT/2 + 5 :#Change
        red.y -= VEL_RED
        star_collide_red(red, star)

#Controls movement of  ship 1's bullets across the screen and ensures that only 3 can be fired at a time.
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
   for bullet in yellow_bullets:
       bullet.y += BULLET_VEL_YELLOW
       if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
       elif bullet.y > HEIGHT:
            yellow_bullets.remove(bullet)

#Controls movement of  ship 2's bullets across the screen and ensures that only 3 can be fired at a time.
   for bullet in red_bullets:
       bullet.y -= BULLET_VEL_RED
       if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
       elif bullet.y < 0:
           red_bullets.remove(bullet)

#Displays winenr text messege to the screen.
def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, (255, 0, 0))
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    global VEL_YELLOW
    global VEL_RED
    global MAX_BULLETS_RED
    global MAX_BULLETS_YELLOW
    global BULLET_VEL_RED
    global BULLET_VEL_YELLOW

#resets all global variables to their original default settings before starting new game.
    VEL_RED = 5
    VEL_YELLOW = 5
    MAX_BULLETS_RED = 3
    MAX_BULLETS_YELLOW = 3
    BULLET_VEL_YELLOW = 7
    BULLET_VEL_RED = 7
    pygame.display.update()
    pygame.time.delay(5000)
    

#Randomly selects star's y position to dteermine whetehr it appears at the top half or bottom half of the screen.
y_position = [175, 625]
rand_index = randrange(len(y_position))
star_y = y_position[rand_index]


#The main fucntion which handles most of the game's functionality.
def main():
    
    #draws the sapceships and star to the screen.
    red = pygame.Rect(300, 700, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(1100, 100, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    star = pygame.Rect(700, star_y, 50, 50)

    #Creates empty lists storing each of the two ships' respective bullets fired onto the screen.
    red_bullets = []
    yellow_bullets = []

    #Sets health for each ship.
    red_health = 10
    yellow_health = 10

    #Defines clock for the game.
    clock = pygame.time.Clock()
    run = True
    while run:
        #Runs the clock at the rate of frames per second.
        clock.tick(FPS)
        #Exits the game if the user quits.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            #Codes the funtionality for the movement of both ships' fired bullets.
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS_YELLOW:
                    bullet =  pygame.Rect(
                        yellow.x + yellow.width//2 - 2, yellow.y + yellow.height, 5, 30)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS_RED:
                    bullet =  pygame.Rect(
                        red.x + red.width//2 - 2, red.y, 5, 30)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            #Decrements the health of each ship when they are hit by the other's bullets.
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()
            
            #Selects a powerup at random to apply to the ship that collides with teh star.
            if event.type == POWER_YELLOW:
                rand_ind = randrange(len(powerups))
                buff = powerups[rand_ind]
                print(buff)
                star.move_ip(1000, 1000)
                buff_effect(buff, 'yellow')

            if event.type == POWER_RED:
                rand_ind = randrange(len(powerups))
                buff = powerups[rand_ind]
                print(buff)
                star.move_ip(1000, 1000)
                buff_effect(buff, 'red')


        #Sets the winner text depending on who's health reduces to 0 first.
        winner_text = ""
        if red_health < 0:
            winner_text = "Yellow Victory!"
            
        if yellow_health < 0:
            winner_text = "Red Victory!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        #Keeps track of keys pressed and passes those into teh respective fuctions handling the ships' movements.
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow, star)
        red_handle_movement(keys_pressed, red, star)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        
        #Draws all objects and text to the screen for every iteration.
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, star)

    #recursively calls the main function.
    main()

#Runs the main function when main.py is open.
if __name__ == "__main__":
    main()
