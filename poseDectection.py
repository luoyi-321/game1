
import matplotlib.pyplot as plt
import mediapipe as mp
from draw import drawBody,drawHand,drawhead,drawLeg,drawheadBypic
import cv2
import math

mp_pose = mp.solutions.pose
pose_video = mp_pose.Pose(static_image_mode = False, model_complexity = 1,min_detection_confidence=0.7)

def getcoordimate(obj,image):
    x = int(obj.x * image[0])
    y = int(obj.y * image[1])
    return x, y
def distance(pointOne:list,pointTwo:list):
    return math.dist(pointOne,pointTwo)
def CenterOffPoint (pointOne:list,pointTwo:list):
    return (int((pointOne[0]+pointTwo[0])/2),int((pointOne[1]+pointTwo[1])/2))

def detectPose(image,output_image, pose = pose_video, draw=False, display=False,headPosition =[0,0]):
    height,width,_ = image.shape
    neckShift = 40
    
    output_image = output_image
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(imageRGB)
    if results.pose_landmarks and draw:
        nose = results.pose_landmarks.landmark[0]
        noseCenter = (getcoordimate(nose,(width,height)))
        # print(noseCenter)
        
        Lshoulder = (getcoordimate(results.pose_landmarks.landmark[11],(width,height)))
        Rshoulder = (getcoordimate(results.pose_landmarks.landmark[12],(width,height)))
        Rshoulder = [Rshoulder[0],Rshoulder[1]+neckShift]
        Lshoulder = [Lshoulder[0],Lshoulder[1]+neckShift]
        Rwrit = (getcoordimate(results.pose_landmarks.landmark[16],(width,height)))
        Lwrit = (getcoordimate(results.pose_landmarks.landmark[15],(width,height)))
        Relbow = (getcoordimate(results.pose_landmarks.landmark[14],(width,height)))
        Lelbow = (getcoordimate(results.pose_landmarks.landmark[13],(width,height)))
        hipShift = 40
        Lhip = (getcoordimate(results.pose_landmarks.landmark[23],(width,height)))
        Lhip = (Lhip[0],Lhip[1]-hipShift)
        Rhip= (getcoordimate(results.pose_landmarks.landmark[24],(width,height)))
        Rhip = (Rhip[0],Rhip[1]-hipShift)

        # print(Lshoulder)
        Lknee = (getcoordimate(results.pose_landmarks.landmark[25],(width,height)))
        Rknee = (getcoordimate(results.pose_landmarks.landmark[26],(width,height)))
        
        Lankle = (getcoordimate(results.pose_landmarks.landmark[27],(width,height)))
        Rankle = (getcoordimate(results.pose_landmarks.landmark[28],(width,height)))
        # leftEye = results.pose_landmarks.landmark[2]
        # rightEye = results.pose_landmarks.landmark[5]
        leftEre = (getcoordimate(results.pose_landmarks.landmark[7],(width,height)))
        rightEre = (getcoordimate(results.pose_landmarks.landmark[8],(width,height)))
        
        bodyCenter = CenterOffPoint(Lshoulder,Rshoulder)
        hipCenter = CenterOffPoint(Lhip,Rhip)
        # facesize1 = int((leftEre.x*width)-((nose.x*width)))
        facesize= int(distance(noseCenter,bodyCenter)/3)
        # if facesize+20 < facesize1:
        #     facesize=facesize1
        if facesize <= 0 :
            facesize = 10
        # print(facesize)
        headPosition = (noseCenter[0]+facesize,noseCenter[1]+facesize)
        # hair
        neckWidth = int((facesize/2)+(facesize/2))
        drawLeg(output_image,Lhip,Rhip,Rknee,Lknee,Rankle,Lankle,hipCenter,neckWidth)
        output_image= drawBody(Lshoulder,Rshoulder,Lhip,Rhip,facesize,output_image)
        # drawhead(noseCenter,output_image,facesize,bodyCenter)
        drawHand(output_image,Rwrit,Lwrit,Relbow,Lelbow,Rshoulder,Lshoulder,neckWidth)
        drawheadBypic(noseCenter,output_image,facesize,bodyCenter)
    if display:
        plt.figure(figsize=[22,22])
        plt.subplot(121);plt.imshow(image[:,:,::-1]);plt.title('Original Image');plt.axis('off')
        plt.subplot(122);plt.imshow(output_image[:,:,::-1]);plt.title('Output Image');plt.axis('off')
    else:
        return output_image,headPosition
    
