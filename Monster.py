#framework cited from CMU 15112 website
#http://www.cs.cmu.edu/~112/notes/notes-oop.html
from pygamegame import PygameGame
import pygame
from Items import *
from Issac import *
from MakeBoard import *
import random
class Monster(pygame.sprite.Sprite):
    def init(self):
        self.IssacHurt=False
        self.edge=140
        self.monsterLst=[]
        Issac.init(self)
        self.monsterHitLst=[]
        self.fly=pygame.image.load("monsterfly.png").convert_alpha()
        self.fly2left=pygame.image.load("bigflyleft.png").convert_alpha()
        self.fly2right=pygame.image.load("bigflyright.png").convert_alpha()
        self.fly3left=pygame.image.load("hugeflyleft.png").convert_alpha()
        self.fly3right=pygame.image.load("hugeflyright.png").convert_alpha()
        self.bigMonster=pygame.image.load("monsternormal.png").convert_alpha()
        self.bigMonsterFiring=pygame.image.load("monsterfiring.png").convert_alpha()
        self.evilIssac=pygame.image.load("monsterIssac.png").convert_alpha()
        self.spider=pygame.image.load("spider.png").convert_alpha()
        self.dodgingMonsterLeft=pygame.image.load("dodgingmonster2.png").convert_alpha()
        self.dodgingMonsterRight=pygame.image.load("dodgingmonster.png").convert_alpha()
        self.monsterBullet=pygame.image.load("monsterbullet.png").convert_alpha()
        self.ghost=pygame.image.load("ghost.png").convert_alpha()
        self.lordofflies=pygame.image.load("lordofflies.png").convert_alpha()
        self.lordoffliesShooting=pygame.image.load("lordoffliesshoot.png").convert_alpha()
        self.firingMonster=pygame.image.load("monsternormal.png").convert_alpha()
        self.firingMonsterFiring=pygame.image.load("monsterfiring.png").convert_alpha()
        self.monsterBulletSize=28
        self.timeCount=0
        self.monsterBulletSpeed=10
        self.monsterBulletRange=200
        self.normalFlyLst=[]
        self.bigFlyLst=[]
        self.hugeFlyLst=[]
        self.bigFlyBulletLst=[]
        self.hugeFlyBulletLst=[]
        self.evilIssacLst=[]
        self.spiderLst=[]
        self.dodgingMonsterLst=[]
        self.ghostLst=[]
        self.lordoffliesLst=[]
        self.firingMonsterLst=[]
        self.bigFlyHeight=61
        self.bigFlyWidth=40
        (self.hugeFlyWidth,self.hugeFlyHeight)=(57,51)
        (self.bigFlyWidth,self.bigFlyHeight)=(40,61)
        (self.normalFlyWidth,self.normalFlyHeight)=(57,30)
        (self.spiderWidth,self.spiderHeight)=(57,30)
        (self.evilIssacWidth,self.evilIssacHeight)=(85,76)
        (self.ghostWidth,self.ghostHeight)=(68,59)
        (self.dodgingMonsterWidth,self.dodgingMonsterHeight)=(113,99)
        (self.lordoffliesWidth,self.lordoffliesHeight)=(170,183)
        (self.lordLeft,self.lordUp)=(True,True)
        (self.firing,self.firingTime)=(False,0)
        self.fireRight=True
        (self.firingMonsterWidth,self.firingMonsterHeight)=(255,207)
        self.firingMonsterFiringHeight=1134
        
    def addMonster(self,blood,image1,image2,listname):
        name=__class__.__name__
        x=random.randint(self.edge,2304-self.edge-100)
        y=random.randint(self.edge,1296-self.edge-100)
        cor=(x,y)
        (IssacX,IssacY)=self.bgIssacRect
        if image2==None:
            listname.append((cor,name,blood,image1))
        else:
            if x<IssacX:
                image=image1
            else:
                image=image2
            listname.append((cor,name,blood,image))
        
    def moveMonster(self,speed,monsterlist):
        newLst=[]
        for monster in monsterlist:
            (IssacX,IssacY)=self.bgIssacRect
            (monsterX,monsterY)=monster[0]
            direction=random.randint(0,1)
            if direction==0:
                if IssacX<monsterX:
                    monsterX-=speed
                    if monsterX<self.edge:
                        monsterX=self.edge
                else:
                    monsterX+=speed
                    if monsterX>2304-self.edge:
                        monsterX=2304-self.edge
            elif direction==1:
                if IssacY<monsterY:
                    monsterY-=speed
                    if monsterY<self.edge:
                        monsterY=self.edge
                else:
                    monsterY+=speed
                    if monsterY>1296-self.edge:
                        monsterY=1296-self.edge
            newLst.append(((monsterX,monsterY),monster[1],monster[2],monster[3]))
        monsterlist=newLst
        
    def timerFired(self, dt):
        pass
        
        #monster collides with Issac, Issac loses blood, monster loses blood
    def monsterCollide(self,monsterlist,monsterWidth,monsterHeight):
        (IssacX,IssacY)=self.bgIssacRect
        newLst=[]
        for monster in monsterlist:
            monsterBlood=monster[2]
            (monsterX,monsterY)=monster[0]
            if (IssacX-self.IssacWidth/2-monsterWidth<=monsterX<=IssacX+self.IssacWidth/2 and 
                    IssacY-self.IssacHeight/2-monsterHeight<=monsterY<=IssacY+self.IssacHeight/2):
                monsterBlood-=self.IssacDamage
                self.IssacHurt=True
                if len(self.blood)>0 and self.blood[-1]=="halfblack":
                    Items.BlackHeartEffect(self)
                if len(self.blood)>0:
                    if "half" in self.blood[-1]:
                        self.blood.pop(-1)
                    else:
                        self.blood[-1]="half"+self.blood[-1]
                if monsterBlood>0:
                    newLst.append(((monsterX,monsterY),monster[1],monsterBlood,monster[3]))
            else:
                newLst.append(monster)
        return newLst
    
    #detect if the bullets shoot by Issac gets any monster
    #if yes, bullet gone, monster loses blood
    #monster gone if blood level smaller than 0    
    def IssacBulletCollide(self,bulletX,bulletY,monsterlist,monsterWidth,monsterHeight):
        hit=False
        newMonsterLst=[]
        for monster in monsterlist:
            (monsterX,monsterY)=monster[0]
            monsterBlood=monster[2]
            if ((bulletX-monsterWidth<=monsterX<=bulletX+self.bulletSize and
                bulletY-monsterHeight<=monsterY<=bulletY+self.bulletSize) and hit==False):
                hit=True
                monsterBlood-=self.IssacDamage
                if monsterBlood>0:
                    self.monsterHitLst.append((monsterX,monsterY,monster[3],2))
                    newMonsterLst.append(((monsterX,monsterY),monster[1],monsterBlood,monster[3]))
            else:
                newMonsterLst.append(monster)
        return (newMonsterLst,hit)
        
    def redrawAll(self, screen,bulletLst,monsterLst):
        (bgX,bgY)=self.bgRect
        if bulletLst!=None and bulletLst!=[]:
            for bullet in bulletLst:
                cor=(bullet[0]+bgX,bullet[1]+bgY)
                screen.blit(self.monsterBullet,cor)
        if monsterLst!=0:
            for monster in monsterLst:
                image=monster[3]
                (x,y)=monster[0]
                x+=bgX
                y+=bgY
                screen.blit(image,(x,y))

