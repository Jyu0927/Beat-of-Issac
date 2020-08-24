#framework cited from CMU 15112 website
#http://www.cs.cmu.edu/~112/notes/notes-oop.html
#font downloaded from https://www.fontsquirrel.com/fonts/amatic
#all the images all taken directly from the game the afterbirth of Isaac
import pygame
import os.path
from pathlib import Path
from pygamegame import PygameGame
from Issac import Issac
from Monster import *
from MakeBoard import *
from Items import *
from beatDetection import *
import random
########make evilIssac shoot bullets!!!!!
###ghost can't be killed by Issac bullets!
###Issac can't be hurt by huge flies' bullet!
class Game(PygameGame):
    
    def init(self):
        self.mode="start"
        Issac.init(self)
        (x,y)=(self.bgIssacRect)
        Monster.init(self)
        Items.init(self)
        self.timecount=0
        self.IssacHurtTime=0
        #Monster.init(x,y)
        self.startBackground=pygame.image.load("startbg.png")
        self.losingBg=pygame.image.load("losing.png")
        self.winningBg=pygame.image.load("winning.png")
        self.instructionBg=pygame.image.load("instructionbg.png")
        self.gameWon=False
        self.instructionHighLighted=False
        self.gameHighLighted=False
        self.musicTime=0
        self.musicPlaying=False
        self.countdown=100
        self.inputString=""
        self.musicBeat=None
        MakeBoard.init(self)
        self.gamePause=False
        self.musicStopped=False
        
    def keyPressed(self):
        if self.mode=="start":
            if 1 in self.keys:
                if self.keys[pygame.K_RETURN]==1:
                    try:
                        self.musicBeat=beatDetection(self.inputString)
                        self.music=self.inputString
                    except:
                        self.inputString=""
                elif self.keys[pygame.K_BACKSPACE]==1:
                    self.inputString=self.inputString[:-1]
                else:
                    key = [pygame.key.name(index) for index, press in enumerate(self.keys) if press][0]
                    self.inputString+=str(key)
        elif self.mode=="instructions":
            # if self.keys[pygame.K_SPACE]==1:
            #     self.mode="game"
            if self.keys[pygame.K_s]==1:
                self.mode="start"
        elif self.mode=="makeboard":
            MakeBoard.keyPressed(self)
            if self.keys[pygame.K_s]==1:
                self.mode="start"
        elif self.mode=="game" and self.gamePause==True:
            if self.musicStopped==False:
                pygame.mixer.music.pause()
                self.musicStopped=True
            if self.keys[pygame.K_p]==1:
                self.gamePause=not self.gamePause
                if self.musicStopped==True:
                    pygame.mixer.music.unpause()
                    self.musicStopped=False
        elif self.mode=="game" and self.gamePause==False:
            if self.keys[pygame.K_r]==1:
                self.mode="start"
                Game.init(self)
                pygame.mixer.music.stop()
            MakeBoard.IssacandBoard(self)
            Issac.keyPressed(self)
            if self.keys[pygame.K_p]==1:
                self.gamePause=not self.gamePause
            if self.keys[pygame.K_b]==1 and len(self.storeLst)>0 and self.money>=10:
                self.money-=10
                item=self.storeLst[0]
                if item==self.damageup1:
                    self.IssacDamage+=10
                elif item==self.damageup2:
                    self.IssacDamage+=15
                elif item==self.speedup1:
                    self.speed+=5
                elif item==self.speedup2:
                    self.speed+=5
                elif item==self.randomneedle:
                    damagevalue=random.randint(-5,10)
                    speedvalue=random.randint(-5,5)
                    self.IssacDamage+=damagevalue
                    self.speed+=speedvalue
                self.storeLst.pop(0)
        elif self.mode=="lost" or self.mode=="won":
            if self.keys[pygame.K_s]==1:
                self.mode="start"
                Game.init(self)
            
            

                
        
    def timerFired(self,dt):
        if self.timecount%100==0:
            lordimage=self.lordoffliesShooting
            LordofFlies.shootFlies(self)
        else:
            lordimage=self.lordofflies    
        if self.firing==True:
            self.firingTime+=1
        if self.firingTime>=50:
            self.firingTime=0
            self.firing=False
        self.keys=pygame.key.get_pressed()
        self.timecount+=1
        if len(self.blood)==0 and self.gameWon==False:
            self.mode="lost"
            pygame.mixer.music.stop()
        if len(self.blood)>0 and self.gameWon==True:
            self.mode="won"
        if self.mode=="game" and self.gamePause==False:
            newHitLst=[]
            for monster in self.monsterHitLst:
                time=monster[3]-1
                if time>0:
                    newHitLst.append((monster[0],monster[1],monster[2],time))
            self.monsterHitLst=newHitLst
            if (pygame.mixer.music.get_busy()==False and len(self.blood)>0 and self.normalFlyLst==[] and
                self.bigFlyLst==[] and self.hugeFlyLst==[] and self.spiderLst==[] and
                self.ghostLst==[] and self.dodgingMonsterLst==[] and self.lordoffliesLst==[] and
                self.firingMonsterLst==[]):
                    self.mode="won"
            self.musicTime+=1
            Issac.timerFired(self,dt)
            NormalFly.moveMonster(self,10)
            BigFly.moveMonster(self,2)
            HugeFly.moveMonster(self)
            LordofFlies.moveMonster(self,lordimage)
            for monster in self.bigFlyLst:
                if self.timecount%30==0:
                    BigFly.shootBullet(self,monster)
            if self.firing==False:
                chance=random.randint(1,100)
                if chance<=3:
                    self.firing=True
            ####make monster fire here
            if self.firing==True:
                fireImage=self.firingMonsterFiring
            else:
                fireImage=self.firingMonster
            FiringMonster.moveMonster(self,fireImage)
            BigFly.moveBullet(self)
            if self.timecount%30==0:
                HugeFly.shootBullet(self)
            HugeFly.moveBullet(self)
            Spider.moveMonster(self,5)
            #Spider.monsterCollide(self,self.spiderLst,self.spiderWidth,self.spiderHeight)
            EvilIssac.moveMonster(self,3)
            Ghost.moveMonster(self)
            DodgingMonster.moveMonster(self,3)
            Coin.collide(self)
            Heart.collide(self)
            if len(self.blood)>0:
                BigFly.bulletCollide(self)
                HugeFly.bulletCollide(self)
            if self.IssacHurt==False:
                self.normalFlyLst=NormalFly.monsterCollide(self,self.normalFlyLst,self.normalFlyWidth,self.normalFlyHeight)
                self.hugeFlyLst=HugeFly.monsterCollide(self,self.hugeFlyLst,self.hugeFlyWidth,self.hugeFlyHeight)
                self.spiderLst=Spider.monsterCollide(self,self.spiderLst,self.spiderWidth,self.spiderHeight)
                self.evilIssacLst=EvilIssac.monsterCollide(self,self.evilIssacLst,self.evilIssacWidth,self.evilIssacHeight)
                self.ghostLst=Ghost.monsterCollide(self,self.ghostLst,self.ghostWidth,self.ghostHeight)
                self.dodgingMonsterLst=DodgingMonster.monsterCollide(self,self.dodgingMonsterLst,self.dodgingMonsterWidth,self.dodgingMonsterHeight)
                self.lordoffliesLst=LordofFlies.monsterCollide(self,self.lordoffliesLst,self.lordoffliesWidth,self.lordoffliesHeight)
                MakeBoard.IssacandSpines(self)
                if self.firing==True:
                    self.firingMonsterLst=FiringMonster.monsterCollide(self,self.firingMonsterLst,self.firingMonsterWidth,self.firingMonsterFiringHeight)
                else:
                    self.firingMonsterLst=FiringMonster.monsterCollide(self,self.firingMonsterLst,self.firingMonsterWidth,self.firingMonsterHeight)
            else:
                self.IssacHurtTime+=1
                if self.IssacHurtTime==20:
                    self.IssacHurt=False
                    self.IssacHurtTime=0
            newbulletLst=[]
            hitLst=[]
            for bullet in self.bulletCors:
                hitLst=[]
                (bulletX,bulletY)=(bullet[1],bullet[2])
                (self.normalFlyLst,hit)=NormalFly.IssacBulletCollide(self,bulletX,bulletY,self.normalFlyLst,self.normalFlyWidth,self.normalFlyHeight)
                hitLst.append(hit)
                (self.bigFlyLst,hit)=BigFly.IssacBulletCollide(self,bulletX,bulletY,self.bigFlyLst,self.bigFlyWidth,self.bigFlyHeight)
                hitLst.append(hit)
                (self.hugeFlyLst,hit)=HugeFly.IssacBulletCollide(self,bulletX,bulletY,self.hugeFlyLst,self.hugeFlyWidth,self.hugeFlyHeight)
                hitLst.append(hit)
                (self.spiderLst,hit)=Spider.IssacBulletCollide(self,bulletX,bulletY,self.spiderLst,self.spiderWidth,self.spiderHeight)
                hitLst.append(hit)
                (self.evilIssacLst,hit)=EvilIssac.IssacBulletCollide(self,bulletX,bulletY,self.evilIssacLst,self.evilIssacWidth,self.evilIssacHeight)
                hitLst.append(hit)
                (self.ghostLst,hit)=Ghost.IssacBulletCollide(self,bulletX,bulletY,self.ghostLst,self.ghostWidth,self.ghostHeight)
                hitLst.append(hit)
                (self.dodgingMonsterLst,hit)=DodgingMonster.IssacBulletCollide(self,bulletX,bulletY,self.dodgingMonsterLst,self.dodgingMonsterWidth,self.dodgingMonsterHeight)
                hitLst.append(hit)
                (self.lordoffliesLst,hit)=LordofFlies.IssacBulletCollide(self,bulletX,bulletY,self.lordoffliesLst,self.lordoffliesWidth,self.lordoffliesHeight)
                hitLst.append(hit)
                (self.firingMonsterLst,hit)=FiringMonster.IssacBulletCollide(self,bulletX,bulletY,self.firingMonsterLst,self.firingMonsterWidth,self.firingMonsterHeight)
                hitLst.append(hit)
                if True not in hitLst:
                    newbulletLst.append(bullet)
            self.bulletCors=newbulletLst
            
        
        
        
        
        
        
        
    def redrawAll(self,screen):
        pygame.font.init()
        if self.mode=="start":
            #screenSize(1152,648)
            pygame.mixer.init(44100, -16,2,2048)
            screen.blit(self.startBackground,(0,0))
            font=pygame.font.Font("Amatic-Bold.ttf",200)
            otherFont=pygame.font.Font("AmaticSC-Regular.ttf",40)
            musicFont=pygame.font.Font("Amatic-Bold.ttf",30)
            otherHighlighted=pygame.font.Font("Amatic-Bold.ttf",40)
            text=font.render("BEAT    OF    ISAAC",True,(255,255,255))
            pygame.draw.rect(screen,(255,255,255),(20,585,400,35),0)
            pathText=musicFont.render(self.inputString,True,(0,0,0))
            screen.blit(pathText,(20,585))
            (mouseX,mouseY)=pygame.mouse.get_pos()
            getMusicText=otherHighlighted.render("type  path  of  your  song  and  press  enter",True,(255,255,255))
            screen.blit(getMusicText,(20,520))
            if self.musicBeat!=None:
                self.inputString=""
                gotMusicText=musicFont.render("Got  Your  Music!",True,(0,0,0))
                screen.blit(gotMusicText,(20,585))
            if 840<=mouseX<=980 and 510<=mouseY<=545:
                instructionText=otherHighlighted.render("INSTRUCTIONS",True,(255,255,0))
                self.mode="instructions"
            else:
                instructionText=otherHighlighted.render("INSTRUCTIONS",True,(255,255,255))
            if 840<=mouseX<=1080 and 550<=mouseY<=585:
                makeBoardText=otherHighlighted.render("MAKE  YOUR  OWN  BOARD",True,(255,255,0))
                self.mode="makeboard"
            else:
                makeBoardText=otherHighlighted.render("MAKE  YOUR  OWN  BOARD",True,(255,255,255))
            if 840<=mouseX<=1020 and 590<=mouseY<=625:
                gameText=otherHighlighted.render("START  YOUR  GAME",True,(255,255,0))
                self.mode="game"
                if self.musicBeat==None:
                    self.music="default.wav"
                self.musicBeat=beatDetection(self.music)
                (self.level0,self.level1,self.level2,self.level3)=beatLevel(self.musicBeat)
                pygame.mixer.music.load(self.music)
                pygame.mixer.music.play()
            else:
                gameText=otherHighlighted.render("START  YOUR  GAME",True,(255,255,255))
            screen.blit(text,(210,150))
            screen.blit(gameText,(840,590))
            screen.blit(instructionText,(840,510))
            screen.blit(makeBoardText,(840,550))
        elif self.mode=="makeboard":
            MakeBoard.redrawAll(self,screen)
            font=pygame.font.Font("Amatic-Bold.ttf",30)
            text11=font.render("press  'space'  to  place  obstacle,  press  again  to  change  or  cancel.",True,(255,255,0))
            text12=font.render("when  ready,  press  's'  to  go  back  to  start  screen.", True, (255,255,0))
            screen.blit(text11,(20,15))
            screen.blit(text12,(20,50))
        elif self.mode=="instructions":
            screen.blit(self.instructionBg,(0,0))
            font=pygame.font.Font("Amatic-Bold.ttf",35)
            titleFont=pygame.font.Font("Amatic-Bold.ttf",70)
            titleText=titleFont.render("INSTRUCTIONS",True,(0,0,0))
            s=pygame.Surface((900,550))
            s.set_alpha(90)
            s.fill((255,255,255))
            screen.blit(s,(126,50))
            #the obstacles only affects Issac but not monsters nor Issac's bullets
            #when the music ends, you have unlimited time to kill all the monsters to win
            #explore rest of the game by yourself and have fun!
            #press 's' to go back to start page and start the game
            text0=font.render("the  music  path  input  only  takes  in  wav  files,  type  only  lowercase  letters.", True,(0,0,0))
            text1=font.render("have  a  simple  file  name  and  put  the  file  inside  the  folder  to  make  it  easier.",True,(0,0,0))
            text2=font.render("go  to  'make  your  own  board'  to  add  obstacles  onto  the  board  to  make  game  harder.",True,(0,0,0))
            text3=font.render("'w',  'a',  's',  'd'  control  movements  and  'up',  'down',  'left',  'right'  control  bullets.",True,(0,0,0))
            text4=font.render("the  obstacles  only  affect  isaac  but  not  monsters  or  Isaac's  bullets",True,(0,0,0))
            text5=font.render("monsters  and  items  will  appear  in  random  locations  based  on  beats  of  your  song.",True,(0,0,0))
            text6=font.render("press  'b'  to  buy  tools  to  upgrade  Issac.",True,(0,0,0))
            text7=font.render("when  the  music  ends,  you  have  unlimited  time  to  kill  all  the  monsters  to  win.",True,(0,0,0))
            text8=font.render("when  in  game,  press  'r'  to  restart  the  game,  press  'p'  to  pause  and  resume  the  game.", True, (0,0,0))
            text9=font.render("explore  rest  of  the  game  by  yourself  and  have  fun!",True,(0,0,0))
            text10=font.render("#this  is  a  humble  remake  of  the  game  'afterbirth  of  isaac'",True,(0,0,0))
            text11=font.render("press  's'  to  go  back  to  the  start  screen.",True, (255,255,0))
            screen.blit(text0,(180,150))
            screen.blit(text1,(180,185))
            screen.blit(text2,(180,220))
            screen.blit(text3,(180,255))
            screen.blit(text4,(180,290))
            screen.blit(text5,(180,325))
            screen.blit(text6,(180,360))
            screen.blit(text7,(180,395))
            screen.blit(text8,(180,430))
            screen.blit(text9,(180,465))
            screen.blit(text10,(180,500))
            screen.blit(text11,(400,540))
            screen.blit(titleText,(450,70))
        elif self.mode=="game":
            screen.fill((255, 255, 255))
            screen.blit(self.bg,self.bgRect)
            MakeBoard.gameBg(self,screen)
            Issac.redrawAll(self,screen)
            #MakeBoard.gameBg(self,screen)
            if self.IssacHurt==True and self.IssacHurtTime<=3:
                MakeBoard.IssacHitEffect(self,screen)
            try:
                (nextTime,nextBeat)=self.musicBeat[0]
                time=pygame.mixer.music.get_pos()//10
                #print (time,nextTime)
                if time>=nextTime*100:
                    self.musicBeat.pop(0)
                    while len(self.musicBeat)>0 and self.musicBeat[0][0]==nextTime:
                        self.musicBeat.pop(0)
                    #LordofFlies.addMonster(self,100,self.lordofflies, None,self.lordoffliesLst)
                    if self.level0<=nextBeat<self.level1:
                        num=random.randint(0,4)
                        if num==0:
                            NormalFly.addMonster(self,20,self.fly,None,self.normalFlyLst)
                        elif num==1:
                            Spider.addMonster(self,20,self.spider,None,self.spiderLst)
                        elif num==2:
                            EvilIssac.addMonster(self,20,self.evilIssac,None,self.evilIssacLst)
                        elif num==3:
                            Coin.placeItem(self,self.coin,self.coinLst)
                        elif num==4:
                            Heart.placeItem(self,self.itemRedheart,self.heartLst)
                    if self.level1<=nextBeat<self.level2:
                        num=random.randint(0,4)#make keys
                        if num==0:
                            BigFly.addMonster(self)
                        elif num==1:
                            HugeFly.addMonster(self,30,self.fly3left,self.fly3right,self.hugeFlyLst)
                        elif num==2:
                            Ghost.addMonster(self,50,self.ghost,None,self.ghostLst)
                        elif num==3:
                            Heart.placeItem(self,self.itemBlueheart,self.heartLst)
                        elif num==4:
                            DodgingMonster.addMonster(self,50,self.dodgingMonsterLeft,self.dodgingMonsterRight,self.dodgingMonsterLst)
                        #elif num==5: place keys
                    elif self.level2<=nextBeat<self.level3:
                        num=random.randint(0,2)
                        if num==0:
                            if len(self.lordoffliesLst)==0:
                                LordofFlies.addMonster(self,150,self.lordofflies,None,self.lordoffliesLst)
                            else:
                                FiringMonster.addMonster(self)
                        elif num==1:
                            FiringMonster.addMonster(self)
                        elif num==2:
                            Heart.placeItem(self,self.itemBlackheart,self.heartLst)
                        #create monsters and golden chests
                        ####doesn't create big monsters!"""
            except:
                pass
            NormalFly.redrawAll(self,screen,None,self.normalFlyLst)
            BigFly.redrawAll(self,screen)
            HugeFly.redrawAll(self,screen,self.hugeFlyBulletLst,self.hugeFlyLst)
            Spider.redrawAll(self,screen,None,self.spiderLst)
            EvilIssac.redrawAll(self,screen,None,self.evilIssacLst)
            Ghost.redrawAll(self,screen,None,self.ghostLst)
            LordofFlies.redrawAll(self,screen,None,self.lordoffliesLst)
            FiringMonster.redrawAll(self,screen,None,self.firingMonsterLst)
            DodgingMonster.redrawAll(self,screen,None,self.dodgingMonsterLst)
            Coin.redrawAll(self,screen,self.coinLst)
            Heart.redrawAll(self,screen,self.heartLst)
            MakeBoard.MonsterHitEffect(self,screen)
            font=pygame.font.Font("Amatic-Bold.ttf",35)
            if len(self.storeLst)>0:
                storeImage=self.storeLst[0]
                screen.blit(storeImage,(1020,200))
                storetext=font.render("$    10",True,(255,255,255))
            else:
                storetext=font.render("Sold Out",True,(255,255,255))
            screen.blit(storetext,(1020,150))
            if self.gamePause==True:
                s=pygame.Surface((600,300))
                s.set_alpha(90)
                s.fill((255,255,255))
                screen.blit(s,(276,174))
                font=pygame.font.Font("Amatic-Bold.ttf",150)
                text=font.render("game   paused",True,(0,0,0))
                screen.blit(text,(330,180))
                font2=pygame.font.Font("Amatic-Bold.ttf",70)
                text2=font2.render("press   'p'   to   resume",True,(255,255,0))
                screen.blit(text2,(390,350))
        elif self.mode=="lost":
            screen.blit(self.losingBg,(0,0))
            font=pygame.font.Font("Amatic-Bold.ttf",200)
            startFont=pygame.font.Font("Amatic-Bold.ttf",88)
            startText=startFont.render("PRESS   'S'   TO   RESTART",True,(255,255,255))
            text=font.render("YOU   LOSE",True,(255,255,255))
            screen.blit(text,(370,150))
            screen.blit(startText,(370,380))
        elif self.mode=="won":
            screen.blit(self.winningBg,(0,0))
            font=pygame.font.Font("Amatic-Bold.ttf",200)
            startFont=pygame.font.Font("Amatic-Bold.ttf",88)
            startText=startFont.render("PRESS  'S'  TO   RESTART",True,(255,255,255))
            text=font.render("YOU  WON",True,(255,255,255))
            screen.blit(text,(370,150))
            screen.blit(startText,(370,380))

                        
            
            
            #level 1 monsters:spiders, normalflies, evil Issacs, 
            #level 2 monsters:bigflies, hugeflies, ghosts, 
            #level 3 monsters: monstros, etc. big monsters
            #level 1 items: coins, red heart
            #level 2 items: blueheart, keys
            #level 3 items: blackheart, gloden chest
        
        
        
        
def main():
    game = Game()
    game.run()

if __name__ == '__main__':
    main()