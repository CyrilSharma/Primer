import csv
import cv2
import mss
import numpy as np
import constants as c
from ast import literal_eval

def loadFromFile():
    with open('output.csv', mode='r') as infile:
        reader = csv.reader(infile)
        mydict = {literal_eval(rows[0]):int(rows[1]) for rows in reader}
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

def determineEquality(img1, img2, cutoff=12000):
    diff = img1 - img2
    diff = np.absolute(diff)
    diff = np.sum(diff, axis=None)
    if diff < cutoff:
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
        return None
    elif matchIndex == 1:
        return 0
    else:
        return matchIndex - 1

def bayesianUpdate(prior, coinToss, biasRange):
    if coinToss == 1:
        likelihood = biasRange
    else:
        likelihood = 1 - biasRange

    evidence = np.sum(likelihood * prior)
    
    # bayes rule
    posterior = likelihood * prior / evidence
    return posterior

def changeToGrayScale(array):
    # if pixel is not white, change to black
    # if pixel is white, change to white
    new_array = np.zeros(array.shape[0:2])
    for i in range(len(array)):
        for j in range(len(array[i])):
            if array[i][j][0] < 240 or array[i][j][1] < 240 or array[i][j][2] < 240:
                new_array[i][j] = 0
            else:
                new_array[i][j] = 255
    return new_array

def grabScreen(topLeft, width, height):
    with mss.mss() as sct:
        monitor = {'top': topLeft[1], 'left': topLeft[0], 'width': width, 'height': height}
        raw_img = sct.grab(monitor)
        img = np.array(raw_img)
        rgb = np.delete(img, 3, axis=2)
        img = changeToGrayScale(rgb)
    return img

def display(img):
    while True:
        cv2.imshow('img', img)
        if cv2.waitKey(0):
            cv2.destroyAllWindows()

if __name__ == "__main__":
    # loadFromFile()
    img = grabScreen(c.scorePosition, 45, 20)
    display(img)