class NormalFly(Monster):
    def moveMonster(self,speed=6):
        newLst=[]
        for monster in self.normalFlyLst:
            x=random.randint(0,speed)
            y=(speed**2-x**2)**0.5
            (IssacX,IssacY)=self.bgIssacRect
            (monsterX,monsterY)=monster[0]
            if monsterX<IssacX: monsterX+=x
            else: monsterX-=x
            if monsterY<IssacY: monsterY+=y
            else: monsterY-=y
            newLst.append(((monsterX,monsterY),monster[1],monster[2],monster[3]))
        self.normalFlyLst=newLst
        
class BigFly(Monster):
    def moveMonster(self,speed=2):
        newLst=[]
        for monster in self.bigFlyLst:
            directionLst=["left","right","up","down"]
            directionIndex=random.randint(0,3)
            direction=directionLst[directionIndex]
            (monsterX,monsterY)=monster[0]
            (IssacX,IssacY)=self.bgIssacRect
            if direction=="up":
                monsterY-=speed
                if monsterY<self.edge:
                    monsterY=self.edge
            elif direction=="down":
                monsterY+=speed
                if monsterY>1296-self.edge:
                    monsterY=1296-self.edge
            elif direction=="left":
                monsterX-=speed
                if monsterX<self.edge:
                    monsterX=self.edge
            elif direction=="right":
                monsterX+=speed
                if monsterX>2304-self.edge:
                    monsterX=2304-self.edge
            if monsterX<IssacX:
                image=self.fly2right
            else:
                image=self.fly2left
            newLst.append(((monsterX,monsterY),monster[1],monster[2],image))
        self.bigFlyLst=newLst
        
    def addMonster(self):
        x=random.randint(self.edge,2304-self.edge)
        y=random.randint(self.edge,1296-self.edge)
        (IssacX,IssacY)=self.bgIssacRect
        if x<IssacX: image=self.fly2right
        else: image=self.fly2left
        self.bigFlyLst.append(((x,y),"bigfly",10,image))
    #calls shoot bullet when the fly dies     change to s single monster input
    def shootBullet(self,monster):
        (monsterX,monsterY)=monster[0]
        self.bigFlyBulletLst.append(("left",monsterX-self.monsterBulletSize,
                                monsterY+self.bigFlyHeight/2-self.monsterBulletSize/2,self.monsterBulletRange))
        self.bigFlyBulletLst.append(("up",monsterX+self.bigFlyWidth/2-self.monsterBulletSize/2,
                                monsterY-self.monsterBulletSize,self.monsterBulletRange))
        self.bigFlyBulletLst.append(("right",monsterX+self.bigFlyWidth,
                                monsterY+self.bigFlyHeight/2-self.monsterBulletSize/2,self.monsterBulletRange))
        self.bigFlyBulletLst.append(("down",monsterX+self.bigFlyWidth/2-self.monsterBulletSize/2,
                                monsterY+self.bigFlyHeight,self.monsterBulletRange))
     #######I changed the format of bullet list, change the timerfired accordingly!                           
    def moveBullet(self):
        newLst=[]
        for bullets in self.bigFlyBulletLst:
            (x,y)=(bullets[1],bullets[2])
            range=bullets[3]
            direction=bullets[0]
            # (left,up,right,down,range)=bullets
            # (leftX,leftY)=left
            # (upX,upY)=up
            # (rightX,rightY)=right
            # (downX,downY)=down
            range-=self.monsterBulletSpeed
            if range>=0:
                if direction=="left":
                    x-=self.monsterBulletSpeed
                    if x<self.edge:
                        x=self.edge
                    newLst.append((direction,x,y,range))
                elif direction=="up":
                    y-=self.monsterBulletSpeed
                    if y<self.edge:
                        y=self.edge
                    newLst.append((direction,x,y,range))
                elif direction=="right":
                    x+=self.monsterBulletSpeed
                    if x>2304-self.edge-self.monsterBulletSize:
                        x=2304-self.edge-self.monsterBulletSize
                    newLst.append((direction,x,y,range))
                elif direction=="down":
                    y+=self.monsterBulletSpeed
                    if y>1296-self.edge-self.monsterBulletSize:
                        y=1296-self.edge-self.monsterBulletSize
                    newLst.append((direction,x,y,range))
        self.bigFlyBulletLst=newLst
        
    def bulletCollide(self):
        (IssacX,IssacY)=self.bgIssacRect
        newLst=[]
        for bullet in self.bigFlyBulletLst:
            (bulletX,bulletY)=(bullet[1],bullet[2])
            if (IssacX-self.IssacWidth/2-self.bigFlyWidth<=bulletX<=IssacX+self.IssacWidth/2 and 
                    IssacY-self.IssacHeight/2-self.bigFlyHeight<=bulletY<=IssacY+self.IssacHeight/2):
                self.IssacHurt=True
                if len(self.blood)>0 and self.blood[-1]=="halfblack":
                    Items.BlackHeartEffect(self)
                if "half" in self.blood[-1]:
                    self.blood.pop(-1)
                else:
                    self.blood[-1]="half"+self.blood[-1]
            else:
                newLst.append(bullet)
        self.bigFlyBulletLst=newLst
                
    def redrawAll(self,screen):
        (bgX,bgY)=self.bgRect
        if self.bigFlyBulletLst!=[]:
            for bullets in self.bigFlyBulletLst:
                (bulletX,bulletY)=(bullets[1],bullets[2])
                bulletX+=bgX
                bulletY+=bgY
                screen.blit(self.monsterBullet,(bulletX,bulletY))
        if self.bigFlyLst!=0:
            for monster in self.bigFlyLst:
                image=monster[3]
                (x,y)=monster[0]
                x+=bgX
                y+=bgY
                screen.blit(image,(x,y))
            
        
