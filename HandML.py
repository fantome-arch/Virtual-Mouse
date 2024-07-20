import cv2 as cv
import mediapipe as mp
import time
import math as mt

class handdetector():
    def __init__(self,mode=False,maxhands=2,detectionconfidence=0.5,trackconfidence=0.5,modelcomplexity=1):
        self.mode=mode
        self.maxhands=maxhands
        self.detectionconfidence=detectionconfidence
        self.trackconfidence=trackconfidence
        self.modelcomplexity=modelcomplexity
        self.mhands = mp.solutions.hands
        self.hands = self.mhands.Hands(self.mode,self.maxhands,self.modelcomplexity,self.detectionconfidence,self.trackconfidence)
        self.mpdraw = mp.solutions.drawing_utils
        self.tipids=[4,8,12,16,20]


    def findhands(self,frame,draw=True):
        rgbimg = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(rgbimg)
        # print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for handland in self.results.multi_hand_landmarks:
                if draw:
                    self.mpdraw.draw_landmarks(frame, handland, self.mhands.HAND_CONNECTIONS)

        return frame
    def findpos(self,img,handno=0,draw=False):
        global currenthand

        self.Landmarks=[]

        if self.results.multi_hand_landmarks:
            currenthand=self.results.multi_hand_landmarks[handno]
            for id, lm in enumerate(currenthand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                self.Landmarks.append([id,cx,cy])
                if draw:
                    cv.circle(img,(cx,cy),20,(0,0,255))





        return self.Landmarks

    def fingersup(self):
        fingers = []
        # Thumb
        if len(self.Landmarks)>0:
            if self.Landmarks[self.tipids[0]][1] > self.Landmarks[self.tipids[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            # Fingers
            for id in range(1, 5):
                if self.Landmarks[self.tipids[id]][2] < self.Landmarks[self.tipids[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            return fingers

    def calculate_angle(self,pt8x,pt8y,pt7x,pt7y,pt6x,pt6y):
        dist87=mt.sqrt((pt8x-pt7x)**2+(pt8y-pt7y)**2)
        dist76=mt.sqrt((pt7x-pt6x)**2+(pt7y-pt6y)**2)
        dist86=mt.sqrt((pt8x-pt6x)**2+(pt8y-pt6y)**2)
        rad=mt.acos((dist87**2+dist76**2-dist86**2)/(2*dist87*dist76))
        angle=mt.degrees(rad)
        return angle




















def main():
    cap = cv.VideoCapture(0)
    ptime = 0
    ctime = 0
    detector=handdetector(maxhands=1)
    while True:
        succ, frame = cap.read()
        #frame = cv.resize(frame, (1920, 1080))
        img=detector.findhands(frame,True)
        list=detector.findpos(frame)
        pt8x,pt8y=list[8][1],list[8][2]
        pt7x,pt7y=list[7][1],list[7][2]
        pt6x,pt6y=list[6][1],list[6][2]
        ang=detector.calculate_angle(pt8x,pt8y,pt7x,pt7y,pt6x,pt6y)
        print(ang)
        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime
        cv.putText(img, str(int(fps)), (10, 70), cv.FONT_HERSHEY_PLAIN, 3, (0, 255, 255))

        cv.imshow('image', frame)
        fing=detector.fingersup()


        c = cv.waitKey(1)
        if c == 27:
            break


if __name__=="__main__":
    main()
