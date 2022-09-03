
from cv2 import CAP_DSHOW
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv
import depthSensor as dp #File made by intel to get rgb and depth images


#Send in a tuple of the approximate rgb value of the object
def detectObject(arrayOfRGB, color, margin, RGBImage, toPlot):
    """Detects objects from image with same color and errormargin as specified

    Args:
        arrayOfRGB (numpy array): array which contains the rgb pixel values
        color (tuple): color of object to detect
        margin (int): errormargin for colorsearch
        RGBImage (OpenCV Image): The image to scan
        toPlot (boolean): True = plot, False = not plot
    """

    x_koor = []
    y_koor = []
    y = -1 #Row
    x = 0 #Column

    #Gets the dimensions of the image
    height, width, channels = RGBImage.shape

    #Loops over pixels
    for pixels in range(0, len(arrayOfRGB)):
        for k in range(0, len(arrayOfRGB[pixels])): #Cal it something useful, not k
            #Counts pixels and syncs x- and y-coordinates to pixels
            if x == 0:
                y += 1
            x = (x + 1) % width
            
            #Calculates difference between image rgb values and the supplied colors rgb values
            diff = arrayOfRGB[pixels][k] - color
            if (all(np.abs(i) <= margin for i in diff)):
                if toPlot:
                    arrayOfRGB[pixels][k] = [255, 255, 0]
                x_koor.append(x)
                y_koor.append(y)

    #Plotting and showing image
    if toPlot:
        #Formats the sizes of axes correctly
        ax = plt.gca()
        ax.set_xlim([0, width])
        ax.set_ylim([0, height])
        ax.invert_yaxis()
        plt.plot(x_koor, y_koor)
        plt.imshow(RGBImage)
        plt.show()
    
    return x_koor, y_koor



#Finds center of object by averaging every x and y coordinate
def findCenter(x_koor, y_koor):
    #If the lists are empty return None
    if not x_koor and not y_koor:
        return None, None
    else:
        x_sum = 0
        y_sum = 0
        for x in x_koor:
            x_sum += x
        for y in y_koor:
            y_sum += y
        try:
            x_avg = int(x_sum / len(x_koor))
            y_avg = int(y_sum / len(y_koor))
            return x_avg, y_avg
        except ZeroDivisionError:
            return None, None



def run(colorOfObject, margin, toPlot):
    """Runs the software
    
    Args:
        colorOfObject (numpy array): The RGB value of the object
        margin (int): The margin of error for the RGB pixels
        toPlot (boolean): True = plot, False = not plot
    """
    #Creates video capture
    capture = cv.VideoCapture(1, CAP_DSHOW)

    #Event loop
    while True:
        #Captures depth Image and RGB image
        RGBImage, depthFrame = dp.depthSensor()

        #Creates a numpy array of the RGBImage
        arrayOfRGB = np.array(RGBImage)

        #Gets the complete list of where the object resides in the image 
        x_koor, y_koor = detectObject(arrayOfRGB, colorOfObject, margin, RGBImage, toPlot)

        #Coordinates of the center of the object
        x, y = findCenter(x_koor, y_koor) 

        
        #If x and y are not None
        if x is not None and y is not None:
            #Gets the distance of the object in meters
            distance = depthFrame.get_distance(x, y)
            print(f"({x}, {y}, {round(distance, 3)})") #Prints the x, y and distance(m)


colorOfObject = np.array([46, 85, 103])
margin = 10
toPlot = True


run(colorOfObject, margin, toPlot)