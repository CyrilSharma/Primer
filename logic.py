from json import load
import threading
import time
from numsaver import changeToGrayScale
import cv2
import mss
import numpy as np
import constants as c
from pynput.mouse import Button, Controller
import pynput.keyboard as pynputKeyboard
from pynput.keyboard import Key
from autoclicker import Autoclicker
from utils import bayesianUpdate, loadFromFile

class Bot(Autoclicker):
    def __init__(self):
        super().__init__()
        self.numHeads = 0
        self.moves = 0
        self.biasRange = np.array([0.5,0.75])
        self.mouse = Controller()
        self.keyboard = pynputKeyboard.Controller()
        self.stateEvaluator = loadFromFile()
        self.initializePrior()
        self.initialized = False

    def initializePrior(self):
        self.prior = np.ones(2) * 1 / 2
    
    def chooseMove(self):
        self.moves += 1
        img = grabScreen()
        numHeads = determineNumber(img)
        coinToss = numHeads - self.numHeads
        self.numHeads = numHeads
        self.prior = bayesianUpdate(self.prior, coinToss, self.biasRange)
        numTails = self.moves - self.numHeads - 1
        print("Num heads: " + str(numHeads) + " | Num tails: " + str(numTails))
        if (self.numHeads, numTails) in self.stateEvaluator:
            action = self.stateEvaluator[(self.numHeads, numTails)]
            print("Chose " + str(action))
        else:
            action = 1
        if action == 0:
            return c.flip_position
        else:
            verdict = np.argmax(self.prior)
            if verdict == 0:
                self.numHeads = 0
                self.initializePrior()
                self.moves = 0
                return c.fair_position
            else:
                self.numHeads = 0
                self.initializePrior()
                self.moves = 0
                return c.cheater_position


    def chooseMove1(self):
        self.moves += 1
        img = grabScreen()
        numHeads = determineNumber(img)
        coinToss = numHeads - self.numHeads
        self.numHeads = numHeads
        print("Prior: ", self.prior, " CoinToss: ", coinToss)
        self.prior = bayesianUpdate(self.prior, coinToss, self.biasRange)
        print("Updated Prior: ", self.prior)
        expectedVal = expectedValue(self.prior)
        print("Num heads: " + str(numHeads) + " | Num tails: " + str(self.moves - self.numHeads - 1))
        print("Expected value: " + str(expectedVal))

        if ((expectedVal < 10.0 and self.moves < 16) and not (expectedVal > -2 and self.moves > 5)) or self.moves < 5:
            return c.flip_position
        else:
            fairProb = self.prior[0]
            if fairProb > 0.5:
                self.numHeads = 0
                self.initializePrior()
                self.moves = 0
                print("Chose Fair", end="\n\n")
                return c.fair_position
            else:
                self.numHeads = 0
                self.initializePrior()
                self.moves = 0
                print("Chose Cheating", end="\n\n")
                return c.cheater_position
    
    def initialize(self):
        if not self.initialized:
            self.mouse.position = c.empty_position
            for _ in range(3):
                self.mouse.click(Button.left, 1)
                time.sleep(1.0)
            self.initialized = True
    
    def clickCheckBox(self):
        self.mouse.position = c.empty_position
        self.mouse.click(Button.left, 1)
        time.sleep(0.5)
        self.mouse.position = c.animation_position
        self.mouse.click(Button.left, 1)
        time.sleep(0.5)
    
    def commandRefresh(self):
        self.keyboard.press(Key.cmd)
        self.keyboard.press('r')
        self.keyboard.release('r')
        self.keyboard.release(Key.cmd)
    
    def run(self):
        while self.program_running:
            while self.running:
                self.initialize()
                if self.moves > 0:
                    move = self.chooseMove()
                else:
                    move = c.flip_position
                    self.moves += 1
                self.mouse.position = move
                self.mouse.press(Button.left)
                time.sleep(0.5)
                self.mouse.release(Button.left)
                if move == c.flip_position:
                    if self.moves < 1:
                        time.sleep(2.5)
                    else:
                        time.sleep(c.flipDelay)
                else:
                    time.sleep(c.choiceDelay)
                if determineGameOver():
                    self.mouse.position = c.namePosition
                    self.mouse.click(Button.left, 1)
                    self.keyboard.type('Knota Scrypt')
                    self.mouse.position = c.gameOverPosition
                    self.mouse.click(Button.left, 1)
                    time.sleep(1.0)
                    self.commandRefresh()
                    time.sleep(8.0)
                    self.clickCheckBox()
                    self.moves = 0
                    self.numHeads = 0
                    self.initializePrior()

def expectedValue(prior):
    fairProb = prior[0]
    cheatProb = 1 - fairProb
    highestProb = max(fairProb, cheatProb)
    expectedValue = highestProb * c.winValue + (1 - highestProb) * c.lossValue
    # print(highestProb, expectedValue)
    return expectedValue
    

def grabScreen():
    with mss.mss() as sct:
        monitor = {'top': 436, 'left': 802, 'width': 30, 'height': 20}
        # Get raw pixels from the screen, save it to a Numpy array
        raw_img = sct.grab(monitor)
        img = np.array(raw_img)
        rgb = np.delete(img, 3, axis=2)
        img = changeToGrayScale(rgb)
    return img

def determineGameOver():
    with mss.mss() as sct:
        monitor = {'top': c.gameOverPosition[0], 'left': c.gameOverPosition[1], 'width': 1, 'height': 1}
        # Get raw pixels from the screen, save it to a Numpy array
        raw_img = sct.grab(monitor)
        img = np.array(raw_img)
        rgb = np.delete(img, 3, axis=2)
        img = changeToGrayScale(rgb)
        if img[0][0] != 255:
            return False
        else:
            return True

def determineEquality(img1, img2):
    diff = img1 - img2
    diff = np.absolute(diff)
    diff = np.sum(diff, axis=None)
    if diff < 12000:
        return True

def determineNumber(img):
    with open('nums.npy', 'rb') as f:
        digitArray = np.load(f)

    matchIndex = -1
    for i in range(len(digitArray)):
        if determineEquality(img, digitArray[i]):
            matchIndex = i
            break
    if matchIndex == -1:
        return -1
    elif matchIndex == 0:
        return 0
    elif matchIndex == 1:
        return 0
    else:
        return matchIndex - 1

def main():
    primerBot = Bot()
    primerBot.run()

if __name__ == '__main__':
    main()