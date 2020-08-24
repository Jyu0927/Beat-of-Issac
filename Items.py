#framework cited from CMU 15112 website
#http://www.cs.cmu.edu/~112/notes/notes-oop.html
from pygamegame import PygameGame
import pygame
from Issac import *
import random
class Items(pygame.sprite.Sprite):
    def init(self):
        Issac.init(self)
        self.coinLst=[]
        self.heartLst=[]
        self.coin=pygame.image.load("itemcoin.png").convert_alpha()
        self.itemRedheart=pygame.image.load("itemredheart.png").convert_alpha()
        self.itemBlueheart=pygame.image.load("itemblueheart.png").convert_alpha()
        self.itemBlackheart=pygame.image.load("itemblackheart.png").convert_alpha()
        (self.coinWidth,self.coinHeight)=(51,33)
        (self.heartWidth,self.heartHeight)=(40,32)
        self.damageup1=pygame.image.load("damageup1.png").convert_alpha()
        self.damageup2=pygame.image.load("damageup2.png").convert_alpha()
        self.speedup1=pygame.image.load("speedup.png").convert_alpha()
        self.speedup2=pygame.image.load("speedup2.png").convert_alpha()
        self.randomneedle=pygame.image.load("needle.png").convert_alpha()
        self.storeLst=[self.damageup1,self.damageup2,self.speedup1,self.speedup2,self.randomneedle]
        random.shuffle(self.storeLst)
        
    def placeItem(self,image,itemlist):
        x=random.randint(self.edge,2304-self.edge)
        y=random.randint(self.edge,1296-self.edge)
        cor=(x,y)
        (IssacX,IssacY)=self.bgIssacRect
        itemlist.append((cor,image))
        
    def redrawAll(self,screen,itemlist):
        (bgX,bgY)=self.bgRect
        for item in itemlist:
            (x,y)=item[0]
            image=item[1]
            x+=bgX
            y+=bgY
            screen.blit(image,(x,y))

# class Coin(pygame.sprite.Sprite):
#     def init(self,x=random.randint(self.edge,2304-self.edge),y=random.randint(self.edge,1296-self.edge)):
#         self.coin=pygame.image.load("itemcoin.png").convert_alpha()
#         coinGroup=pygame.sprite.Group()
#         (self.x,self.y)=(x,y)

    def BlackHeartEffect(self):
        newLst=[]
        for monster in self.normalFlyLst:
            blood=monster[2]-10
            if blood>0:
                newLst.append((monster[0],monster[1],blood,monster[3]))
        self.normalFlyLst=newLst
        newLst1=[]
        for monster in self.bigFlyLst:
            blood=monster[2]-10
            if blood>0:
                newLst1.append((monster[0],monster[1],blood,monster[3]))
        self.bigFlyLst=newLst1
        newLst2=[]
        for monster in self.hugeFlyLst:
            blood=monster[2]-10
            if blood>0:
                newLst2.append((monster[0],monster[1],blood,monster[3]))
        self.hugeFlyLst=newLst2
        newLst3=[]
        for monster in self.evilIssacLst:
            blood=monster[2]-10
            if blood>0:
                newLst3.append((monster[0],monster[1],blood,monster[3]))
        self.evilIssacLst=newLst3
        newLst4=[]
        for monster in self.spiderLst:
            blood=monster[2]-10
            if blood>0:
                newLst4.append((monster[0],monster[1],blood,monster[3]))
        self.spiderLst=newLst4
        newLst5=[]
        for monster in self.dodgingMonsterLst:
            blood=monster[2]-10
            if blood>0:
                newLst5.append((monster[0],monster[1],blood,monster[3]))
        self.dodgingMonsterLst=newLst5
        newLst6=[]
        for monster in self.ghostLst:
            blood=monster[2]-10
            if blood>0:
                newLst6.append((monster[0],monster[1],blood,monster[3]))
        self.ghostLst=newLst6
        newLst7=[]
        for monster in self.lordoffliesLst:
            blood=monster[2]-10
            if blood>0:
                newLst7.append((monster[0],monster[1],blood,monster[3]))
        self.lordoffliesLst=newLst7
        newLst8=[]
        for monster in self.firingMonsterLst:
            blood=monster[2]-10
            if blood>0:
                newLst8.append((monster[0],monster[1],blood,monster[3]))
        self.firingMonsterLst=newLst8
        
        
        
        
        
        
        
        # self.evilIssacLst=[]
        # self.spiderLst=[]
        # self.dodgingMonsterLst=[]
        # self.ghostLst=[]
        # self.lordoffliesLst=[]
        # self.firingMonsterLst=[]        
        
