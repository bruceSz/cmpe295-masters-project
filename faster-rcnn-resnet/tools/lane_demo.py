from __future__ import division
import math
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import os
import operator
import imutils
from skimage import io
from moviepy.editor import VideoFileClip



def grayscale(img):
    
    """Applies the Grayscale transform
    This will return an image with only one color channel
    but NOTE: to see the returned image as grayscale
    (assuming your grayscaled image is called 'gray')
    you should call plt.imshow(gray, cmap='gray')"""
    
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    
def canny(img, low_threshold, high_threshold):
    """Applies the Canny transform"""
    img = np.uint8(img)
    return cv2.Canny(img, low_threshold, high_threshold)

def gaussian_blur(img, kernel_size):
    """Applies a Gaussian Noise kernel"""
#    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 200)

def region_of_interest(img, vertices):
    """
    Applies an image mask.
    
    Only keeps the region of the image defined by the polygon
    formed from `vertices`. The rest of the image is set to black.
    """
    #defining a blank mask to start with
    mask = np.zeros_like(img)   
    
    #defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255
        
    #filling pixels inside the polygon defined by "vertices" with the fill color    
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    
    #returning the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)
    
    return masked_image


def fit_line(xs,ys,a,b):

    """

    Collects the set of x and y coordinates of all points in lists 'xs' and 'ys' respectively.
    A line fitting is done using these points using built in least square API which returns
    a slope 'm' and intercept 'c'.  Paramters 'a' and 'b' are y coordinates of the
    points between which a line will be drawn on top of video clip. The x coorindates
    are obtained using 'a' and 'b' along with 'm' and 'c' and using
    equation of a straight line

    """
    # Chekcing against empty list, if empty return 0s
    if  not (xs):
        return 0,0,0,0
    
    # Preparing vectors for least square
    z = np.vstack([xs, np.ones(len(xs))]).T
    s = np.array(ys)

    # Applying least square fitting on points
    m, c = np.linalg.lstsq(z, np.array(ys))[0]   #Applying least squares method
    
    #Using slope and intercept plus y coordinates to get x-coordinates
    x1 = int(a/m - c/m)              
    x2 = int(b/m - c/m)
    
    return x1,a,x2,b

def draw_lines(img, lines, color=[255, 0, 0], thickness=10):
    """
    This function draws `lines` with `color` and `thickness`.    
    Lines are drawn on the image inplace (mutates the image).
 
    """
    
    yFinal = 540
    yIni = 350
    xPlus = []
    yPlus = []
    xMinus = []
    yMinus= []
    slope_range = 0.2

    if lines is not None:
        for line in lines:
            if line is not None:
                for x1,y1,x2,y2 in line:
                    # check slope   
                    slope = (y2-y1)/(x2-x1)
		    
 		    # Collect all points with + ve slope
                    if (slope > slope_range):
                        xPlus.append(x1)
                        xPlus.append(x2)
                        yPlus.append(y1)
                        yPlus.append(y2)

                    # Collect all points with - ve slope
                    elif ((slope) < (-slope_range)):
                        xMinus.append(x1)
                        xMinus.append(x2)
                        yMinus.append(y1)
                        yMinus.append(y2)
                    # If out of range, lists defined in beginning of this function will be empty  
                    else:
                        continue
    
    x1,y1,x2,y2 = fit_line(xPlus,yPlus, yIni,yFinal)
    cv2.line(img,(x1,y1),(x2,y2),color, thickness)  
    x1,y1,x2,y2 = fit_line(xMinus,yMinus, yIni,yFinal)
    cv2.line(img,(x1,y1),(x2,y2),color,thickness)  


def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    """
    `img` should be the output of a Canny transform.
        
    Returns an image with hough lines drawn.
    """
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    draw_lines(line_img, lines)
    
    return line_img

# Python 3 has support for cool math symbols.

