import cv2
import numpy as np
import math
import cvzone


# color = {
#     'skincolor':(162,203,255),
#     'DskinColor':(120,152,188),
#     'hair':(109,109,109),
#     'hairRed':(100,100,109),
#     'black':(0,0,0),
#     'pinkyRed':(80,32,158),
#     'shirtBody':(181,179,131),
#     'Dshirtbody':(133,112,82),
#     'Dblue' : (86,61,36),
#     'white': (255,255,255)
    
# }
color = {
    'skincolor':(134,191,234),
    'DskinColor':(81,143,192),
    'hair':(109,109,109),
    'hairRed':(100,100,109),
    'black':(0,0,0),
    'pinkyRed':(80,32,158),
    'shirtBody':(33,174,236),
    'Dshirtbody':(0,127,212),
    'Dblue' : (86,61,36),
    'white': (255,255,255)
    
}


def azmiusAngel(pointOne,pointTwo):
    angle = 0.0
    x1,y1 = pointOne[0],pointOne[1]
    x2,y2 = pointTwo[0],pointTwo[1]
    
    dx = x2 -x1
    dy = y2 -y1
    if x2 == x1 :
        angle = math.pi/2.0
        if y2 == y1:
            angle = 0.0
        elif y2 < y1:
            angle = 3.0*math.pi/2.0
    elif x2 > x1 and y2 > y1 :
        angle = math.atan(dx/dy)
    elif x2 > x1 and y2 < y1 :
        angle = math.pi/2.0 + math.atan(-dy/dx)
    elif x2 < x1 and y2 < y1 :
        angle = math.pi +  math.atan(dx/dy)
    elif x2 < x1 and y2 > y1 :
        angle = 3.0*math.pi/2.0+ math.atan(dx/dy)
    
    return int(angle *180 /math.pi)

def drawheadBypic(center,image,faceSize,bodyCenter):
    headImage = cv2.imread('avoidObstacles/resource/head.png',cv2.IMREAD_UNCHANGED)
    imageWidth = imageHeight = int(faceSize*15)
    headImage = cv2.resize(headImage,(int(imageWidth*0.3),int(imageHeight*0.3)))
    neckWidht = int((faceSize/2)+(faceSize/2))
    neckStartpoint = (center[0]-int(faceSize/2),center[1]+int(faceSize/2))
    neckEndpoint = bodyCenter
    Center = (center[0]-int(imageWidth*0.3/2),center[1]-int(imageHeight*0.3/2))
    # print(Center)
    if int(faceSize/2) < 1 :
        faceSize = 4
    # ptss = np.array([neckStartpoint,[neckStartpoint[0]+neckWidht,neckStartpoint[1]],[bodyCenter[0]+int(neckWidht/2),bodyCenter[1]],[bodyCenter[0]-int(neckWidht/2),bodyCenter[1]]])
    # cv2.fillPoly(image,pts = [ptss],color=color['skincolor'])
    cv2.circle(image,neckEndpoint,int(faceSize/1.4),color['white'],-1)
    cv2.circle(image,neckEndpoint,int(faceSize/1.6),color['hair'],-1)
    cv2.line(image,center,neckEndpoint,color['skincolor'],neckWidht)
    ptss = np.array([neckStartpoint, [neckStartpoint[0]+neckWidht,neckStartpoint[1]], [bodyCenter[0]-int(neckWidht/2),bodyCenter[1]]])
    cv2.fillPoly(image,pts = [ptss],color = color['DskinColor'])

    image = cvzone.overlayPNG(image,headImage,Center)
    return image


