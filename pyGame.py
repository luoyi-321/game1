import cv2

image = cv2.imread('avoidObstacles/resource/Coin.png')

cv2.imshow("image",image)
print(str(image.shape))
cv2.waitKey(10)