class HugeFly(Monster):
    def moveMonster(self):
        (IssacX,IssacY)=self.bgIssacRect
        newLst=[]
        for monster in self.hugeFlyLst:
            (monsterX,monsterY)=monster[0]
            if monsterX<IssacX:
                image=self.fly3right
            else:
                image=self.fly3left
            monster=(monster[0],monster[1],monster[2],image)
            newLst.append(monster)
        self.hugeFlyLst=newLst
       
#######huge fly doesn't shoot bullet!!!!
    def shootBullet(self):
        for monster in self.hugeFlyLst:
            if self.timeCount%5==0:
                (monsterX,monsterY)=monster[0]
                (IssacX,IssacY)=self.bgIssacRect
                if monsterX<IssacX:
                    self.hugeFlyBulletLst.append((monsterX+self.hugeFlyWidth,monsterY+self.hugeFlyHeight/2-self.monsterBulletSize,self.monsterBulletRange,"rightup"))
                    self.hugeFlyBulletLst.append((monsterX+self.hugeFlyWidth,monsterY+self.hugeFlyHeight/2,self.monsterBulletRange,"rightdown"))
                else:
                    self.hugeFlyBulletLst.append((monsterX,monsterY+self.hugeFlyHeight/2-self.monsterBulletSize,self.monsterBulletRange,"leftup"))
                    self.hugeFlyBulletLst.append((monsterX,monsterY+self.hugeFlyHeight/2,self.monsterBulletRange,"leftdown"))
            
    def moveBullet(self):
        newLst=[]
        for bullet in self.hugeFlyBulletLst:
            (speedX,speedY)=(6,3)
            (x,y,range,direction)=bullet
            if direction=="rightup":
                x+=speedX
                y-=speedY
                range-=speedX
                if range>=0 and x<=2304-self.edge and y>=self.edge:
                    newLst.append((x,y,range,direction))
            elif direction=="rightdown":
                x+=speedX
                y+=speedY
                range-=speedX
                if range>=0 and x<=2304-self.edge and y<=1296-self.edge:
                    newLst.append((x,y,range,direction))
            elif direction=="leftup":
                x-=speedX
                y-=speedY
                range-=speedX
                if range>=0 and x>=self.edge and y>=self.edge:
                    newLst.append((x,y,range,direction))
            elif direction=="leftdown":
                x-=speedX
                y+=speedY
                range-=speedX
                if range>=0 and x>=self.edge and y<=1296-self.edge:
                    newLst.append((x,y,range,direction))
        self.hugeFlyBulletLst=newLst
        
    def bulletCollide(self):
        (IssacX,IssacY)=self.bgIssacRect
        newLst=[]
        for bullet in self.hugeFlyBulletLst:
            (bulletX,bulletY)=(bullet[0],bullet[1])
            if (IssacX-self.IssacWidth/2-self.hugeFlyWidth<=bulletX<=IssacX+self.IssacWidth/2 and 
                    IssacY-self.IssacHeight/2-self.hugeFlyHeight<=bulletY<=IssacY+self.IssacHeight/2):
                self.IssacHurt=True
                if len(self.blood)>0 and self.blood[-1]=="halfblack":
                    Items.BlackHeartEffect(self)
                if "half" in self.blood[-1]:
                    self.blood.pop(-1)
                else:
                    self.blood[-1]="half"+self.blood[-1]
            else:
                newLst.append(bullet)
        self.hugeFlyBulletLst=newLst
        
    # def addMonster(self):
    #     x=random.randint(self.edge,2304-self.edge)
    #     y=random.randint(self.edge,1296-self.edge)
    #     (IssacX,IssacY)=self.bgIssacRect
    #     if x<IssacX: image=self.fly3left
    #     else: image=self.fly3right
    #     self.monsterLst.append(((x,y),"hugefly",10,image))
    
        