def weighted_img(img, initial_img, alpha=0.8, beta=1., gamma=0.):
    """
    `img` is the output of the hough_lines(), An image with lines drawn on it.
    Should be a blank image (all black) with lines drawn on it.
    
    `initial_img` should be the image before any processing.
    
    The result image is computed as follows:
    
    NOTE: initial_img and img must be the same shape!
    """
    return cv2.addWeighted(initial_img, alpha, img, beta, gamma)


def process_image(img):
    
    img = imutils.resize(img, height = min(480, img.shape[0]))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    kernel_size = 5
    blur_gray = gaussian_blur(gray,kernel_size)

    edges = canny(blur_gray, 5, 140)
#     cv2.imwrite("canny.jpg", edges)
    # cv2.imshow("canny image", edges)
    # cv2.waitKey(0)
    
    # Masking out our area of interest 
    mask = np.zeros_like(edges)   
    ignore_mask_color = 255 
    imshape = edges.shape

    # Define four sided polygon, whose upper two vertices are chosen with hit and trial
    # Lower vertices stretch down to image border
 
    rows = imshape[0] # height
    cols = imshape[1] # width
   
    # the vertices are an array of polygons (i.e array of arrays) and the data type must be integer
    # Now we apply a region mask to focus only in our region of interest.
    # The region of interest will be defined by a trapezoid with two vertex in the bottom corners
    # of the image and the other two in the 'horizon' area of the road aprox.

    # Params for region of interest
    bot_left = [80, 480]
    bot_right = [cols*0.95, 480]
    apex_right = [cols*0.55, 250]
    apex_left = [cols*0.4, 250]

    vertices = [np.array([bot_left, bot_right, apex_right, apex_left], dtype=np.int32)]
    
    # Define region of interest based on image shape
    masked_edges = region_of_interest (edges, vertices)
    # cv2.imshow("masked image",masked_edges)
    # cv2.waitKey(0)
   
   
    #  Hough transform parameters
    # rho = 1# distance resolution in pixels of the Hough gridl
    rho = 2
    theta = 1*np.pi/180 # angular resolution in radians of the Hough grid
    # threshold = 20    # minimum number of votes (intersections in Hough grid cell)
    threshold = 70
    # min_line_length = 30 #minimum number of pixels making up a line
    min_line_length = 1
    max_line_gap = 200    
    # max_line_gap = 60    # maximum gap in pixels between connectable line segments
    final_lines = np.copy(img)*0 # creating a blank to draw lines on

    # Run Hough on edge detected image
    # Output "final _lines" is an array containing endpoints of detected line segments

    # final_lines = hough_lines(masked_edges, rho, theta, threshold, min_line_length, max_line_gap)

    final_lines = np.copy(img)*0 # creating a blank to draw lines on
   
    # Run Hough on edge detected image
    # Output "final _lines" is an array containing endpoints of detected line segments
    final_lines = hough_lines(masked_edges, rho, theta, threshold, min_line_length, max_line_gap)

#     final_lines = hough_lines(masked_edges,2,np.pi/180,20,1,1)
    # cv2.imshow("hough lines",final_lines)
    # cv2.waitKey(0)
  
    # Create a "color" binary image to combine with line image
    color_edges = np.dstack((img[:,:,0], img[:,:,1], img[:,:,2])) 

    # Draw the lines on the edge image
    final = weighted_img(final_lines, color_edges )

    return final
    

if __name__ == '__main__':	

    folder_name = '/home/student/cmpe295-masters-project/faster-rcnn-resnet/data/input-images/'
    folder_name_res = '/home/student/cmpe295-masters-project/faster-rcnn-resnet/data/output-images/'
    t_images = os.listdir(folder_name)

    for d in range(len(t_images)):
        if "00" not in t_images[d]:
           img = io.imread(folder_name+t_images[d])
           pimg = process_image(img)                      # processed image
           # plt.show() 
           cv2.imwrite(os.path.join(folder_name_res, 'processesd_'+ t_images[d]), pimg)
           print (folder_name_res + 'processed_'+ t_images[d])

           ## Show output frame
           # cv2.imshow("output", pimg)
           # cv2.waitKey(0)

    # Only plotting the last image
    plt.imshow(pimg)