def drawhead(center:list,image,faceSize:int,bodyCenter: list):
    # hair
    hairCenter = (center[0]-int(faceSize/2),center[1]-int(faceSize/1.5))
    if int(faceSize/2) < 1 :
        faceSize = 4
    cv2.circle(image,hairCenter,int(faceSize/1.6),color['hairRed'],-1)
    cv2.circle(image,(center[0]+int(faceSize/2),hairCenter[1]),int(faceSize/1.6),color['hairRed'],-1)
    cv2.ellipse(image,(center[0],hairCenter[1]),(faceSize,int(faceSize/2)),0,0,360,color['hairRed'],-1)
    # cv2.circle(image,(hairCenter[0]+int(faceSize/2),hairCenter[1]),int(faceSize),color['hair'],-1)
    
    
    # eres
    cv2.circle(image,(center[0]-faceSize,center[1]),int(faceSize/6),color['pinkyRed'],-1)
    cv2.circle(image,(center[0]+faceSize,center[1]),int(faceSize/6),color['pinkyRed'],-1)
    # neck
    neckWidht = int((faceSize/2)+(faceSize/2))
    neckStartpoint = (center[0]-int(faceSize/2),center[1]+int(faceSize/2))
    neckEndpoint = bodyCenter
    # ptss = np.array([neckStartpoint,[neckStartpoint[0]+neckWidht,neckStartpoint[1]],[bodyCenter[0]+int(neckWidht/2),bodyCenter[1]],[bodyCenter[0]-int(neckWidht/2),bodyCenter[1]]])
    # cv2.fillPoly(image,pts = [ptss],color=color['skincolor'])
    cv2.circle(image,neckEndpoint,int(faceSize/1.4),color['white'],-1)
    cv2.circle(image,neckEndpoint,int(faceSize/1.6),color['hair'],-1)
    cv2.line(image,center,neckEndpoint,color['skincolor'],neckWidht)
    
    # print("bodycenter",bodyCenter)
    ptss = np.array([neckStartpoint, [neckStartpoint[0]+neckWidht,neckStartpoint[1]], [bodyCenter[0]-int(neckWidht/2),bodyCenter[1]]])
    cv2.fillPoly(image,pts = [ptss],color = color['DskinColor'])
    # face
    cv2.circle(image,center,faceSize,color['skincolor'],-1)
    # eyes
    leftEye = (center[0]-int(faceSize/3),center[1]-int(faceSize/2))
    rightEye =(center[0]+int(faceSize/3),center[1]-int(faceSize/2))
    
    cv2.circle(image,leftEye,int(faceSize/6),color['black'],-1)
    cv2.circle(image,rightEye,int(faceSize/6),color['black'],-1)
    cv2.rectangle(image,(rightEye[0]-int(faceSize/5),rightEye[1]-int(faceSize/5)),(rightEye[0]+int(faceSize/6),rightEye[1]-int(faceSize/6)),color['black'],-1)
    cv2.rectangle(image,(leftEye[0]-int(faceSize/5),leftEye[1]-int(faceSize/5)),(leftEye[0]+int(faceSize/6),leftEye[1]-int(faceSize/6)),color['black'],-1)
    # nose
    pts = np.array([[center[0],center[1]-6],[center[0]-2,center[1]],[center[0],center[1]+2]])
    cv2.fillPoly(image,pts = [pts],color = color['black'])
    # # freshin
    Lfreshin = (center[0]-int(faceSize/3),center[1])
    Rfreshin = (center[0]+int(faceSize/3),center[1])
    
    cv2.ellipse(image,Lfreshin,(int(faceSize/6),int(faceSize/10)),0,0,360,color['pinkyRed'],-1)
    cv2.ellipse(image,Rfreshin,(int(faceSize/6),int(faceSize/10)),0,0,360,color['pinkyRed'],-1)
    
    # cv2.fillPoly(image,Lfreshin,int(faceSize/6),color['pinkyRed'],-1)
    # cv2.fillPoly(image,Rfreshin,int(faceSize/6),color['pinkyRed'],-1)
    
    # mouse
    contours = np.array([[center[0]-int(faceSize/5),center[1]+int(faceSize/3)], [center[0],center[1]+int(faceSize/2)], [center[0]+int(faceSize/3),center[1]+int(faceSize/4)]])
    cv2.fillPoly(image, pts = [contours], color=color['pinkyRed'])
    
    return image