class Spider(Monster):
    def moveMonster(self,speed):
        newLst=[]
        for monster in self.spiderLst:
            (IssacX,IssacY)=self.bgIssacRect
            (monsterX,monsterY)=monster[0]
            direction=random.randint(0,1)
            if direction==0:
                if IssacX<monsterX:
                    monsterX-=speed
                    if monsterX<self.edge:
                        monsterX=self.edge
                else:
                    monsterX+=speed
                    if monsterX>2304-self.edge:
                        monsterX=2304-self.edge
            elif direction==1:
                if IssacY<monsterY:
                    monsterY-=speed
                    if monsterY<self.edge:
                        monsterY=self.edge
                else:
                    monsterY+=speed
                    if monsterY>1296-self.edge:
                        monsterY=1296-self.edge
            newLst.append(((monsterX,monsterY),monster[1],monster[2],monster[3]))
        self.spiderLst=newLst
    # def moveMonster(self,speed=10):
    #     newLst=[]
    #     for monster in self.spiderLst:
    #         directionLst=["left","right","up","down"]
    #         directionIndex=random.randint(0,3)
    #         direction=directionLst[directionIndex]
    #         (monsterX,monsterY)=monster[0]
    #         (IssacX,IssacY)=self.bgIssacRect
    #         if direction=="up":
    #             monsterY-=speed
    #             if monsterY<self.edge:
    #                 monsterY=self.edge
    #         elif direction=="down":
    #             monsterY+=speed
    #             if monsterY>1296-self.edge:
    #                 monsterY=1296-self.edge
    #         elif direction=="left":
    #             monsterX-=speed
    #             if monsterX<self.edge:
    #                 monsterX=self.edge
    #         elif direction=="right":
    #             monsterX+=speed
    #             if monsterX>2304-self.edge:
    #                 monsterX=2304-self.edge
    #         newLst.append(((monsterX,monsterY),monster[1],monster[2],self.spider))
    # self.spiderLst=newLst
    
