#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
from pygame.locals import *
from Snake3 import Snake3
import sys
import MySQLdb
from MenuOption import MenuOption
import pygame
class Game():
    WIDTH=640
    HEIGHT=670
    BACKGROUND_COLOR=(193,255,193)
    gameDisplay=None
    clock=None
    options=None
    SIZE=30
    SNAKE_SIZE=20
    score=0
    TICK=15
    def __init__(self):
        pygame.init()
        self.gameDisplay = pygame.display.set_mode((self.WIDTH,self.HEIGHT),0,0)
        self.clock = pygame.time.Clock()
        self.options=[MenuOption(self.gameDisplay,pygame.Rect(120,250,400,50),"NEW GAME",30),
        MenuOption(self.gameDisplay,pygame.Rect(120,330,400,50),"LOCAL HIGHSCORES",30),
        MenuOption(self.gameDisplay,pygame.Rect(120,410,400,50),"INTERNET HIGHSCORES",30),
        MenuOption(self.gameDisplay,pygame.Rect(120,490,400,50),"QUIT",30)]
    def start(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    for i in range(len(self.options)):
                        if self.options[i].getRect().collidepoint(pos):
                            if i==0:
                                self.gameLoop()
                            if i==2:
                                self.internetScoresLoop()
            self.gameDisplay.fill((193,255,193))
            for option in self.options:
                pos = pygame.mouse.get_pos()
                if option.getRect().collidepoint(pos):
                    option.hovered=True
                else:
                    option.hovered=False
                option.draw()
            self.drawHeader()
            pygame.display.update()
            pygame.display.flip()
            self.clock.tick(self.TICK)
            
    def gameLoop(self):
        running=False
        while True:
            snake=Snake3(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key==pygame.K_SPACE:
                        running=True
                        break
                    if event.key==pygame.K_ESCAPE:
                        return
            self.gameDisplay.fill((193,255,193))
            self.drawBounds()
            if snake.score!=0:
                self.displayScore()
            self.startText()
            pygame.display.update()
            pygame.display.flip()
            self.clock.tick(self.TICK)
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running=False
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key==pygame.K_LEFT:
                            snake.setDirection('LEFT')
                            snake.move()
                            continue
                        elif event.key==pygame.K_RIGHT:
                            snake.setDirection('RIGHT')
                            snake.move()
                            continue
                        elif event.key==pygame.K_UP:
                            snake.setDirection('UP')
                            snake.move()
                            continue
                        elif event.key==pygame.K_DOWN:
                            snake.setDirection('DOWN')
                            snake.move()
                            continue
                if snake.canMove():
                    snake.move()
                else:
                    running=False
                    self.gameOverLoop(snake.score)
                self.gameDisplay.fill((193,255,193))
                self.drawBounds()
                self.drawSnake(snake)
                self.showScore(snake.score,snake.appleScore)
                snake.appleScore=snake.appleScore-1
                pygame.display.update()
                pygame.display.flip()
                self.clock.tick(self.TICK)
    
    def gameOverLoop(self,punkty):
        text=''
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if (event.key>47 and event.key<58) or (event.key>96 and event.key<123) and len(text)<20:
                        text+=str(pygame.key.name(event.key))
                    if event.key==13 and len(text)>0:
                        self.saveScore(text,punkty)
                        return
            self.gameDisplay.fill((193,255,193))
            self.drawBounds()
            FONT=pygame.font.SysFont("comicsansms",30)
            TEXT=FONT.render("YOUR SCORE: "+str(punkty),True,(0,255,0))
            self.gameDisplay.blit(TEXT,[170,200,200,50])
            TEXT=FONT.render("INTERNET RANK: "+str(self.internetRank(punkty)+1),True,(0,255,0))
            self.gameDisplay.blit(TEXT,[170,250,200,50])
            TEXT=FONT.render("LOCAL RANK: "+str(324),True,(0,255,0))
            self.gameDisplay.blit(TEXT,[170,300,200,50])
            TEXT=FONT.render("YOUR NICKNAME: ",True,(0,255,0))
            self.gameDisplay.blit(TEXT,[170,350,200,50])
            FONT=pygame.font.SysFont("comicsansms",30)
            TEXT=FONT.render(text,True,(0,0,255))
            self.gameDisplay.blit(TEXT,[170,400,200,50])
            pygame.display.update()
            pygame.display.flip()
            self.clock.tick(self.TICK)
                
    def drawHeader(self):
        FONT=pygame.font.SysFont("Freestyle Script",200)
        TEXT=FONT.render("SNAKE",True,(0,255,0))
        self.gameDisplay.blit(TEXT,[79,7,200,200])
        
    def drawBounds(self):
        BROWN_DARK=(94,38,18)
        pygame.draw.rect(self.gameDisplay,BROWN_DARK,(0,30,20,670),0)
        pygame.draw.rect(self.gameDisplay,BROWN_DARK,(620,30,20,670),0)
        pygame.draw.rect(self.gameDisplay,BROWN_DARK,(20,650,600,20),0)
        pygame.draw.rect(self.gameDisplay,BROWN_DARK,(20,30,600,20),0)
        
    def drawSnake(self,snake):
        head_color=[255,0,0]
        body_color=[0,255,0]
        food_color=[0,0,255]
        position=[snake.foodX*self.SNAKE_SIZE+10+20,snake.foodY*self.SNAKE_SIZE+10+50]
        pygame.draw.circle(self.gameDisplay,food_color,position,10,0)
        position=[snake.snakeX[0]*self.SNAKE_SIZE+10+20,snake.snakeY[0]*self.SNAKE_SIZE+10+50]
        pygame.draw.circle(self.gameDisplay,head_color,position,10,0)
        for i in range(1,len(snake.snakeX)):
            position=[snake.snakeX[i]*self.SNAKE_SIZE+10+20,snake.snakeY[i]*self.SNAKE_SIZE+10+50]
            pygame.draw.circle(self.gameDisplay,body_color,position,10,0)
    
    def internetRank(self,punkty):
        #db = MySQLdb.connect("localhost","root","","snake")
        db = MySQLdb.connect("85.10.205.173","snake","snake123","snakehighscores")
        cur = db.cursor()
        cur.execute("SELECT count(*) from gracze where punkty > "+str(punkty))
        for row in cur.fetchall() :
            return row[0]
    def saveScore(self,gracz,punkty):
        db = MySQLdb.connect("85.10.205.173","snake","snake123","snakehighscores")
        cur = db.cursor()
        cur.execute("INSERT INTO `gracze`(`nick`, `punkty`) VALUES ('"+str(gracz)+"',"+str(punkty)+")")
        db.commit()
    def showScore(self,s,a):
        font=pygame.font.SysFont("comicsansms",20)
        BLUE=(0,0,255)
        score_text=font.render("Score: "+str(s),True,BLUE)
        self.gameDisplay.blit(score_text,[0,0])
        score_text=font.render("Food score: "+str(a),True,BLUE)
        print(str(a))
        self.gameDisplay.blit(score_text,[480,0])
        
    def displayScore(self,punkty):
        FONT=pygame.font.SysFont("Goudy Stout",25)
        TEXT=FONT.render("Liczba punktow: "+punkty,True,(0,255,0))
        self.gameDisplay.blit(TEXT,[170,220,640,30])
    def startText(self):
        FONT=pygame.font.SysFont("Goudy Stout",25)
        TEXT=FONT.render("Press SPACE to start",True,(0,255,0))
        self.gameDisplay.blit(TEXT,[54,300,640,30])
        
    def printScores(self):
        #db = MySQLdb.connect("localhost","root","","snake")
        db = MySQLdb.connect("85.10.205.173","snake","snake123","snakehighscores")
        cur = db.cursor()
        cur.execute("SELECT * FROM `gracze` order by punkty desc limit 20")
        listaGraczy=[]
        listaPunktow=[]
        for row in cur.fetchall() :
            listaGraczy.append(str(row[1]))
            listaPunktow.append(str(row[2]))
    def internetScoresLoop(self):
        db = MySQLdb.connect("85.10.205.173","snake","snake123","snakehighscores")
        cur = db.cursor()
        cur.execute("SELECT * FROM `gracze` order by punkty desc limit 20")
        listaGraczy=[]
        listaPunktow=[]
        for row in cur.fetchall() :
            listaGraczy.append(str(row[1]))
            listaPunktow.append(str(row[2]))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    return
            self.gameDisplay.fill((193,255,193))
            FONT=pygame.font.SysFont("Tahoma",15)
            for i in range(len(listaGraczy)):
                TEXT=FONT.render(str(i+1)+". "+str(listaGraczy[i]),True,(0,255,0))
                self.gameDisplay.blit(TEXT,[54,100+i*20,640,30])
                TEXT=FONT.render(str(listaPunktow[i]),True,(0,255,0))
                self.gameDisplay.blit(TEXT,[300,100+i*20,640,30])
            pygame.display.update()
            pygame.display.flip()
            self.clock.tick(self.TICK)
if __name__ == "__main__":
    Game().start()
    