def drawBody(Lshoulder,Rshoulder,Lhip,Rhip,faceSize,image):
    ExplainValue = 30
    hipShift = int(((faceSize/2)+(faceSize/2))/2)
    Lhip = (Lhip[0]+hipShift,Lhip[1])
    Rhip = (Rhip[0]-hipShift,Rhip[1])
    
    shoulderPTS = np.array([Lshoulder,
                            [Lshoulder[0],Lshoulder[1]-int(faceSize/1.2)],
                            [Rshoulder[0],Rshoulder[1]-int(faceSize/1.2)],
                            Rshoulder])
    bodyPTS = np.array([
        Lshoulder,Rshoulder,Rhip,Lhip
    ])
    logoImage = cv2.imread('avoidObstacles/resource/logo.png',cv2.IMREAD_UNCHANGED)
    logoImageWidth = logoImageHeight = int((Lshoulder[0]-Rshoulder[0]))
    if int((Lshoulder[0]-Rshoulder[0])) < 2:
        logoImageWidth = logoImageHeight = 1
    logoImage = cv2.resize(logoImage,(logoImageWidth,logoImageHeight))
    LbodySid = np.array([
        Lshoulder,
        [Lhip[0]-ExplainValue,Lhip[1]],
        Lhip
        # [Lshoulder[0]+ExplainValue+ExplainValue,Lshoulder[1]+ExplainValue],
        # [Lhip[0]+ExplainValue+ExplainValue,Lhip[1]-ExplainValue]
    ])
    RbodySid = np.array([
        Rshoulder,
        [Rhip[0]+ExplainValue,Rhip[1]],
        Rhip
        # [Lshoulder[0]+ExplainValue+ExplainValue,Lshoulder[1]+ExplainValue],
        # [Lhip[0]+ExplainValue+ExplainValue,Lhip[1]-ExplainValue]
    ])
        # 
    # cv2.fillPoly(image,pts = [RbodySid],color = color['shirtBody'])
    
    # cv2.fillPoly(image,pts = [LbodySid],color = color['shirtBody'])
    # angle = azmiusAngel(Lshoulder,Rshoulder)
    # print(angle)
    # cv2.ellipse(image,(int((Lshoulder[0]+Rshoulder[0])/2),int((Lshoulder[1]+Rshoulder[1])/2)),(int((Lshoulder[0]-Rshoulder[0])/2),int(ExplainValue*2.3)),angle,180,360,color['shirtBody'],-1)
    cv2.fillPoly(image,pts = [shoulderPTS],color = color['Dshirtbody'])
    cv2.fillPoly(image,pts = [bodyPTS],color = color['shirtBody'])
    cv2.fillPoly(image,pts = [LbodySid],color = color['Dshirtbody'])
    cv2.fillPoly(image,pts = [RbodySid],color = color['Dshirtbody'])
    cv2.polylines(image,pts= [bodyPTS],isClosed=True,color=color['black'],thickness=2)
    cv2.polylines(image,pts= [bodyPTS],isClosed=True,color=color['black'],thickness=2)

    # cv2.rectangle(image,Lshoulder,Rhip,color['shirtBody'],-1)
    image = cvzone.overlayPNG(image,logoImage,Rshoulder)
    # print(Rshoulder)
    return image


