import csv
import numpy as np
from ast import literal_eval

def loadFromFile():
    with open('output.csv', mode='r') as infile:
        reader = csv.reader(infile)
        mydict = {literal_eval(rows[0]):int(rows[1]) for rows in reader}
        # print(mydict)
    # tablePrint(mydict)
    return mydict

def probSequence(state):
    probFair = 0.5 ** (state[0] + state[1]) / (0.5 ** (state[0] + state[1]) + (0.75 ** state[0] * 0.25 ** state[1]))
    return probFair

def tablePrint(table):
    # add title and labels
    print("  ", end="")
    for T in range(15):
        strT = "{:02d}".format(T)
        print(f"{strT}", end=" ")
    print("")

    # print stateActionMap in table format
    for H in range(15):
        strH = "{:02d}".format(H)
        print(f"{strH}", end=" ")
        for T in range(15):
            print(f"{table[(H,T)]}  ", end="")
        print()

def bayesianUpdate(prior, coinToss, biasRange):
    if coinToss == 1:
        likelihood = biasRange
    else:
        likelihood = 1 - biasRange

    evidence = np.sum(likelihood * prior)
    
    # bayes rule
    posterior = likelihood * prior / evidence
    return posterior

loadFromFile()