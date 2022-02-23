import cv2
import numpy as np
import handtrackingmodule as htm
import time
import pyautogui

#########################
wCam, hCam = 1080, 720
frameR = 200 # 프레임 줄임
smoothening = 1.3
#########################

pTime = 0
plocX, plocY = 0,0
clocX, clocY = 0,0
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)
wScr, hScr = pyautogui.size()
print(wScr, hScr)

while True:
    # 1. 핸드 랜드마크를 찾음 
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    # 2. 핸드 랜드마크를 찾음 
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        # print(x1, y1, x2, y2)
        # 3. 어느 손가락이 위로 올라가는지 확인
        fingers = detector.fingersUp()
        #print(fingers)
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                      (255, 0, 255), 2)
        # 4. 검지 손가락만 이동 모드
        if fingers[1]==1 and fingers[2]==0:

            # 5. 좌표를 변환

            x3 = np.interp(x1, (frameR, wCam-frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScr))
            # 6. 값을 평활함
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
            # 7. 마우스 옮김
            pyautogui.moveTo(clocX, clocY) #좌우반전 wScr-x3
            cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY

        # 8. 검지와 가운뎃손가락이 모두 위로 향함 : 클릭 모드
        if fingers[1] == 1 and fingers[2] ==1:
            # 9. Find distance between fingers
            length, img, lineInfo = detector.findDistance(8, 12, img)
            print(length)
            # 10. 거리가 짧으면 마우스를 클릭함
            if length < 20:
                cv2.circle(img, (lineInfo[4], lineInfo[5]),
                           15, (0, 255, 0), cv2.FILLED)
                pyautogui.click()



    # 11. 프레임률
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                (255,0,0),3)
    
    # 12. 디스플레이
    cv2.imshow("가상 마우스", img)
    cv2.waitKey(1)
