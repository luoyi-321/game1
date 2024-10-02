import numpy as np
import cv2


width ,height = 760,560
class Box:
    def __init__(self,x,y,w,h):
        self.x = x
        self.y = y
        self.w = w+x
        self.h = h+y
        self.color = (50,50,50)
    def draw(self,image):
        image = cv2.rectangle(image,(self.x,self.y),(self.w,self.h),self.color,-1)
        return image
    def move(self,p1,p2):
        if self.x < p1 and self.y > p2:
            if p1 < p2:
                pass
            else:
                pass
        elif self.x < p1 and self.y < p2:
            if p1 < p2:
                pass
            else:
                pass
        elif self.x > p1 and self.y < p2: 
            if p1 < p2:
                pass
            else:
                pass 
        elif self.x > p1 and self.y > p2:
            if p1 < p2:
                pass
            else:
                pass 
        
def GameStart(state):
    timeSet  = 10
    box = Box(200,50,100,150)
    while state:
        image = np.zeros((height,width,3),dtype=np.uint8)
        if timeSet == 50:
            if box.h <= height:
                print(box.h)
                box.x = box.x - 1
                box.y = box.y + 2
                box.w = box.w -1
                box.h = box.h +2
                timeSet = 10
                if box.x < 0 :
                    box.x = 1
        timeSet += 1
        image = box.draw(image)
        cv2.imshow("image",image)
        cv2.waitKey(1)


if __name__ == '__main__':
    GameStart(True)