import os
from utils import *
import pygame, sys, random
clock = pygame.time.Clock() 
from pygame.locals import * 
from pygame import mixer
pygame.init() 

mixer.init()
pygame.display.set_caption('CorriRuto')

WINDOW_SIZE = (1000,600)
screen = pygame.display.set_mode(WINDOW_SIZE,0,32)

player_walkR = [pygame.image.load('assets/naruto1d.png'), pygame.image.load('assets/naruto2d.png'), pygame.image.load('assets/naruto3d.png'), pygame.image.load('assets/naruto4d.png'), pygame.image.load('assets/naruto5d.png'), pygame.image.load('assets/naruto6d.png'), pygame.image.load('assets/naruto7d.png'), pygame.image.load('assets/naruto8d.png'), pygame.image.load('assets/naruto9d.png'), pygame.image.load('assets/naruto10d.png'), pygame.image.load('assets/naruto11d.png'), pygame.image.load('assets/naruto12d.png'), pygame.image.load('assets/naruto13d.png'), pygame.image.load('assets/naruto14d.png'), pygame.image.load('assets/naruto15d.png')] #carrega a imagem do meu personagem
player_walkL = [pygame.image.load('assets/naruto1e.png'), pygame.image.load('assets/naruto2e.png'), pygame.image.load('assets/naruto3e.png'), pygame.image.load('assets/naruto4e.png'), pygame.image.load('assets/naruto5e.png'), pygame.image.load('assets/naruto6e.png'), pygame.image.load('assets/naruto7e.png'), pygame.image.load('assets/naruto8e.png'), pygame.image.load('assets/naruto9e.png'), pygame.image.load('assets/naruto10e.png'), pygame.image.load('assets/naruto11e.png'), pygame.image.load('assets/naruto12e.png'), pygame.image.load('assets/naruto13e.png'), pygame.image.load('assets/naruto14e.png'), pygame.image.load('assets/naruto15e.png')]
player_jump = [pygame.image.load('assets/jumped.png'), pygame.image.load('assets/jumpe.png')]
obstaculo_sprite = pygame.image.load('assets/obstaculo1.png')
obstaculo1_sprite = pygame.image.load('assets/obstaculo2.png')
bg = pygame.image.load('assets/background.png')
home = pygame.image.load('assets/home.png')
play = pygame.image.load('assets/play.png')
instructions = pygame.image.load('assets/instructions.png')
exit = pygame.image.load('assets/exit.png')
gameOver= pygame.image.load('assets/gameOver.png')
playAgainGameOver= pygame.image.load('assets/playAgainGameOver.png')
exitGameOver= pygame.image.load('assets/exitGameOver.png')
last = "right"

pulo = False
moving_right = False
moving_left = False
vertical_momentum = 0
air_timer = 0
walkCount = 0
wait = 0

player_location = [-3,536]
player_y_momentum = 1

player_rect = pygame.Rect(player_location[0],player_location[1],player_walkL[0].get_width(),player_walkL[0].get_height())#isso aqui eh pra tratar colisao

array_rect = [0, 590]
minGap=250
maxGap=950
obstaculo_X1=900
obstaculo_Y=510
obstaculo_X2=random.randint(900+minGap, 900+maxGap)
obstaculo_X3=random.randint(obstaculo_X2+minGap, obstaculo_X2+maxGap)
lastObstacle=obstaculo_X3
speed=-8
posbgX = 0

fd = os.open(PATH, os.O_RDWR)
print('Arquivo aberto com sucesso!')

def game_over():
    global fd
    global player_location, obstaculo_X1, obstaculo_Y, obstaculo_X2, obstaculo_X3, lastObstacle, speed, posbgX, array_rect
    global player_rect, player_y_momentum, walkCount, air_timer, vertical_momentum, moving_left
    global moving_right, pulo, player_location, minGap, maxGap

    sprites_screen2 = [1, 0, 0]

    while True:
        button = read_button(fd=fd, show_output_msg=False)

        if BUTTONS_OPTIONS[button] == "START":
            player_location = [-3, 536] 
            obstaculo_X1=900
            obstaculo_Y=510
            obstaculo_X2=random.randint(900+minGap, 900+maxGap)
            obstaculo_X3=random.randint(obstaculo_X2+minGap, obstaculo_X2+maxGap)
            lastObstacle=obstaculo_X3
            pulo = False
            moving_right = False
            moving_left = False
            vertical_momentum = 0
            air_timer = 0
            walkCount = 0
            minGap=250
            maxGap=950

            player_y_momentum = 1

            player_rect = pygame.Rect(player_location[0],player_location[1],player_walkL[0].get_width(),player_walkL[0].get_height())#isso aqui eh pra tratar colisao

            array_rect = [0, 590]
            speed=-6
            posbgX = 0

            game_loop()
        elif BUTTONS_OPTIONS[button] == "UP":
            pygame.quit()
            quit()

        if sprites_screen2[0]: screen.blit(gameOver, (0,0))
        if sprites_screen2[1]: screen.blit(playAgainGameOver, (0,0))
        if sprites_screen2[2]: screen.blit(exitGameOver, (0,0))

        pygame.display.update()

