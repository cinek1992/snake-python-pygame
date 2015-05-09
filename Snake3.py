# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
import sys
import random

class Snake3():
    score=0
    snakeX=[]
    snakeY=[]
    DIRECTION='LEFT'
    foodX=0
    foodY=0
    SIZE=0
    appleScore=0
    def __init__(self,size):
        self.SIZE=size
        self.snakeX=[]
        self.snakeY=[]
        self.snakeX.append(20)
        self.snakeX.append(21)
        self.snakeX.append(22)
        self.snakeY.append(15)
        self.snakeY.append(15)
        self.snakeY.append(15)
        self.getFood()
    def getFood(self):
        found=False
        self.appleScore=60+len(self.snakeX)
        while not found:
            newX=random.randint(0,self.SIZE-1)
            newY=random.randint(0,self.SIZE-1)
            if not self.search(newX,newY):      
                self.foodX=newX
                self.foodY=newY
                return
            
    def search(self,x,y):
        for i in range(len(self.snakeX)):
            if x==self.snakeX[i] and y == self.snakeY[i]:
                return True
        return False
    
    def getDirection(self):    
        return self.DIRECTION
    
    def move(self):
        headX=0
        headY=0
        if self.DIRECTION=='UP':
            headX=self.snakeX[0]
            headY=self.snakeY[0]-1
            if headX==self.foodX and headY==self.foodY:
                self.score+=self.appleScore
                self.getFood()
            else:
                del self.snakeX[-1]
                del self.snakeY[-1]
            self.DIRECTION='UP'
        elif self.DIRECTION=='DOWN':
            headX=self.snakeX[0]
            headY=self.snakeY[0]+1
            if headX==self.foodX and headY==self.foodY:
                self.score+=self.appleScore
                self.getFood()
            else:
                del self.snakeX[-1]
                del self.snakeY[-1]
            self.DIRECTION='DOWN'
        elif self.DIRECTION=='LEFT':
            headX=self.snakeX[0]-1
            headY=self.snakeY[0]
            if headX==self.foodX and headY==self.foodY:
                self.score+=self.appleScore
                self.getFood()
            else:
                del self.snakeX[-1]
                del self.snakeY[-1]
            self.DIRECTION='LEFT'
        elif self.DIRECTION=='RIGHT':
            headX=self.snakeX[0]+1
            headY=self.snakeY[0]
            if headX==self.foodX and headY==self.foodY:
                self.score+=self.appleScore
                self.getFood()
            else:
                del self.snakeX[-1]
                del self.snakeY[-1]
            self.DIRECTION='RIGHT'
        self.snakeX.insert(0,headX)
        self.snakeY.insert(0,headY)
        
    def canMove(self):
        if self.DIRECTION=='UP' and (self.snakeY[0]-1<0 or self.search(self.snakeX[0],self.snakeY[0]-1)):
            return False
        elif self.DIRECTION=='DOWN' and (self.snakeY[0]+1==self.SIZE or self.search(self.snakeX[0],self.snakeY[0]+1)):
            return False
        elif self.DIRECTION=='LEFT' and (self.snakeX[0]-1<0 or self.search(self.snakeX[0]-1,self.snakeY[0])):
            return False
        elif self.DIRECTION=='RIGHT' and (self.snakeX[0]+1==self.SIZE or self.search(self.snakeX[0]+1,self.snakeY[0])):
            return False
        return True
        
    def setDirection(self,dir):
        if dir=='DOWN':
            if self.DIRECTION=='UP':
                return
            self.DIRECTION='DOWN'
        elif dir=='UP':
            if self.DIRECTION=='DOWN':
                return
            self.DIRECTION='UP'
        elif dir=='RIGHT':
            if self.DIRECTION=='LEFT':
                return
            self.DIRECTION='RIGHT'
        elif dir=='LEFT':
            if self.DIRECTION=='RIGHT':
                return
            self.DIRECTION='LEFT'