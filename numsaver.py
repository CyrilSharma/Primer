import cv2
import mss
import numpy as np
from utils import changeToGrayScale

def loadNums(display=False):
    with open('nums.npy', 'rb') as f:
        digitArray = np.load(f)
    
    if display:
        index = 0
        while index < len(digitArray):
            img = digitArray[index]
            cv2.imshow('OpenCV/Numpy normal', img)
            cv2.setWindowProperty('OpenCV/Numpy normal', cv2.WND_PROP_TOPMOST, 1)
            cv2.waitKey(25)
            input("Press Enter to proceed -> ")
            cv2.destroyAllWindows()
            index += 1

    return digitArray

def testNums():
    with open('nums.npy', 'rb') as f:
        digitArray = np.load(f)
    
    with mss.mss() as sct:
        # Part of the screen to capture
        monitor = {'top': 436, 'left': 802, 'width': 30, 'height': 20}
        # monitor = {'top': 436, 'left': 802, 'width': 5, 'height': 5}
        screenCapturing = True

        while screenCapturing:
            input("Press Enter to select a new digit -> ")
            # Get raw pixels from the screen, save it to a Numpy array
            raw_img = sct.grab(monitor)
            img = np.array(raw_img)

            rgb = np.delete(img, 3, axis=2)
            img = changeToGrayScale(rgb)

            # Display the picture
            cv2.imshow('OpenCV/Numpy normal', img)
            cv2.setWindowProperty('OpenCV/Numpy normal', cv2.WND_PROP_TOPMOST, 1)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

            user_string = input("Press enter to continue, and q to quit: ")
            if user_string.lower() == "q":
                screenCapturing = False
                cv2.destroyAllWindows()
            if inNumpyList(img, digitArray):
                print("Image is in the array!")
            else:
                print("Image is not in the array!")

def saveNums():
    # button = Button.left
    # delay = 0.001
    # mouse = Controller()
    # mouse.position = (662, 707)
    with mss.mss() as sct:
        # Part of the screen to capture
        monitor = {'top': 436, 'left': 802, 'width': 30, 'height': 20}
        # monitor = {'top': 436, 'left': 802, 'width': 5, 'height': 5}
        digitArray = []
        screenCapturing = True

        while screenCapturing:
            input("Press Enter to select a new digit -> ")
            # mouse.click(button)
            # Get raw pixels from the screen, save it to a Numpy array
            raw_img = sct.grab(monitor)
            img = np.array(raw_img)

            rgb = np.delete(img, 3, axis=2)
            img = changeToGrayScale(rgb)

            # Display the picture
            cv2.imshow('OpenCV/Numpy normal', img)
            cv2.setWindowProperty('OpenCV/Numpy normal', cv2.WND_PROP_TOPMOST, 1)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

            user_string = input("Press S to skip, C to continue, and Q to quit: ")
            if user_string.lower() == "c":
                digitArray.append(img)
            elif user_string.lower() == "q":
                screenCapturing = False
                cv2.destroyAllWindows()
        digitArray = np.stack(digitArray)
        with open('nums.npy', 'wb') as f:
            np.save(f, digitArray)

def inNumpyList(arr, list):
    for i in range(len(list)):
        if np.array_equal(arr, list[i]):
            return True
    return False

if __name__ == "__main__":
    """ saveNums()
    loadNums(True)
    testNums() """

    cv2.imshow()