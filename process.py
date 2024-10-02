import numpy as np
import cv2
import math
import os
import cvzone
import random
import time

from poseDectection import detectPose
from ObjectDD import ObjectDD,CoverageLine,IMage

ScreenWidth,ScreenHieght = 1080,760
Image_DIR = 'avoidObstacles/pic'
resource_DIR = 'avoidObstacles/resource'
ObjectPos = (int(ScreenWidth/4),0)
print(ObjectPos)
ObjectName : str
score = 0
timeSet = 10
num = 4
timeTodicided = 50
dicided = False
size = 0.5
coinWidth,coinHeight = 150,150

Run = True
resource = ('Coin.png','Player1.png','Player2.png')

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, ScreenWidth)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, ScreenHieght)


     
def drawobject(image,Object):
    if Object.status:
        for img in Object.img:
            image = cvzone.overlayPNG(image,img,Object.img.pos)
    else:
        return image
    return image 

def distance(pointOne:list,pointTwo:list):
    return math.dist(pointOne,pointTwo)

def ObjectSet():
    OBJECT_NAME = ['RsideHalfObject.png','LsideHalfObject.png','UpObject.png','MidObject.png']
    ObjectList = []
    for i in range(len(OBJECT_NAME)):
        object_name = OBJECT_NAME[i]
        if object_name == 'UpObject.png':
            img1 = cv2.imread(f'{Image_DIR}/right.png',cv2.IMREAD_UNCHANGED)
            IMGheight1,IMGwidth1,_ = img1.shape
            img1 = cv2.resize(img1,(int(IMGwidth1*0.25),int(IMGheight1*0.25)))
            # imgPos = (270,0)
            # img1 = IMage(img1,imgPos)

            img2 = cv2.imread(f'{Image_DIR}/left.png',cv2.IMREAD_UNCHANGED)
            IMGheight2,IMGwidth2,_ = img2.shape
            img2 = cv2.resize(img2,(int(IMGwidth2*0.25),int(IMGheight2*0.25)))
            # imgPos = (0,0)
            # img2 = IMage(img2,imgPos)

            img3 = cv2.imread(f'{Image_DIR}/up.png',cv2.IMREAD_UNCHANGED)
            IMGheight3,IMGwidth3,_ = img3.shape
            img3 = cv2.resize(img3,(int(IMGwidth3*0.25),int(IMGheight3*0.25)))
            # imgPos = (250,0)
            # img3 = IMage(img3,imgPos)
            IMAGE = [img1,img2,img3]

            objectDD = ObjectDD(IMAGE,ObjectPos,object_name,IMGwidth1,IMGheight1)
            ObjectList.append(objectDD)
        elif object_name == 'MidObject.png':
            img1 = cv2.imread(f'{Image_DIR}/right.png',cv2.IMREAD_UNCHANGED)
            IMGheight1,IMGwidth1,_ = img1.shape
            img1 = cv2.resize(img2,(int(IMGwidth1*0.25),int(IMGheight1*0.25)))
            # imgPos = (0,0)
            # img1 = IMage(img1,imgPos)

            img2 = cv2.imread(f'{Image_DIR}/left.png',cv2.IMREAD_UNCHANGED)
            IMGheight2,IMGwidth2,_ = img2.shape
            img2 = cv2.resize(img2,(int(IMGwidth2*0.25),int(IMGheight2*0.25)))
            # imgPos = (250,0)
            # img2 = IMage(img2,imgPos)
            IMAGE = [img1,img2]
            objectDD = ObjectDD(IMAGE,ObjectPos,object_name,IMGwidth1,IMGheight1)
            ObjectList.append(objectDD)
        else:
            img = cv2.imread(f'{Image_DIR}/{object_name}',cv2.IMREAD_UNCHANGED)
            IMGheight,IMGwidth,_ = img.shape
            img = cv2.resize(img,(int(IMGwidth*0.25),int(IMGheight*0.25)))
            # imgPos = (0,0)
            # img = IMage(img,imgPos)
            IMAGE = [img]
            objectDD = ObjectDD(IMAGE,ObjectPos,object_name,IMGwidth,IMGheight)
            ObjectList.append(objectDD)
        
    return ObjectList

def ObjectReset():
    ObjectsList = ObjectSet()
    currentObject  = ObjectsList[random.randint(0,len(ObjectsList)-1)]
    return currentObject

def draw_fool(image,PTS,color):
    PTS = np.array(PTS)
    image  = cv2.fillPoly(image,pts= [PTS],color = color)
    return image
def drawsideWall(currentIamgePos,currentImageHeight,image):
    pts  = np.array([[0,0] ,currentIamgePos ,[currentIamgePos[0],currentImageHeight], [0,ScreenHieght]])
    cv2.fillPoly(image,pts= [pts],color = (160,140,140))
    return image
