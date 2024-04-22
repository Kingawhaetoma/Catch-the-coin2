# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 23:27:14 2024

@author: kinga
"""

import pygame, random, simpleGE

class Coin(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("Coin.png")
        self.setSize(25, 25)
        self.reset()
        self.coinSound = simpleGE.Sound("coinEffect.wav")
        
    def reset(self):
        self.y = 10
        self.x = random.randint(0, self.screenWidth)
        self.dy = random.randint(3, 8)
        
    def checkBounds(self):
        if self.bottom > self.screenHeight:
            self.reset()


class Boy(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("boy.png")
        self.setSize(90, 90)
        self.position = (320, 400)
        self.moveSpeed = 5
    
    def process(self):
        if self.isKeyPressed(pygame.K_LEFT):
            self.x -= self.moveSpeed
        if self.isKeyPressed(pygame.K_RIGHT):
            self.x += self.moveSpeed
            
class LblScore(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Score: 0"
        self.center = (120, 30)
        
class LblTime(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Time Left: 10"
        self.center = (500, 30) 


class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.setImage("sky.png")
        
        self.timer = simpleGE.Timer()
        self.timer.totalTime = 10
        self.score = 0
        
        self.boy = Boy(self)
        self.coins = [Coin(self) for _ in range(10)]
        
        self.lblScore = LblScore()
        self.lblTime = LblTime()
        
        self.sprites = [self.boy, self.coins, self.lblScore, self.lblTime]
        
        pygame.mixer.music.load("newSong.mp3")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
    
    def process(self):
        for coin in self.coins:
            if coin.collidesWith(self.boy):
                coin.coinSound.play()
                coin.reset()
                self.score += 1
                self.lblScore.text = f"Score: {self.score}"
                
        self.lblTime.text = f"Time Left: {self.timer.getTimeLeft():.2f}"
        if self.timer.getTimeLeft() < 0:
            print(f"Final Score: {self.score}")
            self.stop()

class Instruction(simpleGE.Scene):
    def __init__(self, score):
        super().__init__()
        self.setImage("plainField.png")
        
        self.response = "quit"
        
        self.instruction = simpleGE.MultiLabel()
        self.instruction.textLines = [
            "Welcome to Kross's Coin Collector!",
            "You are playing as Kross, the adventurous boy.",
            "Use the left and right arrow keys to move Kross.",
            "Your objective is to collect as many coins as possible in 10 seconds.",
            "",
            "Good luck and have fun!"]
        
        self.instruction.center = (320, 240)
        self.instruction.size = (500, 250)
        
        self.prevScore = score
        self.lblScore = simpleGE.Label()
        self.lblScore.text = f"Last Score: {self.prevScore}"
        self.lblScore.center = (320, 50)
        
        self.btnPlay = simpleGE.Button()
        self.btnPlay.text = "Play (Up)"
        self.btnPlay.center = (100, 400)
        
        self.btnQuit = simpleGE.Button()
        self.btnQuit.text = "Quit (Down)"
        self.btnQuit.center = (550, 400)
        
        self.sprites = [self.instruction, 
                        self.lblScore, 
                        self.btnPlay, 
                        self.btnQuit]

        
    def process(self):
        if self.btnQuit.clicked:
            self.response = "quit"
            self.stop()
        if self.btnPlay.clicked:
            self.response = "play"
            self.stop()

        if self.isKeyPressed(pygame.K_UP):
            self.response = "play"
            self.stop()
        if self.isKeyPressed(pygame.K_DOWN):
            self.response = "quit"
            self.stop()


def main():
    keepGoing = True
    score = 0
    while keepGoing:
        instruction = Instruction(score)
        instruction.start()
        
        if instruction.response == "play":
            game = Game()
            game.start()
            score = game.score
        else:
            keepGoing = False

if __name__ == "__main__":
    main()