class EvilIssac(Monster):
    # def moveMonster(self,speed=3):
    #     newLst=[]
    #     for monster in self.evilIssacLst:
    #         (monsterX,monsterY)=monster[0]
    #         if self.timeCount%2==0:
    #             monsterX+=speed
    #         elif self.timeCount%2==1:
    #             monsterX-=speed
    #         newLst.append(((monsterX,monsterY),monster[1],monster[2],monster[3]))
    #     self.evilIssacLst=newLst
    def moveMonster(self,speed=2):
        newLst=[]
        for monster in self.evilIssacLst:
            directionLst=["left","right"]
            directionIndex=random.randint(0,1)
            direction=directionLst[directionIndex]
            (monsterX,monsterY)=monster[0]
            (IssacX,IssacY)=self.bgIssacRect
            if direction=="left":
                monsterX-=speed
                if monsterX<self.edge:
                    monsterX=self.edge
            elif direction=="right":
                monsterX+=speed
                if monsterX>2304-self.edge:
                    monsterX=2304-self.edge
            newLst.append(((monsterX,monsterY),monster[1],monster[2],self.evilIssac))
        self.evilIssacLst=newLst
        
    def timerFired(self,dt):
        self.timeCount+=1
        
class Ghost(Monster):
    def moveMonster(self,speed=10):
        newLst=[]
        for monster in self.ghostLst:
            x=random.randint(0,speed)
            y=(speed**2-x**2)**0.5
            (IssacX,IssacY)=self.bgIssacRect
            (monsterX,monsterY)=monster[0]
            if monsterX<IssacX: monsterX+=x
            else: monsterX-=x
            if monsterY<IssacY: monsterY+=y
            else: monsterY-=y
            newLst.append(((monsterX,monsterY),monster[1],monster[2],monster[3]))
        self.ghostLst=newLst
    
