#snake game
from sys import *
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT']='1'
import time
import pygame
import random
import mysql.connector as sq
database=sq.connect(host='localhost',user='root',passwd='1923',database='joy')
cursor=database.cursor()
pygame.init()
pygame.mixer.init()

# window (whenever any change in display we have to write display.update())
screen_width=900
screen_height=600
root=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Snake Game')
pygame.display.update()

#Colors
white=(255,255,255)
red=(255,0,0)
black=(0,0,0)
blue=(0,0,255)
green=(0,255,0)

#specific variable

font=pygame.font.SysFont(None,55)

clock=pygame.time.Clock()

def text_screen(text,color,x,y):
    screen_text=font.render(text,True,color)
    root.blit(screen_text,[x,y])
def plot_screen(root,color,skn_list,snake_size):
    for x,y in skn_list:
        pygame.draw.rect(root,color,[x,y,snake_size,snake_size],0,10)
def welcome():
    pygame.mixer.music.load('welcome.mp3')
    pygame.mixer.music.play()
    running=True
    while running:
        root.fill((255,210,210))
        text_screen('Snake Game By Joy',(255,100,155),screen_width/4+50,screen_height/2-100)
        text_screen('Hello bachhoooo..!',(155,155,255),screen_width/4+50,screen_height/2-50)
        text_screen('Game khelne ke liye space dbaye!',(255,80,80),screen_width/6,screen_height/2)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    gameloop()
#gameloop
def gameloop():
    cursor.execute('select highscore from score_manager;')
    data=cursor.fetchone()
    highscore=data[0]
    pygame.mixer.music.load('running.mp3')
    pygame.mixer.music.play(10000)
    running=True
    game_over=False
    snake_x=45
    snake_y=55
    velocity_x=0
    velocity_y=0
    skn_list=[]
    skn_length=1
    init=1
    score=0
    snake_size=15
    fps=120
    food_x=random.randint(20,screen_width-20)
    food_y=random.randint(20,screen_height-20)
    while running:
        if game_over:
            root.fill(black)
            text_screen(text,red,screen_width/3,screen_height/2-100)
            text_screen('GAME OVER! PRESS ENTER TO RESTART',red,screen_width/12,screen_height/2-50)
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    running=False
                elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RETURN:
                        welcome()
        else:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    running=False
                elif event.type == pygame.KEYDOWN:
                    if event.key==pygame.K_RIGHT:
                        if velocity_x==0:
                            velocity_x=init
                            velocity_y=0
                    elif event.key==pygame.K_LEFT:
                        if velocity_x==0:
                            velocity_x=-init
                            velocity_y=0
                    elif event.key==pygame.K_UP:
                        if velocity_y==0:    
                            velocity_y=-init
                            velocity_x=0
                    elif event.key==pygame.K_DOWN:
                        if velocity_y==0:    
                            velocity_y=init
                            velocity_x=0
            snake_x+=velocity_x
            snake_y+=velocity_y
            root.fill(black)
            text_screen('SCORE : '+str(score)+' Highscore : '+str(highscore),red,0,0)
            if abs(snake_x-food_x)<15 and abs(snake_y-food_y)<15:
                score+=10
                skn_length+=5  
                food_x=random.randint(20,screen_width-20)
                food_y=random.randint(20,screen_height-20)
                if init<4:
                    init+=0.125
            head=[]
            head.extend([snake_x,snake_y])
            skn_list.append(head)
            pygame.draw.rect(root,green,[food_x,food_y,snake_size,snake_size],0,50)
            plot_screen(root,blue,skn_list,snake_size)
            if len(skn_list)>skn_length:
                skn_list.pop(0)
            if head in skn_list[:-1]:
                game_over=True
                pygame.mixer.music.load('game_over.mp3')
                pygame.mixer.music.play()
            if snake_x<=0:
                snake_x=screen_width
            elif snake_x>=screen_width:
                snake_x=0
            elif snake_y<=0:
                snake_y=screen_height
            elif snake_y>=screen_height:
                snake_y=0
        pygame.display.update()
        clock.tick(fps)
        if highscore<score:
            highscore=score
            text=f'NEW HIGHSCORE : {highscore}'
        else:
            text=f'HIGHSCORE : {highscore}'
    cursor.execute(f'update score_manager set highscore={highscore};')
    database.commit()
    pygame.mixer.music.load('bye.mp3')
    pygame.mixer.music.play()
    time.sleep(0.5)
    pygame.quit()
    exit()
welcome()