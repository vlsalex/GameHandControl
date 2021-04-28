import cv2
import time
import HandTrackingModule as htm
import math
import keyboard


def getForwardK(lmList):
    y = (lmList[8][1] + lmList[12][1] + lmList[16][1] + lmList[20][1]) // 4
    x = (lmList[8][2] + lmList[12][2] + lmList[16][2] + lmList[20][2]) // 4
    cv2.circle(img, (y, x), 5, (255, 0, 0), -1)

    hansDistance1 = distanceCalculate(lmList[0][1], lmList[0][2], y, x)
    hansDistance2 = distanceCalculate(lmList[0][1], lmList[0][2], lmList[5][1], lmList[5][2])

    return hansDistance1 / hansDistance2


def getHorizontalK(lmList, width):
    return lmList[0][1] / width - 0.5


def distanceCalculate(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))


dirs = {
    'forward': 0,
    'left': 0,
    'right': 0
}

pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)
detector = htm.handDetector()
while True:
    success, img = cap.read()

    old_dirs = dirs.copy()

    dirs = {
        'forward': 0,
        'left': 0,
        'right': 0
    }

    img = detector.findHands(img, draw=True)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        if getForwardK(lmList) < 0.9:
            dirs['forward'] = 1
        horizontalK = getHorizontalK(lmList, len(img[0]))
        if horizontalK > 0.1:
            dirs['left'] = 1
        if horizontalK < -0.1:
            dirs['right'] = 1

    print("=================")
    print(dirs)
    print(old_dirs)
    print("=================")

    if dirs['forward'] != old_dirs['forward']:
        if dirs['forward'] == 1:
            keyboard.press("w")
            print("press")
        else:
            keyboard.release("w")

    if dirs['left'] != old_dirs['left']:
        if dirs['left'] == 1:
            keyboard.press("a")
        else:
            keyboard.release("a")

    if dirs['right'] != old_dirs['right']:
        if dirs['right'] == 1:
            keyboard.press("d")
        else:
            keyboard.release("d")

    cv2.imshow("Image", img)

    if cv2.waitKey(1) == ord('q'):
        break