def redrawGameWindow():
    global walkCount
    
    if walkCount+1 >= 75:
        walkCount = 0
    
    if (moving_left) and (pulo == False):
        screen.blit(player_walkL[walkCount//5], (player_location[0], player_location[1]))
        walkCount += 1
    elif (moving_right) and (pulo == False):
        screen.blit(player_walkR[walkCount//5], (player_location[0], player_location[1]))
        walkCount += 1
    elif pulo:
        if last == "right":
            screen.blit(player_jump[0], (player_location[0], player_location[1]))
        if last == "left":
            screen.blit(player_jump[1], (player_location[0], player_location[1]))
    else:
        if last == "right":
            screen.blit(player_walkR[0], (player_location[0], player_location[1]))
        if last == "left":
            screen.blit(player_walkL[0], (player_location[0], player_location[1]))

    pygame.display.update()

increase_speed = pygame.USEREVENT+1
pygame.time.set_timer(increase_speed, 500)

def game_loop():
    global fd 
    global posbgX, obstaculo_Y, obstaculo_X1, obstaculo_X2,obstaculo_X3, moving_right, moving_left, vertical_momentum, speed, array_rect, obstaculo_sprite, obstaculo1_sprite
    global player_location, player_rect, pulo, walkCount, last, wait, minGap, maxGap, lastObstacle

    while True:
        clock.tick(60)
        screen.blit(bg, (posbgX,0))
        screen.blit(bg, (posbgX+1000,0))
        screen.blit(obstaculo_sprite, (obstaculo_X1, obstaculo_Y))
        screen.blit(obstaculo_sprite, (obstaculo_X2, obstaculo_Y))
        screen.blit(obstaculo_sprite, (obstaculo_X3, obstaculo_Y))

        if posbgX > -1000:
            posbgX -= 1
        else:
            posbgX = 0

        button = read_button(fd=fd, show_output_msg=False)

        if BUTTONS_OPTIONS[button] != "OFF": 
            if (BUTTONS_OPTIONS[button] == "RIGHT"):
                moving_right = True
                last = "right"
            elif (BUTTONS_OPTIONS[button] == "LEFT"):
                moving_left = True
                last = "left"
            elif ((BUTTONS_OPTIONS[button] == "UP") or (BUTTONS_OPTIONS[button] == "RIGHT-UP") or (BUTTONS_OPTIONS[button] == "LEFT-UP")) and (pulo == False):
                pulo = True
                if air_timer < 6:
                    vertical_momentum = -12
            else:
                moving_left = False
                moving_right = False
                walkCount = 0
        else:
            moving_left = False
            moving_right = False
            walkCount = 0

        if moving_right == True:
            if player_location[0] < 1000:
                player_location[0] += 6 
            else:
                player_location[0] = 1000
        if moving_left == True:
            if player_location[0] > 0:
                player_location[0] -= 6 
            else:
                player_location[0] = 0
        player_location[1] += vertical_momentum
        vertical_momentum += 0.6
        if vertical_momentum > 8:
            vertical_momentum = 8
        
        
        player_rect.x = player_location[0]
        player_rect.y = player_location[1]
        
        test_rect2 = pygame.Rect(array_rect[0], array_rect[1], 1000, 10)
        obstaculo1= pygame.Rect(obstaculo_X1, obstaculo_Y, obstaculo_sprite.get_width(), obstaculo_sprite.get_height())
        obstaculo2= pygame.Rect(obstaculo_X2, obstaculo_Y, obstaculo_sprite.get_width(), obstaculo_sprite.get_height())
        obstaculo3= pygame.Rect(obstaculo_X3, obstaculo_Y, obstaculo_sprite.get_width(), obstaculo_sprite.get_height())

        obstaculo1
        obstaculo_X1+=speed
        obstaculo_X2+=speed
        obstaculo_X3+=speed
        lastObstacle+=speed

        if (obstaculo_X1<-60):
            obstaculo_X1=random.uniform(lastObstacle+minGap, lastObstacle+maxGap)
            lastObstacle=obstaculo_X1

        if (obstaculo_X2<-60):
            obstaculo_X2=random.uniform(lastObstacle+minGap, lastObstacle+maxGap)
            lastObstacle=obstaculo_X2

        if (obstaculo_X3<-60):
            obstaculo_X3=random.uniform(lastObstacle+minGap, lastObstacle+maxGap)
            lastObstacle=obstaculo_X3

        if player_rect.colliderect(test_rect2):
            player_location[1] = array_rect[1]-player_walkL[0].get_height()
            pulo = False
    
        if player_rect.colliderect(obstaculo1):
            pulo = False
            game_over()
        
        if player_rect.colliderect(obstaculo2):
            pulo = False
            game_over()
        
        if player_rect.colliderect(obstaculo3):
            pulo = False
            game_over()

        for event in pygame.event.get():    
            if event.type == increase_speed:
                if event.type == increase_speed:
                    speed -= 0.1
                    minGap += 6
                    maxGap += 6

            if event.type == QUIT:
                pygame.quit() 
                sys.exit()

        redrawGameWindow()

def game_intro():
    global fd

    sprites_screen = [1, 0, 0, 0]

    while True:
        button = read_button(fd=fd, show_output_msg=False)  

        if BUTTONS_OPTIONS[button] == "START":
            game_loop()

        if sprites_screen[0] : screen.blit(home, (0,0))
        if sprites_screen[1] : screen.blit(play, (0,0))
        if sprites_screen[2] : screen.blit(instructions, (0,0))
        if sprites_screen[3] : screen.blit(exit, (0,0))
        pygame.display.update()
        clock.tick(90)

game_intro()
