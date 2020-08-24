#framework cited from CMU 15112 website
#http://www.cs.cmu.edu/~112/notes/notes-oop.html
from pygamegame import PygameGame
import pygame
import random
from Issac import *
class MakeBoard(pygame.sprite.Sprite):
    def init(self):
        Issac.init(self)
        self.makeBoardbg=pygame.image.load("makeboardbg.png").convert_alpha()
        self.mushroom=pygame.image.load("mushroom.png").convert_alpha()
        self.spines=pygame.image.load("spines.png").convert_alpha()
        self.stone=pygame.image.load("stone2.png").convert_alpha()
        self.pot=pygame.image.load("pot.png").convert_alpha()
        self.mushroomMark=pygame.image.load("mushroommark.png").convert_alpha()
        self.spinesMark=pygame.image.load("spinesmark.png").convert_alpha()
        self.stoneMark=pygame.image.load("stone2mark.png").convert_alpha()
        self.potMark=pygame.image.load("potmark.png").convert_alpha()
        self.boardLst=[[None]*25 for i in range (12)]
        (self.edgeX,self.edgeY)=(76,84)
        self.blockUnit=40
        
    def IssacandBoard(self):
        self.IssacCollideBoard=False
        (IssacX,IssacY)=self.bgIssacRect
        (IssacX,IssacY)=(IssacX-self.IssacWidth/2,IssacY-self.IssacHeight/2)
        self.obstacleLst=[]
        for row in range (12):
            for col in range (25):
                if self.boardLst[row][col]!=2 and self.boardLst[row][col]!=0 and self.boardLst[row][col]!=None:
                    self.obstacleLst.append((row,col))
        for position in self.obstacleLst:
            (row,col)=position
            (xCor,yCor)=(col*self.blockUnit*2+self.edgeX*2,row*self.blockUnit*2+self.edgeY*2)
            if self.keys[pygame.K_a]==1:
                if xCor<IssacX<=xCor+self.blockUnit*2 and yCor+self.blockUnit*2+20>IssacY+self.IssacHeight>yCor:
                    self.IssacCollideBoard=True
                    IssacX=xCor+self.blockUnit*2
            if self.keys[pygame.K_d]==1:
                if (xCor<=IssacX+self.IssacWidth<xCor+self.blockUnit*2 and yCor+self.blockUnit*2+20>IssacY+self.IssacHeight>yCor):
                    self.IssacCollideBoard=True
                    IssacX=xCor-self.IssacWidth
            if self.keys[pygame.K_w]==1:
                if yCor<IssacY+self.IssacHeight<=yCor+self.blockUnit*2+20 and xCor+self.blockUnit*2+self.IssacWidth>IssacX+self.IssacWidth>xCor:
                    self.IssacCollideBoard=True
                    IssacY=yCor+self.blockUnit*2+20-self.IssacHeight
            if self.keys[pygame.K_s]==1:
                if (yCor<=IssacY+self.IssacHeight<=yCor+self.blockUnit*2 and xCor+self.blockUnit*2+self.IssacWidth>IssacX+self.IssacWidth>xCor):
                    self.IssacCollideBoard=True
                    IssacY=yCor-self.IssacHeight
        (IssacX,IssacY)=(IssacX+self.IssacWidth/2,IssacY+self.IssacHeight/2)
        self.bgIssacRect=(IssacX,IssacY)
        
    def keyPressed(self):
        (mouseX,mouseY)=pygame.mouse.get_pos()
        if self.edgeX<=mouseX<=1502-self.edgeX and self.edgeY<=mouseY<=648-self.edgeY:
            self.currentBlock=[(mouseY-self.edgeY)//self.blockUnit,
                    (mouseX-self.edgeX)//self.blockUnit]
        else:
            self.currentBlock=None
        if self.currentBlock!=None:
            if self.keys[pygame.K_SPACE]==1:
                if self.boardLst[self.currentBlock[0]][self.currentBlock[1]]==None:
                    self.boardLst[self.currentBlock[0]][self.currentBlock[1]]=random.randint(1,4)
                else:
                    self.boardLst[self.currentBlock[0]][self.currentBlock[1]]=(self.boardLst[self.currentBlock[0]][self.currentBlock[1]]+1)%5
               
    def IssacandSpines(self):
        (IssacX,IssacY)=self.bgIssacRect
        (IssacX,IssacY)=(IssacX-self.IssacWidth/2,IssacY-self.IssacHeight/2)
        self.spineLst=[]
        for row in range (12):
            for col in range (25):
                if self.boardLst[row][col]==2:
                    self.spineLst.append((row,col))
        for position in self.spineLst:
            (row,col)=position
            (xCor,yCor)=(col*self.blockUnit*2+self.edgeX*2,row*self.blockUnit*2+self.edgeY*2)
            if (xCor-self.IssacWidth<=IssacX<=xCor+80 and
                yCor-self.IssacHeight<=IssacY<=yCor+80):
                if yCor+80+20<=IssacY+self.IssacHeight<=yCor+80+self.IssacHeight:
                    pass
                else:
                    self.IssacHurt=True
                    if self.blood[-1]=="halfblack":
                        Item.BlackHeartEffect(self)
                    if len(self.blood)>0:
                        if "half" in self.blood[-1]:
                            self.blood.pop(-1)
                        else:
                            self.blood[-1]="half"+self.blood[-1]
        
        
            
               
    def gameBg(self,screen):
        (bgX,bgY)=self.bgRect
        for row in range (12):
            for col in range (25):
                cors=(col*self.blockUnit*2+self.edgeX*2+bgX,row*self.blockUnit*2+self.edgeY*2+bgY)
                if self.boardLst[row][col]==1:
                    image=self.mushroom
                elif self.boardLst[row][col]==2:
                    image=self.spines
                elif self.boardLst[row][col]==3:
                    image=self.stone
                elif self.boardLst[row][col]==4:
                    image=self.pot
                elif self.boardLst[row][col]==0 or self.boardLst[row][col]==None:
                    image=None
                if image!=None:
                    screen.blit(image,cors)
        
    # def IssacHitEffect(self,screen):
    #     (x,y)=self.IssacRect
    #     s=pygame.Surface((self.IssacWidth,self.IssacHeight))
    #     s.set_alpha(50)
    #     s.fill((255,0,0))
    #     screen.blit(s,(x,y))
        
    def IssacHitEffect(self,screen):
        (x,y)=self.IssacRect
        HitImage=self.image.copy()
        HitImage.fill((255, 0, 0, 100), None, pygame.BLEND_RGBA_MULT)
        screen.blit(HitImage,(x,y))
        
    def MonsterHitEffect(self,screen):
        (bgX,bgY)=(self.bgRect)
        for monster in self.monsterHitLst:
            (x,y)=(monster[0],monster[1])
            image=monster[2]
            image=image.copy()
            image.fill((255,0,0,150),None, pygame.BLEND_RGBA_MULT)
            screen.blit(image,(x+bgX,y+bgY))
        
    def redrawAll(self,screen):
        screen.fill((255, 255, 255))
        screen.blit(self.makeBoardbg,(0,0))
        if self.currentBlock!=None:
            rect=(self.currentBlock[1]*self.blockUnit+self.edgeX,
                    self.currentBlock[0]*self.blockUnit+self.edgeY)
                    #self.blockUnit,
                    #self.blockUnit)
            s=pygame.Surface((self.blockUnit,self.blockUnit))
            s.set_alpha(90)
            s.fill((255,255,255))
            screen.blit(s,rect)
            #pygame.draw.rect(screen,"None",rect,5)
        for row in range (12):
            for col in range (25):
                cors=(col*self.blockUnit+self.edgeX,row*self.blockUnit+self.edgeY)
                if self.boardLst[row][col]==1:
                    image=self.mushroomMark
                elif self.boardLst[row][col]==2:
                    image=self.spinesMark
                elif self.boardLst[row][col]==3:
                    image=self.stoneMark
                elif self.boardLst[row][col]==4:
                    image=self.potMark
                elif self.boardLst[row][col]==0 or self.boardLst[row][col]==None:
                    image=None
                if image!=None:
                    screen.blit(image,cors)