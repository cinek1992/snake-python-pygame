# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
from pygame.locals import *
from pygame.locals import *
import pygame
class MenuOption:
    BOX_DARK=(94,38,18)
    BOX_LIGHT=(199,97,20)
    
    BLUE=(0,0,255)
    DISPLAY=None
    RECT=None
    BLUE=(0,0,255)
    TEXT=None
    TextPosX=None
    TextPosY=None
    hovered=False
    
    def __init__(self,display,rect,text,textsize):
        self.DISPLAY=display
        self.RECT=rect
        pygame.font.init()
        self.FONT=pygame.font.SysFont("comicsansms",textsize)
        self.TEXT=self.FONT.render(text,True,self.BLUE)
        textWidth=self.TEXT.get_width()
        textHeight=self.TEXT.get_height()
        self.TextPosX=int((self.RECT.width-textWidth)/2)
        self.TextPosY=int((self.RECT.height-textHeight)/2)
        self.RECT=rect
    def draw(self):
        box_color=self.BOX_DARK
        if self.hovered:
            box_color=self.BOX_LIGHT
        pygame.draw.rect(self.DISPLAY,box_color,self.RECT,0)
        self.DISPLAY.blit(self.TEXT,[self.RECT.x+self.TextPosX,self.RECT.y+self.TextPosY])
        
    def setHovered(self,isHovered):
        self.hovered=isHovered
        
    def getRect(self):
        return self.RECT