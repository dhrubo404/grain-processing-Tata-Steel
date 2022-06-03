
"""
Performing grain processing on following image to find size of particles and store it in a csv file
Step 1: Input Image
Step 2: Denoising and thresholding to seperate ROIs 
Step 3: Clean Image and set up grains
Step 4: Label Grains
Step 5: Measure properites (i.e. Size) 
Step 6: Output into a .csv file

"""
import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy import ndimage
from skimage import measure, color, io

#reading image and defining pixels
img = cv2.imread("C:\\Users\\dhrub\\Desktop\\Images\\image1.jpg",0)

pixels_to_um = 0.5 #pixel to micron conversion 

#denoising

plt.hist(img.flat, bins=100, range=(0,255))

#thresholding using otsu's method

ret, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
print (ret) #best threshold

#cleaning up image
kernel = np.ones((3,3),np.uint8) 
eroded = cv2.erode(thresh,kernel,iterations = 1)
dilated = cv2.dilate(eroded,kernel,iterations = 1)

mask = dilated == 255

print(mask)
#mask = clear_border(mask)
io.imshow(mask)

io.imshow(mask[250:280, 250:280])

s = [[1,1,1],[1,1,1],[1,1,1]]
#label_im, nb_labels = ndimage.label(mask)
labeled_mask, num_labels = ndimage.label(mask, structure=s)

#The function outputs a new image that contains a different integer label 
#for each object, and also the number of objects found.


#Let's color the labels to see the effect
img2 = color.label2rgb(labeled_mask, bg_label=0)

cv2.imshow('Colored Grains', img2)
cv2.waitKey(0)


print(num_labels) 




clusters = measure.regionprops(labeled_mask, img)  #send in original image for Intensity measurements

#The output of the function is a list of object properties. 

#Test a few measurements
print(clusters[0].perimeter)

#Can print various parameters for all objects
for prop in clusters:
    print('Label: {} Area: {}'.format(prop.label, prop.area))
    
    
propList = ['Area',
            'equivalent_diameter', #Added... verify if it works
            'orientation', #Added, verify if it works. Angle btwn x-axis and major axis.
            'MajorAxisLength',
            'MinorAxisLength',
            'Perimeter',
            'MinIntensity',
            'MeanIntensity',
            'MaxIntensity']    
    

output_file = open("C:\\Users\\dhrub\\Documents\\image1.csv", 'w')
output_file.write(',' + ",".join(propList) + '\n') #join strings in array by commas, leave first cell blank
#First cell blank to leave room for header (column names)

for cluster_props in clusters:
    #output cluster properties to the excel file
    output_file.write(str(cluster_props['Label']))
    for i,prop in enumerate(propList):
        if(prop == 'Area'): 
            to_print = cluster_props[prop]*pixels_to_um**2   #Convert pixel square to um square
        elif(prop == 'orientation'): 
            to_print = cluster_props[prop]*57.2958  #Convert to degrees from radians
        elif(prop.find('Intensity') < 0):          # Any prop without Intensity in its name
            to_print = cluster_props[prop]*pixels_to_um
        else: 
            to_print = cluster_props[prop]     #Reamining props, basically the ones with Intensity in its name
        output_file.write(',' + str(to_print))
    output_file.write('\n')
output_file.close()#Closes the file, otherwise it would be read only. 
