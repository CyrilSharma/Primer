import pprint
import csv

from utils import probSequence, tablePrint

def main():
    netValues = {}
    for H in range(16):
        for T in range(16):
            probFair = probSequence([H, T])
            probCheat = 1 - probFair
            probCorrectGuess = max(probFair, probCheat)
            probIncorrectGuess = 1 - probCorrectGuess
            expectedValue = probCorrectGuess * 15 + probIncorrectGuess * -30
            netValues[(H, T)] = expectedValue - (H + T)
            # print(f"H: {H}, T: {T}, netValue: {expectedValue - (H + T)}")
    
    trueValue = {}
    stateActionMap = {}
    completedNodes = set()
    
    completedNodes.add((15, 15))
    trueValue[(H, T)] = netValues[(H, T)]

    H = 15
    for T in range(14, -1, -1):
        trueValue[(H,T)] = max(netValues[(H, T)], trueValue[(H, T+1)])
        completedNodes.add((H, T))
    
    T = 15
    for H in range(14, -1, -1):
        trueValue[(H,T)] = max(netValues[(H, T)], trueValue[(H+1, T)])
        completedNodes.add((H, T))
    

    for H in range(14,-1,-1):
        for T in range(14,-1,-1):
            probFair = probSequence([H, T])
            probCheat = 1 - probFair
            probCorrectGuess = max(probFair, probCheat)
            probIncorrectGuess = 1 - probCorrectGuess
            probHeads = 0.5 * probFair + 0.75 * probCheat
            probTails = 1 - probHeads
            trueValue[(H,T)] = max(netValues[(H,T)], netValues[(H,T+1)] * probTails + netValues[(H+1,T)] * probHeads)
            stateActionMap[(H,T)] = 1 if netValues[(H,T)] > netValues[(H,T+1)] * probTails + netValues[(H+1,T)] * probHeads else 0
    
    pprint.pprint(trueValue)
    pprint.pprint(stateActionMap)
    tablePrint(stateActionMap)
    
    w = csv.writer(open("output1.csv", "w"))
    for key, val in stateActionMap.items():
        w.writerow([key, val])

if __name__ == "__main__":
    main()
