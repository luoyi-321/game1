import cv2
import numpy as np 
import time

from ObjectDD import ObjectDD
from process import *
#----------- avairable 
ScreenWidth,ScreenHieght = 1080,760

# ----------------class

class sideWall:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def draw(self,image):
        pts = np.array([[0,0],[self.x,0]])
        cv2.fillPoly(image,pts)
        return image       

class scoreDash:
    def __init__(self,x1,x2,y1,y2,text:str):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.text = text
        
    def draw(self,image):
        circleRadius = int((self.y2-self.y1)/2)
        circleCenter = int((self.y2+self.y1)/2)
        cv2.rectangle(image,(self.x1,self.y1),(self.x2,self.y2),(0,136,255),-1)
        cv2.circle(image,(self.x1,circleCenter),circleRadius,(0,136,255),-1)
        cv2.circle(image,(self.x2,circleCenter),circleRadius,(0,136,255),-1)
        cv2.putText(image,self.text,(self.x1+10,circleCenter),cv2.FONT_HERSHEY_COMPLEX,0.6,(255,255,255))
        return image


Image_DIR = 'avoidObstacles/pic'
resource_DIR = 'avoidObstacles/resource'
ObjectPos = (int(ScreenWidth/4),0)
score = 0
timeSet = 10
num = 4
timeTodicided = 50
dicided = False
size = 0.5

Run = True
resource = ('Coin.png','Player1.png','Player2.png')

# ----------------prepare object
coinWidth,coinHeight = 150,150
coin_img = cv2.imread(f'{resource_DIR}/{resource[0]}',cv2.IMREAD_UNCHANGED)
coin_img = cv2.resize(coin_img,(int(coinWidth*0.5 ),int(coinHeight*0.5)))
IMAGE = [coin_img]
coin  = ObjectDD(IMAGE,(int(ScreenWidth/2),0),'Coin.png',coinWidth,coinHeight)
scoreDB = scoreDash(50,150,50,100,f"Score: {score}")

currentObject = ObjectReset()
isNotdicide = True
processOne_State = True
processTwo_State = True

while Run:          
    coinWidth,coinHeight = 150,150
    coin_img = cv2.imread(f'{resource_DIR}/{resource[0]}',cv2.IMREAD_UNCHANGED)
    coin_img = cv2.resize(coin_img,(int(coinWidth*0.5),int(coinHeight*0.5)))
    imgPos = (0,0)
    coin_img = (coin_img,imgPos)
    IMAGE = [coin_img]
    coin  = ObjectDD(IMAGE,(int(ScreenWidth/2),0),'Coin.png',coinWidth,coinHeight)

    currentObject = ObjectReset()
    image  =  np.zeros((ScreenHieght,ScreenWidth,3),dtype=np.uint8)
    currentObject = proCessOne(processOne_State,currentObject,coin,scoreDB,ScreenHieght,ScreenWidth)
    # print(currentObject.position,currentObject.Name)
    currentObject,score = processTwo(processOne_State,currentObject,coin,scoreDB,ScreenHieght,ScreenWidth,score)
   

