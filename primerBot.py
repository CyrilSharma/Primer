import time
import numpy as np
import constants as c
from autoclicker import Autoclicker
import pyautogui
from logic import LogicHandler
from utils import determineEquality, determineNumber, grabScreen, loadFromFile

class Bot(Autoclicker):
    def __init__(self):
        super().__init__()
        self.logic = LogicHandler()
        self.savedImages = {}
        self.initialized = False
    
    def initialize(self):
        if not self.initialized:
            pyautogui.click(x = c.empty_position[0], y = c.empty_position[1], clicks=3, interval=0.5)
            self.fetchImages()
            self.initialized = True
    
    def fetchImages(self):
        self.savedImages["score"] = grabScreen(c.scorePosition, 45, 20)
        self.savedImages["heads"] = grabScreen(c.headsPosition, 30, 20)
        self.savedImages["tails"] = grabScreen(c.tailsPosition, 30, 20)
    
    def chooseMove(self):
        headsImg = grabScreen(c.headsPosition, 30, 20)
        numHeads = determineNumber(headsImg)

        # error correction
        if numHeads is None:
            return c.flip_position

        headsUpdate, tailsUpdate = self.findUpdates()
        if (headsUpdate == 1 and tailsUpdate == 1):
            if (self.logic.moves == 0):
                headsUpdate = numHeads if (numHeads == 1 or numHeads == 0) else 1
                tailsUpdate = 1 - numHeads if (numHeads == 1 or numHeads == 0) else 0
        print(f"H+ {headsUpdate} | L+ {tailsUpdate}")
        self.logic.update(headsUpdate)

        action = self.logic.getAction()
        if action != 0:
            self.logic.display()
            
        if action == 0:
            return c.flip_position
        elif action == 1:
            self.logic.reset()
            return c.fair_position
        elif action == 2:
            self.logic.reset()
            return c.cheater_position
    
    def findUpdates(self):
        imgH = grabScreen(c.headsPosition, 30, 20)
        imgT = grabScreen(c.tailsPosition, 30, 20)
        updates = [0,0]
        updates[0] = 0 if determineEquality(self.savedImages["heads"], imgH, cutoff=7000) else 1
        updates[1] = 0 if determineEquality(self.savedImages["tails"], imgT, cutoff=7000) else 1
        return updates
    
    def checkIfCorrect(self):
        img = grabScreen(c.scorePosition, 45, 20)
        if determineEquality(self.savedImages["score"],img, cutoff=7000):
            self.savedImages["score"] = img
            return False
        else:
            self.savedImages["score"] = img
            return True
    
    def gameOver(self):
        pyautogui.click(x = c.namePosition[0], y = c.namePosition[1])
        pyautogui.typewrite('zetaSquare')
        pyautogui.click(x = c.gameOverPosition[0], y = c.gameOverPosition[1])
        time.sleep(1.0)
        pyautogui.hotkey('cmd', 'r')
        time.sleep(8.0)
        pyautogui.click(x = c.animation_position[0], y = c.animation_position[1])
        self.fetchImages()

    def run(self):
        while self.program_running:
            while self.running:
                self.initialize()
                move = self.chooseMove()
                self.fetchImages()
                pyautogui.click(x = move[0], y = move[1])
                if move == c.flip_position:
                    time.sleep(c.flipDelay)
                else:
                    correct = self.checkIfCorrect()
                    print("Correct: " + str(correct))
                    time.sleep(c.choiceDelay)
                if determineGameOver():
                    self.gameOver()

def determineGameOver():
    img = grabScreen(c.gameOverPosition, 1, 1)
    return img[0][0] == 255