class Coin(Items):
    def collide(self):
        newLst=[]
        (IssacX,IssacY)=self.bgIssacRect
        for coin in self.coinLst:
            (coinX,coinY)=coin[0]
            if (IssacX-self.IssacWidth/2-self.coinWidth<=coinX<=IssacX+self.IssacWidth/2 and 
                IssacY-self.IssacHeight/2-self.coinHeight<=coinY<=IssacY+self.IssacHeight/2):
                self.money+=1
            else:
                newLst.append(coin)
        self.coinLst=newLst
        
    def addMoney(self):
        self.money+=1
        
    
    
class Heart(Items):
    def collide(self):
        newLst=[]
        (IssacX,IssacY)=self.bgIssacRect
        for heart in self.heartLst:
            (heartX,heartY)=heart[0]
            image=heart[1]
            if (IssacX-self.IssacWidth/2-self.heartWidth<=heartX<=IssacX+self.IssacWidth/2 and 
                IssacY-self.IssacHeight/2-self.heartHeight<=heartY<=IssacY+self.IssacHeight/2):
                if image==self.itemRedheart:
                    if len(self.blood)>=3:
                        if "red" not in self.blood[2]:
                            self.blood.insert(0,"red")
                        elif self.blood[2]=="halfred":
                            self.blood[2]="red"
                        else:
                            newHeart=heartPush(self,heartX,heartY,image)
                            newLst.append(newHeart)
                    else:
                        self.blood.insert(0,"red")
                        if len(self.blood)>3:
                            self.blood.pop()

                elif image==self.itemBlueheart:
                    if "half" not in self.blood[-1] or "red" in self.blood[-1]:
                        if len(self.blood)==12:
                            newHeart=heartPush(self,heartX,heartY,image)
                            newLst.append(newHeart)
                        else:
                            self.blood.append("blue")
                    else:
                        self.blood[-1]=self.blood[-1][4:]
                        self.blood.append("halfblue")
                        if len(self.blood)>12:
                            self.blood.pop(-1)
                elif image==self.itemBlackheart:
                    if "half" not in self.blood[-1] or "red" in self.blood[-1]:
                        if len(self.blood)==12:
                            newHeart=heartPush(self,heartX,heartY,image)
                            newLst.append(newHeart)
                        else:
                            self.blood.append("black")
                    else:
                        self.blood[-1]=self.blood[-1][4:]
                        self.blood.append("halfblack")
                        if len(self.blood)>12:
                            self.blood.pop(-1)
            else:
                newLst.append(heart)
        self.heartLst=newLst
        
def heartPush(self,heartX,heartY,image):
    (IssacX,IssacY)=self.bgIssacRect
    if self.keys[pygame.K_w]==1 and IssacY-self.IssacHeight/2-self.heartHeight<=heartY<=IssacY-self.IssacHeight/2-self.heartHeight+20:
        heartY-=self.speed
        if heartY<self.edge:
            heartY=self.edge
        return (((heartX,heartY),image))
    elif self.keys[pygame.K_s]==1 and IssacY+self.IssacHeight/2-20<=heartY<=IssacY+self.IssacHeight/2:
        heartY+=self.speed
        if heartY>1296-self.edge-self.heartHeight:
            heartY=1296-self.edge-self.heartHeight
        return (((heartX,heartY),image))
    elif self.keys[pygame.K_a]==1 and IssacX-self.IssacWidth/2-self.heartWidth<=heartX<=IssacX-self.IssacWidth/2-self.heartWidth+20:
        heartX-=self.speed
        if heartX<self.edge:
            heartX=self.edge
        return (((heartX,heartY),image))
    elif self.keys[pygame.K_d]==1 and IssacX+self.IssacWidth/2-20<=heartX<=IssacX+self.IssacWidth/2:
        heartX+=self.speed
        if heartX>2304-self.edge-self.heartWidth:
            heartX=2304-self.edge-self.heartWidth
        return (((heartX,heartY),image))
    else:
        return (((heartX,heartY),image))

    # def loseHeart(self):
    #     lastheart=self.blood[-1]
    #     if lastheart=="halfred" or lastheart=="halfblue" or lastheart=="halfblack":
    #         self.blood.pop()
    #     else:
    #         self.blood[-1]="half"+lastheart