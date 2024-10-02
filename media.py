import mediapipe as mp
import cv2
import matplotlib.pyplot as plt


mp_pose = mp.solutions.pose
pose_image = mp_pose.Pose(static_image_mode = True, min_detection_confidence=0.5, model_complexity = 1)
pose_video = mp_pose.Pose(static_image_mode = False, model_complexity = 1,min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils
DISTANCE = 20
def detectPose(image, pose, draw=False, display=False):
    output_image = image.copy()
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    results = pose.process(imageRGB)
    if results.pose_landmarks and draw:
        mp_drawing.draw_landmarks(image = output_image,landmark_list=results.pose_landmarks,
                                    connections=mp_pose.POSE_CONNECTIONS,
                                    landmark_drawing_spec=mp_drawing.DrawingSpec(color=(255,255,255),
                                                                            thickness=3,circle_radius=3),
                                    connection_drawing_spec=mp_drawing.DrawingSpec(color=(49,125,237),
                                                                                    thickness=2,circle_radius=2))
    if display:
        plt.figure(figsize=[22,22])
        plt.subplot(121);plt.imshow(image[:,:,::-1]);plt.title('Original Image');plt.axis('off')
        plt.subplot(122);plt.imshow(output_image[:,:,::-1]);plt.title('Output Image');plt.axis('off')
    else:
        return output_image,results

WIDTH , HEIGHT = 1280 ,960
camera_video = cv2.VideoCapture(0)
camera_video.set(3, WIDTH)
camera_video.set(4, HEIGHT)

# cv2.namedWindow('Hands Joined?', cv2.WINDOW_NORMAL)
while camera_video.isOpened():
    ok, frame = camera_video.read()
    if not ok:
        continue
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    frame, results = detectPose(frame, pose_video, draw=True)
    Nose = results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE]
    
    if (Nose.y*HEIGHT+0.5)+ DISTANCE > HEIGHT/2:
        
        cv2.putText(frame,"Down",(50,50),cv2.FONT_HERSHEY_SIMPLEX,0.75,(0,0,255),2)
    elif (Nose.x*WIDTH+0.5) + DISTANCE < WIDTH/2:
        cv2.putText(frame,"Left",(50,50),cv2.FONT_HERSHEY_SIMPLEX,0.75,(0,0,255),2)
    elif (Nose.x*WIDTH+0.5) -DISTANCE > WIDTH/2:
        cv2.putText(frame,"Right",(50,50),cv2.FONT_HERSHEY_SIMPLEX,0.75,(0,0,255),2)
    else:
        cv2.putText(frame,"Center",(50,50),cv2.FONT_HERSHEY_SIMPLEX,0.75,(0,0,255),2)
    #     frame, _ = checkHandsJoined(frame, results, draw=True)
        
    cv2.imshow('Hands Joined?', frame)
    k = cv2.waitKey(1) & 0xFF
    if (k == 27):
        break
camera_video.release()
cv2.destroyAllWindows()