#framework cited from CMU 15112 website
#http://www.cs.cmu.edu/~112/notes/notes-oop.html
from pygamegame import PygameGame
import pygame
class Issac(pygame.sprite.Sprite):
    def init(self):
        self.IssacCollideBoard=False
        (self.bgIssacRect)=(1152,648)
        self.bg=pygame.image.load("background.png")
        self.damageValue=pygame.image.load("damagevalue.png")
        self.speedValue=pygame.image.load("speed.png")
        self.coinValue=pygame.image.load("coinvalue.png")
        self.headDownbodyDown=pygame.image.load("Issac1.png").convert_alpha()
        self.headDownbodyLeft=pygame.image.load("Issac2.png").convert_alpha()
        self.headDownbodyRight=pygame.image.load("Issac3.png").convert_alpha()
        self.headLeftbodyLeft=pygame.image.load("Issac4.png").convert_alpha()
        self.headLeftbodyRight=pygame.image.load("Issac5.png").convert_alpha()
        self.headLeftbodyDown=pygame.image.load("Issac6.png").convert_alpha()
        self.headRightbodyDown=pygame.image.load("Issac7.png").convert_alpha()
        self.headRightbodyLeft=pygame.image.load("Issac8.png").convert_alpha()
        self.headRightbodyRight=pygame.image.load("Issac9.png").convert_alpha()
        self.headUpbodyLeft=pygame.image.load("Issac10.png").convert_alpha()
        self.headUpbodyRight=pygame.image.load("Issac11.png").convert_alpha()
        self.headUpbodyDown=pygame.image.load("Issac12.png").convert_alpha()
        self.emptyheart=pygame.image.load("emptyheart.png").convert_alpha()
        self.fullredheart=pygame.image.load("fullheart.png").convert_alpha()
        self.halfredheart=pygame.image.load("halfheart.png").convert_alpha()
        self.blueheart=pygame.image.load("fullblueheart.png").convert_alpha()
        self.halfblueheart=pygame.image.load("halfblueheart.png").convert_alpha()
        self.fullblackheart=pygame.image.load("fullblackheart.png").convert_alpha()
        self.halfblackheart=pygame.image.load("halfblackheart.png").convert_alpha()
        self.image=self.headDownbodyDown
        self.rect=self.image.get_rect()
        self.bullet1=pygame.image.load("bullet1.png").convert_alpha()
        self.bgSize=(2304,1296)
        self.displaySize=(1152,648)
        (self.bgRect)=(-576,-324)
        (self.bgX,self.bgY)=(self.bgRect)
        (self.bgIssacRect)=(1152,648)
        (self.bgIssacX,self.bgIssacY)=(self.bgIssacRect)
        self.IssacWidth=96
        self.IssacHeight=112
        self.IssacDamage=10
        self.speed=15
        self.money=5
        self.direction=None
        pygame.init()
        self.IssacRect=(self.bgX+self.bgIssacX-self.IssacWidth/2,
                    self.bgY+self.bgIssacY-self.IssacHeight/2)
        (self.IssacX,self.IssacY)=(self.IssacRect)
        self.bulletSpeed=15
        self.range=300
        self.radius=10
        (self.IssacWidth,self.IssacHeight)=(96,112)
        (self.width,self.height)=(1152,648)
        self.bulletCors=[]
        self.bulletSize=34
        self.timeCount=0
        self.blood=["red","red","red"]
        self.displayheartWidth=40
        self.IssacDead=False

    def keyPressed(self):
        (x,y)=(self.bgIssacRect)
        (displayX,displayY)=(self.IssacRect)
        (backX,backY)=(self.bgRect)
        if self.keys[pygame.K_a]==1 and self.IssacCollideBoard==False :
            if (backX==0 and 0<=x<=576) or (backX==-1152 and 1728<=x<=2304):
                x-=self.speed
                if x<=140: x=140
            else:
                x-=self.speed
                backX+=self.speed
                if backX>=0: backX=0
        if self.keys[pygame.K_d]==1 and self.IssacCollideBoard==False:
            if (backX==0 and 0<=x<=576) or (backX==-1152 and 1728<=x<=2304):
                x+=self.speed
                if x>=2164: x=2164
            else:
                x+=self.speed
                backX-=self.speed
                if backX<=-1152: backX=-1152
        if self.keys[pygame.K_w]==1 and self.IssacCollideBoard==False:
            if (backY==0 and 0<=y<=324) or (backY==-648 and 972<=y<=1296):
                y-=self.speed
                if y<=100: y=100    #upper edge 100
            else:
                y-=self.speed
                backY+=self.speed
                if backY>=0: backY=0
        if self.keys[pygame.K_s]==1 and self.IssacCollideBoard==False:
            if (backY==0 and 0<=y<=324) or (backY==-648 and 972<=y<=1296):
                y+=self.speed
                if y>=1156: y=1156    #lower edge 140
            else:
                y+=self.speed
                backY-=self.speed
                if backY<=-648: backY=-648   
        (self.bgIssacRect)=(x,y)
        (self.bgRect)=(backX,backY)
        self.IssacRect=(backX+x-self.IssacWidth/2,
                    backY+y-self.IssacHeight/2)
                    
        if self.keys[pygame.K_UP]==1:
            if self.keys[pygame.K_d]==1:
                self.image=self.headUpbodyRight
            elif self.keys[pygame.K_a]==1:
                self.image=self.headUpbodyLeft
            else: self.image=self.headUpbodyDown
        elif self.keys[pygame.K_DOWN]==1:
            if self.keys[pygame.K_d]==1:
                self.image=self.headDownbodyRight
            elif self.keys[pygame.K_a]==1:
                self.image=self.headDownbodyLeft
            else: self.image=self.headDownbodyDown
        elif self.keys[pygame.K_LEFT]==1:
            if self.keys[pygame.K_d]==1:
                self.image=self.headLeftbodyRight
            elif self.keys[pygame.K_a]==1:
                self.image=self.headLeftbodyLeft
            else: self.image=self.headLeftbodyDown
        elif self.keys[pygame.K_RIGHT]==1:
            if self.keys[pygame.K_d]==1:
                self.image=self.headRightbodyRight
            elif self.keys[pygame.K_a]==1:
                self.image=self.headRightbodyLeft
            else: self.image=self.headRightbodyDown
        if (self.keys[pygame.K_UP]==0 and self.keys[pygame.K_DOWN]==0
    and self.keys[pygame.K_LEFT]==0 and self.keys[pygame.K_RIGHT]==0):
            if self.keys[pygame.K_a]==1: self.image=self.headLeftbodyLeft
            elif self.keys[pygame.K_d]==1: self.image=self.headRightbodyRight
            elif self.keys[pygame.K_w]==1: self.image=self.headUpbodyDown
            elif self.keys[pygame.K_s]==1: self.image=self.headDownbodyDown
            else: self.image=self.headDownbodyDown
        if self.timeCount%8==0:
            (direction,bulletX,bulletY)=(None,None,None)
            if self.keys[pygame.K_UP]==1:
                direction="up"
                (bulletX,bulletY)=(x-self.bulletSize/2,y-self.IssacHeight/2-self.bulletSize)
            elif self.keys[pygame.K_DOWN]==1:
                direction="down"
                (bulletX,bulletY)=(x-self.bulletSize/2,y)
            elif self.keys[pygame.K_LEFT]==1:
                direction="left"
                (bulletX,bulletY)=(x-self.bulletSize-self.IssacWidth/2,y-self.bulletSize/2)
            elif self.keys[pygame.K_RIGHT]==1:
                direction="right"
                (bulletX,bulletY)=(x+self.IssacWidth/2,y-self.bulletSize/2)
            if direction!=None and x!=None and y!=None:
                self.bulletCors.append((direction,bulletX,bulletY,x,y))
        if self.keys[pygame.K_UP]==1 or self.keys[pygame.K_DOWN]==1 or self.keys[pygame.K_LEFT]==1 or self.keys[pygame.K_RIGHT]==1:
            self.timeCount+=1
        if (self.keys[pygame.K_UP]==0 and self.keys[pygame.K_DOWN]==0
    and self.keys[pygame.K_LEFT]==0 and self.keys[pygame.K_RIGHT]==0):
            self.timeCount=0
            if self.keys[pygame.K_a]==1: self.image=self.headLeftbodyLeft
            elif self.keys[pygame.K_d]==1: self.image=self.headRightbodyRight
            elif self.keys[pygame.K_w]==1: self.image=self.headUpbodyDown
            elif self.keys[pygame.K_s]==1: self.image=self.headDownbodyDown
            else: self.image=self.headDownbodyDown
        
    # def keyReleased(self):
    #     if (self.keys[pygame.K_UP]==0 and self.keys[pygame.K_DOWN]==0
    # and self.keys[pygame.K_LEFT]==0 and self.keys[pygame.K_RIGHT]==0):
    #         if self.keys[pygame.K_a]==1: self.image=self.headLeftbodyLeft
    #         elif self.keys[pygame.K_d]==1: self.image=self.headRightbodyRight
    #         elif self.keys[pygame.K_w]==1: self.image=self.headUpbodyDown
    #         elif self.keys[pygame.K_s]==1: self.image=self.headDownbodyDown
    #         else: self.image=self.headDownbodyDown
        
        
    def timerFired(self, dt):
        #self.keys=pygame.key.get_pressed()
        newList=[]
        (backX,backY)=self.bgSize
        for bullet in self.bulletCors:
            (direction,x,y,IssacX,IssacY)=bullet
            if direction=="up":
                y-=self.bulletSpeed
                if y>=IssacY-self.IssacHeight/2-self.bulletSize-self.range and y>=50:
                    bullet=(direction,x,y,IssacX,IssacY)
                    newList.append(bullet)
            elif direction=="down":
                y+=self.bulletSpeed
                if y<=IssacY+self.range and y<=backY-50:
                    bullet=(direction,x,y,IssacX,IssacY)
                    newList.append(bullet)
            elif direction=="left":
                x-=self.bulletSpeed
                if x>=IssacX-self.bulletSize-self.IssacWidth/2-self.range and x>=100:
                    bullet=(direction,x,y,IssacX,IssacY)
                    newList.append(bullet)
            elif direction=="right":
                x+=self.bulletSpeed
                if x<=IssacX+self.range+self.IssacWidth/2 and x<=backX-130:
                    bullet=(direction,x,y,IssacX,IssacY)
                    newList.append(bullet)
        self.bulletCors=newList
        
    def redrawAll(self, screen):
        screen.blit(self.image,self.IssacRect)
        screen.blit(self.damageValue,(25,300))
        screen.blit(self.coinValue,(25,150))
        screen.blit(self.speedValue,(25,225))
        font=pygame.font.Font("Amatic-Bold.ttf",33)
        text=font.render(str(self.IssacDamage),True,(255,255,255))
        coinText=font.render(str(self.money),True,(255,255,255))
        speedText=font.render(str(self.speed),True,(255,255,255))
        screen.blit(text,(65,295))
        screen.blit(coinText,(65,145))
        screen.blit(speedText,(65,220))
        for bullet in self.bulletCors:
            (direction,x,y,IssacX,IssacY)=bullet
            (backX,backY)=self.bgRect
            bulletx=x+backX
            bullety=y+backY
            rect=(bulletx,bullety)
            screen.blit(self.bullet1,rect)
        n=0
        for i in range (len(self.blood)):
            if n<3 and "red" not in self.blood[i]:
                screen.blit(self.emptyheart,(20+n*self.displayheartWidth,20))
            else:
                if self.blood[i]=="red":
                    screen.blit(self.fullredheart,(20+n*self.displayheartWidth,20))
                elif self.blood[i]=="halfred":
                    screen.blit(self.halfredheart,(20+n*self.displayheartWidth,20))
                elif self.blood[i]=="blue":
                    screen.blit(self.blueheart,(20+n*self.displayheartWidth,20))
                elif self.blood[i]=="halfblue":
                    screen.blit(self.halfblueheart,(20+n*self.displayheartWidth,20))
                elif self.blood[i]=="black":
                    screen.blit(self.fullblackheart,(20+n*self.displayheartWidth,20))
                elif self.blood[i]=="halfblack":
                    screen.blit(self.halfblackheart,(20+n*self.displayheartWidth,20))
            n+=1
        if len(self.blood)<=3:
            empty=3-len(self.blood)
            for i in range (empty):
                screen.blit(self.emptyheart,(20+(len(self.blood)+i)*self.displayheartWidth,20))
            
        
# def main():
#     game = Issac()
#     game.run()
# 
# if __name__ == '__main__':
#     main()