def drawHand(image,Rwrit,Lwrit,Relbow,Lelbow,Rshoulder,Lshoulder,handSize):
    handSize = int(handSize*0.8)
    if handSize <= 0 :
        handSize = 2
    isClose = False
    LhandPTS = np.array([
        Lshoulder,
        Lelbow,
        [Lwrit[0],Lwrit[1]]
    ])
    RhandPTS = np.array([
        Rshoulder,
        Relbow,
        [Rwrit[0],Rwrit[1]]
    ])
    
    cv2.polylines(image,[RhandPTS],isClose,color['skincolor'],handSize,cv2.LINE_AA)
    cv2.polylines(image,[LhandPTS],isClose,color['skincolor'],handSize,cv2.LINE_AA)
    
    
    LhandPTS = np.array([
        Lshoulder,
        [int((Lelbow[0]+Lshoulder[0])*0.5),int((Lelbow[1]+Lshoulder[1])*0.5)],
    ])
    RhandPTS = np.array([
        Rshoulder,
        [int((Relbow[0]+Rshoulder[0])*0.5),int((Relbow[1]+Rshoulder[1])*0.5)],
    ])
    rPTS = np.array([
        [Rshoulder[0]+handSize,Rshoulder[1]+handSize],
        [Rshoulder[0]-handSize,Rshoulder[1]-handSize],
        [Relbow[0]-handSize,Relbow[1]-handSize],
        [Relbow[0]+handSize,Relbow[1]+handSize]
        
    ])
    lPTS = np.array([
        [Lshoulder[0]+handSize,Lshoulder[1]+handSize],
        [Lshoulder[0]-handSize,Lshoulder[1]-handSize],
        [Lelbow[0]-handSize,Lelbow[1]-handSize],
        [Lelbow[0]+handSize,Lelbow[1]+handSize]
    ])

    # cv2.polylines(img = image,pts = [RhandPTS],isClosed = False,color = color['Dshirtbody'],thickness = handSize*2)    
    cv2.polylines(image,[RhandPTS],isClose,color['Dshirtbody'],int(handSize*1.9))
    # cv2.fillPoly(image,pts = [rPTS],color = color['Dshirtbody'])

    cv2.polylines(image,[LhandPTS],isClose,color['Dshirtbody'],int(handSize*1.9))
    # cv2.fillPoly(image,pts = [lPTS],color = color['Dshirtbody'])

    # cv2.circle(image,Lwrit,int(handSize*1.05),color['skincolor'],-1)
    # cv2.circle(image,Lwrit,int(handSize*1.05),color['DskinColor'],1)
    # cv2.circle(image,(Lwrit[0]-15,Lwrit[1]),int(handSize*0.15),color['DskinColor'],-1)


    # cv2.circle(image,Rwrit,int(handSize*1.05),color['skincolor'],-1)
    # cv2.circle(image,Rwrit,int(handSize*1.05),color['DskinColor'],1)
    # cv2.circle(image,(Rwrit[0]+15,Rwrit[1]),int(handSize*0.15),color['DskinColor'],1)

    return image
def drawLeg(image,Lhip,Rhip,Rknee,Lknee,Rankle,Lankle,hipCenter,LegSize):
    LegsSize = LegSize
    hipSize = int(LegSize*0.9)
    LegSize = int(LegSize*1.5)
    if hipSize <= 0 :
        hipSize = 3
    isClose = False
    Lleg = np.array([
        [Lhip[0],Lhip[1]],
        Lknee,
        Lankle
    ])
    Rleg = np.array([
        [Rhip[0],Rhip[1]],
        Rknee,
        Rankle
    ])
    axesHeight  = int((Lhip[0]-Rhip[0])/2)
    if axesHeight < 1 :
        axesHeight = 3
    PTS = np.array([
        Lhip,
        Lknee,
        [hipCenter[0],hipCenter[1]+axesHeight],
        Rknee,
        Rhip
    ])
    # cv2.ellipse(image,(int((Lhip[0]+Rhip[0])/2),int((Lhip[1]+Rhip[1])/2)),(axesHeight,int(hipSize*2)),180,180,360,color['Dblue'],-1)
    cv2.fillPoly(image,pts = [PTS],color = color['Dblue'])
    cv2.polylines(image,[Rleg],isClose,color['Dblue'],LegsSize)
    
    cv2.polylines(image,[Lleg],isClose,color['Dblue'],LegsSize)
    return image
def draw_legBypollies(image,Lhip,Rhip,Rknee,Lknee,Rankle,Lankle,LegSize):
    
    return image