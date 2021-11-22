import time
from cv2 import cv2
import hand_tracking_module as htm
import numpy as np
import pyautogui as pag

wscr, hscr = 1366, 768
redframe = 100
smooth = 5
plocx, plocy = 0, 0
clocx, clocy = 0, 0

cap = cv2.VideoCapture(0)
wcam, hcam = 800, 600
cap.set(3, wcam)
cap.set(4, hcam)

pTime = 0
detector = htm.handDetector()

while True:
    suc, vid = cap.read()

    #detecting hands and position
    vid = detector.findHands(vid)
    lmlist = detector.findPosition(vid)

    #detecting index and middle finger
    if len(lmlist) != 0:
        x1, y1 = lmlist[8][1:]
        x2, y2 = lmlist[12][1:]

        #if fingers are up
        fingers = detector.fingersUp()
        cv2.rectangle(vid, (redframe, redframe), (wcam - redframe, hcam - redframe), (0, 0, 255), 2)
        # index finger = moving mode
        if fingers[1] == 1 and fingers[2] == 0:
            x3 = np.interp(x1, (redframe, wcam - redframe), (0, wscr))
            y3 = np.interp(y1, (redframe, hcam - redframe), (0, hscr))

            #smoothening it up
            clocx = plocx + (x3 - plocx) / smooth
            clocy = plocy + (y3 - plocy) / smooth

            #moving mouse
            pag.moveTo(wscr - clocx, clocy)
            cv2.circle(vid, (x1, y1), 15, (0, 0, 0), cv2.FILLED)
            plocx, plocy = clocx, clocy

            #for clicking
        if fingers[1] == 1 and fingers[2] == 1:
            length, img, lineInfo = detector.findDistance(8, 12, vid)
            print(length)
            if length < 35:
                cv2.circle(vid, (x1, y1), 15, (0, 255, 255), cv2.FILLED)
                cv2.circle(vid, (x2, y2 ), 15, (0, 255, 255), cv2.FILLED)
                cv2.circle(vid, (lineInfo[4], lineInfo[5]), 15, (0, 255, 255), cv2.FILLED)
                #clicking
                pag.click()

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(vid, f'FPS:{int(fps)}', (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
    cv2.imshow('VIDEO', vid)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
