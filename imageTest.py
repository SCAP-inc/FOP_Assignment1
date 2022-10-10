import matplotlib.pyplot as plt
import cv2

image = cv2.imread("terrain.png")
# image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# cv2.imshow("image",image)
# cv2.waitKey(10000)

print(image[587, 336])


plt.imshow(image)
