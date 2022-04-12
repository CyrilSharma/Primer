import random
import numpy as np
import csv
from bruteforce import tablePrint
from tqdm import tqdm

from utils import bayesianUpdate, probSequence

def main():
    train()

class coinSimulator():
    def __init__(self):
        self.prob = random.choice([0.5,0.75])
        self.score = 0
        self.flips = 100
        self.numHeads = 0
        self.numTails = 0
        self.gameOver = False
    
    def updateCharacter(self):
        self.prob = random.choice([0.5,0.75])
        self.numHeads = 0
        self.numTails = 0
    
    def flip(self):
        if self.flips > 0:
            self.flips -= 1
        result = np.random.choice([1,0], p=[self.prob, 1-self.prob])
        if result == 1:
            self.numHeads += 1
        else:
            self.numTails += 1
        return result
    
    def choose(self, choice):
        previous_prob = self.prob
        self.updateCharacter()
        if choice == "fair":
            if previous_prob == 0.5:
                self.flips += 15
                self.score += 1
                return True
        elif choice == "cheater":
            if previous_prob == 0.75:
                self.flips += 15
                self.score += 1
                return True
        self.flips -= 30
        self.gameOver = self.flips < 0
        return False
    
    def reset(self):
        self.prob = random.choice([0.5,0.75])
        self.heads = 0
        self.tails = 0
        self.gameOver = False
        self.score = 0
        self.flips = 100

# (s, a, value)
def train():
    simulator = coinSimulator()
    stateActionMap = {}
    iterations = 5
    numSims = 10000
    for iterNum in range(iterations):
        maxScore = 0
        qTable = {}
        visits = {}
        for i in tqdm(range(numSims)):
            actions = []
            states = [(0,0)]
            prior = np.ones(2) * 1 / 2
            turns = 0

            simulator.reset()
            while simulator.gameOver is False:
                if simulator.flips > 0 and turns < 16:
                    if states[turns] in stateActionMap:
                        desiredChoice = stateActionMap[states[turns]]
                        oppositeChoice = 0 if desiredChoice == 1 else 1
                        selectionProb = (1 - 1 / (iterNum + 2)) if iterNum != iterations - 1 else 1
                        action = np.random.choice([desiredChoice, oppositeChoice], p=[selectionProb, 1 - selectionProb])
                    else:
                        action = np.random.choice([0,1], p=[0.75,0.25])
                else:
                    action = 1

                actions.append(action)
                if action == 0:
                    coinToss = simulator.flip()
                    states.append((simulator.numHeads, simulator.numTails))
                    prior = bayesianUpdate(prior, coinToss, np.array([0.5,0.75]))
                    turns += 1
                else:
                    maxIndex = np.argmax(prior)
                    if maxIndex == 0:
                        choice = "fair"
                    else:
                        choice = "cheater"
                    outcome = simulator.choose(choice)
                    reward = 15 if outcome is True else -30
                    reward -= turns
                    for k in range(len(states)):
                        key = (states[k], actions[k])
                        if key in qTable:
                            qTable[key] += reward
                            visits[key] += 1
                        else:
                            qTable[key] = reward
                            visits[key] = 1
                    prior = np.ones(2) * 0.5
                    states = [(0,0)]
                    actions = []
                    turns = 0
            
            maxScore = max(maxScore, simulator.score)
            if i % 100 == 0:
                print("Max Score:", maxScore)

        print(maxScore)


        for key in visits:
            qTable[key] = qTable[key] / visits[key]
        
        for x in range(10):
            for y in range(10):
                key1 = ((x,y), 1)
                key2 = ((x,y), 0)
                if key2 in qTable:
                    probFair = probSequence((x,y))
                    probCheat = 1 - probFair
                    probHeads = 0.5 * probFair + 0.75 * probCheat
                    probTails = 1 - probHeads
                    if ((x,y+1),1) in qTable and ((x+1,y),1) in qTable and ((x,y+1),0) in qTable and ((x+1,y),0) in qTable:
                        qTable[key2] = max(qTable[((x,y+1),1)], qTable[((x,y+1),0)]) * probTails + max(qTable[((x+1,y),1)], qTable[((x+1,y),0)]) * probHeads
                if key1 in qTable or key2 in qTable:
                    if key1 in qTable and key2 in qTable:
                        bestAction = 1 if qTable[key1] > qTable[key2] else 0
                    elif key1 in qTable:
                        bestAction = 1
                    else:
                        bestAction = 0
                    stateActionMap[(x,y)] = bestAction

        print(stateActionMap)

    w = csv.writer(open("output.csv", "w"))
    for key, val in stateActionMap.items():
        w.writerow([key, val])

main()