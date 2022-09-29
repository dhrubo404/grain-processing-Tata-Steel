from tkinter import Image, image_names
import cv2
from matplotlib import pyplot as plt
from scipy import ndimage
from skimage import measure, color, io

#reading image and defining pixels
image = cv2.imread("C:\\Users\\dhrub\\Desktop\\Images\\image1.jpg",0)

# convert to RGB
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

# create a binary thresholded image
_, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
# show it
plt.imshow(binary, cmap="gray")

# find the contours from the thresholded image
contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# draw all contours
image = cv2.drawContours(image, contours, -1, (0, 255, 0), 2)
# show the image with the drawn contours
plt.imshow(image)
plt.show()
