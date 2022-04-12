from utils import loadFromFile, bayesianUpdate
import numpy as np

class LogicHandler():
    def __init__(self):
        self.prior = np.ones(2) * 0.5
        self.numHeads = 0
        self.numTails = 0
        self.stateEvaluator = loadFromFile()
        self.moves = 0
    
    def update(self, coinFlip):
        self.prior = bayesianUpdate(self.prior, coinFlip, np.array([0.5, 0.75]))
        self.numHeads += coinFlip
        self.numTails += 0 if coinFlip == 1 else 1
        self.moves += 1
    
    def getAction(self):
        action = self.stateEvaluator[(self.numHeads, self.numTails)]
        if action == 0:
            return action
        elif action == 1:
            inc = np.argmax(self.prior)
            return action + inc
        return None
    
    def reset(self):
        self.numHeads = 0
        self.numTails = 0
        self.moves = 0
        self.prior = np.ones(2) * 0.5
    
    def display(self):
        print(f"Heads: {self.numHeads} | Tails: {self.numTails} | Action {self.getAction()} | Moves: {self.moves} | Prior : {self.prior}")