def drawsideWallLeft(currentIamgePos,currentImageHeight,image):
    pts  = np.array([currentIamgePos ,[ScreenWidth,0] ,[ScreenWidth,ScreenHieght], [currentIamgePos[0],currentImageHeight]])
    cv2.fillPoly(image,pts= [pts],color = (160,140,140))
    return image

def proCessOne (processOne_State,currentObject,coin,scoreDB,ScreenHieght,ScreenWidth,timeSet = 10):
    while processOne_State:
        _ , frame = cap.read()
        frame = cv2.flip(frame,1 )
        # image  =  np.zeros((ScreenHieght,ScreenWidth,3),dtype=np.uint8)
        image = cv2.imread('avoidObstacles/resource/BG.jpeg')
        image = cv2.resize(image,(ScreenWidth,ScreenHieght))
        if currentObject.Name == 'LsideHalfObject.png':
            coin.position = (int(ScreenWidth*0.66),coin.position[1])
            coin.status = True
        elif currentObject.Name == 'RsideHalfObject.png':
            coin.position = (int(ScreenWidth*0.33),coin.position[1])
            coin.status = True
        else:
            coin.position = (int(ScreenWidth/2),0)
            coin.status = False
        # image  = cv2.rectangle(image,(0,0),(ScreenWidth,ScreenHieght),(155,155,155),-1)
        # image = drawsideWall((270,0),280,image)
        # image = drawsideWallLeft((590,0),280,image)
        # image = draw_fool(image,[[0,ScreenHieght],[270,280],[590,280],[ScreenWidth,ScreenHieght]],(90,90,90))
        # image = drawobject(image,currentObject) # draw an Object
        # image = drawobject(image,coin)  # draw a Coin 
        image = scoreDB.draw(image)    #draw a dashBord
        image,headPos = detectPose(frame,image,draw=True) 
        timeSet += 1
        if timeSet == 30:
            currentObject = ObjectReset()
            timeSet = 10
        # print(currentObject.Name)
        cv2.imshow("image",image)
        k = cv2.waitKey(1) & 0xFF
        if ( k == ord('k')):
            return currentObject
        cv2.waitKey(1)
def processTwo(processTwo_State,currentObject,coin,scoreDB,ScreenHieght,ScreenWidth,score, timeSet = 10, ObjectSize = 0.5 ,numOfsize = 4):
    
    while processTwo_State:
        _ , frame = cap.read()
        frame = cv2.flip(frame,1 )
        image  =  np.zeros((ScreenHieght,ScreenWidth,3),dtype=np.uint8)
        if currentObject.Name == 'LsideHalfObject.png':
            currentObject.CoverageLine = CoverageLine((215),(0))
            coin.position = (int(ScreenWidth*0.66),coin.position[1])
            coin.status = True
        elif currentObject.Name == 'RsideHalfObject.png':
            currentObject.CoverageLine = CoverageLine((555),(0))
            coin.position = (int(ScreenWidth*0.33),coin.position[1])
            coin.status = True
        else:
            currentObject.CoverageLine = CoverageLine((215,255),(270))
            coin.position = (int(ScreenWidth/2),0)
            coin.status = False
        # image  = cv2.rectangle(image,(0,0),(ScreenWidth,ScreenHieght),(155,155,155),-1)
        # image = drawsideWall((270,0),280,image)
        # image = drawsideWallLeft((590,0),280,image)
        # image = draw_fool(image,[[0,ScreenHieght],[270,280],[590,280],[ScreenWidth,ScreenHieght]],(90,90,90))
        
        image = drawobject(image,currentObject) # draw an Object
        image = drawobject(image,coin)  # draw a Coin 
        image = scoreDB.draw(image)    #draw a dashBord
        image,headPos = detectPose(frame,image,draw=True) 
        
        timeSet += 1
        if timeSet == 30:
            if numOfsize <= 128:
                numOfsize = numOfsize*2
            if ObjectSize < 2 :
                ObjectSize = ObjectSize+0.1
            else:
                return currentObject,score
            timeSet = 10
        coin.img = cv2.resize(coin.img,(int(coinWidth*ObjectSize),int(coinHeight*ObjectSize)))
        currentObject.position  = (int(ScreenWidth/numOfsize),0)
        currentObject.img = cv2.resize(currentObject.img,(int(currentObject.width*ObjectSize),int(currentObject.height*ObjectSize)))
        # print(currentObject.Name)
        cv2.imshow("image",image)
        # print(ObjectSize)
        if ObjectSize >= 1 and ObjectSize < 1.6:
            coinCenter = (coin.position[0]+coinWidth,coin.position[1]+coinHeight)
            headCoinDistance = distance(headPos,coinCenter)
            print(headCoinDistance)
            if headCoinDistance <= 60:
                coin.status = False 
                coin.position = (ScreenWidth,ScreenHieght)
                print(score)
                score += 1
                scoreDB.text = f'score : {score}'
                return currentObject,score
        k = cv2.waitKey(1) & 0xFF
        if ( k == ord('k')):
            return currentObject,score
            break
        cv2.waitKey(1)
