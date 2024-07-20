import cv2 as cv
import HandML as hm


import numpy as np
import time
import pyautogui


pyautogui.PAUSE=0




detector=hm.handdetector(maxhands=1,detectionconfidence=0.5,trackconfidence=0.3,modelcomplexity=1)
cap=cv.VideoCapture(0)
ptime=0
hcam,wcam=480,640
wscr,hscr=pyautogui.size()
cap.set(3,wcam)
cap.set(4,hcam)
plocx,plocy=0,0
clocx,clocy=0,0
smooth=4.5
scrollmode=False
prev=0
fr1x,fr1y=200,100
fr2x,fr2y=wcam-200,hcam-200
clickstate=False
while True:
    ######################DETECTION AND READING#########
    suc,img=cap.read()
    img=cv.flip(img,1)
    detector.findhands(img)
    track=detector.findpos(img,draw=False)
    fingid=detector.fingersup()

    if len(track)>0:
        cv.rectangle(img,(fr1x,fr1y),(fr2x,fr2y),(255,0,0),2)
        cx,cy=int(track[8][1]),int(track[8][2])
        x1 = int(np.interp(cx, (fr1x, fr2x), (0, wscr-1)))
        y1 = int(np.interp(cy, (fr1y, fr2y), (0, hscr-1)))
        clocx=plocx+(x1-plocx)/smooth
        clocy=plocy+(y1-plocy)/smooth
        if fingid[4]==0 and fingid[3]==0:
            clickstate=True
        if fingid[1]==1 and fingid[2]==0 and fingid[4]==0:
            pyautogui.moveTo(clocx,clocy)
        if fingid[4]==1 and fingid[3]==0:
            if clickstate:
                pyautogui.click()
                clickstate=False
        if fingid[2]==1 and fingid[3]==0 and fingid[4]==0:
            pyautogui.rightClick()
        if fingid[0]==0 and fingid[1]==0 and fingid[2]==0 and fingid[3]==0 and fingid[4]==0:
            scrollmode=True
        if track[4][1]==track[8][1] and track[4][2]==track[8][2]:
            print('deez cock')
        else:
            scrollmode=False
        if scrollmode:
            cury=int(track[0][2])
            if cury-prev<-5:
                pyautogui.scroll(-40)
            if cury-prev>5:
                pyautogui.scroll(40)

            prev=cury


        plocx,plocy=clocx,clocy


    #Finalization############
    

    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime
    cv.putText(img, str(int(fps)), (10, 70), cv.FONT_HERSHEY_PLAIN, 3, (0, 255, 255))
    cv.imshow('img',img)
    c=cv.waitKey(1)
    if c==27:
        break







