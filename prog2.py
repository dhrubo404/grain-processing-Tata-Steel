import cv2
import numpy as np

birdEye = cv2.imread("C:\\Users\\dhrub\\Desktop\\Images\\image1.jpg",0)

# Replace all (dark) values below 10 with 10 - avoiding issues where there are black pixels inside an object
birdEye = np.maximum(birdEye, 10)

foreground = birdEye.copy()

seed = (10, 10)  # Use the top left corner as a "background" seed color (assume pixel [10,10] is not in an object).

# Use floodFill for filling the background with black color
cv2.floodFill(foreground, None, seedPoint=seed, newVal=(0, 0, 0), loDiff=(5, 5, 5, 5), upDiff=(5, 5, 5, 5))

# Convert to Grayscale
gray = cv2.cvtColor(foreground, cv2.COLOR_BGR2GRAY)

# Apply threshold
thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)[1]

# Use opening for removing small outliers
thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5)))

# Find contours
cntrs, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# Draw contours
cv2.drawContours(birdEye, cntrs, -1, (255, 0, 255), 3)

# Show images for testing
cv2.imshow('foreground', foreground)
cv2.imshow('gray', gray)
cv2.imshow('thresh', thresh)
cv2.imshow('birdEye', birdEye)

cv2.waitKey()
cv2.destroyAllWindows()