class DodgingMonster(Monster):
    def moveMonster(self,speed=3):
        newLst=[]
        for monster in self.dodgingMonsterLst:
            (monsterX,monsterY)=monster[0]
            (IssacX,IssacY)=self.bgIssacRect
            direction=random.randint(0,1)
            #0--move horizontally
            if (abs(monsterX-IssacX<self.monsterBulletRange) or
                abs(monsterY-IssacX<self.monsterBulletRange)):
                if direction==0:
                    if monsterX<IssacX:
                        monsterX-=speed
                        if monsterX<=self.edge:
                            monsterX=self.edge
                    else:
                        monsterX+=speed
                        if monsterX>=2304-self.edge-self.dodgingMonsterWidth:
                            monsterX=2304-self.edge-self.dodgingMonsterWidth
                elif direction==1:
                    if monsterY<IssacY:
                        monsterY-=speed
                        if monsterY<=self.edge:
                            monsterY=self.edge
                    else:
                        monsterY+=speed
                        if monsterY>=1296-self.edge-self.dodgingMonsterHeight:
                            monsterY=1296-self.edge-self.dodgingMonsterHeight
            if monsterX<IssacX:
                image=self.dodgingMonsterLeft
            else:
                image=self.dodgingMonsterRight
            newLst.append(((monsterX,monsterY),monster[1],monster[2],image))
        self.dodgingMonsterLst=newLst

class LordofFlies(Monster):
    def moveMonster(self,image,speed=5):
        newLst=[]
        for monster in self.lordoffliesLst:
            (monsterX,monsterY)=monster[0]
            if self.lordLeft==True:
                monsterX-=speed
                if monsterX<=self.edge:
                    monsterX=self.edge
                    self.lordLeft=False
            else:
                monsterX+=speed
                if monsterX>=2304-self.edge-self.lordoffliesWidth:
                    monsterX=2304-self.edge-self.lordoffliesWidth
                    self.lordLeft=True
            if self.lordUp==True:
                monsterY-=speed
                if monsterY<=self.edge:
                    monsterY=self.edge
                    self.lordUp=False
            else:
                monsterY+=speed
                if monsterY>=1296-self.edge-self.lordoffliesHeight:
                    monsterY=1296-self.edge-self.lordoffliesHeight
                    self.lordUp=True
            newLst.append(((monsterX,monsterY),monster[1],monster[2],image))
        self.lordoffliesLst=newLst
        
    def shootFlies(self):
        (IssacX,IssacY)=self.bgIssacRect
        for monster in self.lordoffliesLst:
            (monsterX,monsterY)=monster[0]
            (left,right,up,down)=(monsterX-50,monsterX+self.lordoffliesWidth+50,monsterY-50,monsterY+self.lordoffliesHeight+50)
            num=random.randint(1,3)
            for i in range (num):
                locationChoice=random.randint(0,3)
                if locationChoice==0:
                    (x,y)=(random.randint(left,monsterX),random.randint(up,down))
                elif locationChoice==1:
                    (x,y)=(random.randint(right-50,right),random.randint(up,down))
                elif locationChoice==2:
                    (x,y)=(random.randint(up,monsterY),random.randint(left,right))
                elif locationChoice==3:
                    (x,y)=(random.randint(down-50,down),random.randint(left,right))
                flyChoice=random.randint(0,1)
                if flyChoice==0:
                    self.normalFlyLst.append(((x,y),"normalfly",10,self.fly))
                    #add normal fly
                elif flyChoice==1:
                    if x<IssacX:
                        image=self.fly2right
                    else:
                        image=self.fly2left
                    self.bigFlyLst.append(((x,y),"bigfly",10,image))
                    #add big fly
        
class FiringMonster(Monster):
    def addMonster(self):
        x=random.randint(self.edge,2304-200)
        y=100
        self.firingMonsterLst.append(((x,y),"firingmonster",150,self.firingMonster))
        
    def moveMonster(self,image,speed=5):
        newLst=[]
        for monster in self.firingMonsterLst:
            (monsterX,monsterY)=monster[0]
            if self.fireRight==True:
                monsterX+=speed
                if monsterX>=2304-self.edge-self.firingMonsterHeight:
                    monsterX=2304-self.edge-self.firingMonsterHeight
                    self.fireRight=False
            else:
                monsterX-=speed
                if monsterX<=self.edge:
                    monsterX=self.edge
                    self.fireRight=True
            newLst.append(((monsterX,monsterY),monster[1],monster[2],image))
        self.firingMonsterLst=newLst
                    
            