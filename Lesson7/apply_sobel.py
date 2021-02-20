import numpy as np
import cv2
# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg
import pickle



def abs_sobel_thresh(img, orient='x', thresh=(0, 255)):
    """
    Define a function that applies Sobel x or y, then takes an absolute value and applies a threshold. 
    Note: calling your function with 
        orient='x', thresh_min=20, thresh_max=100 
    should produce output like the example image shown above this quiz.

    Args:
        img (Array): The input image
        orient (str, optional): either 'x', or 'y'. Defaults to 'x'.
        thresh (tuple, optional): Create a mask of 1's for the input image where the scaled gradient 
        magnitude is > thresh_min and < thresh_max. Defaults to (0, 255).

    Returns:
        tuple: Return the masked image as binary_output image
    """    
    # Apply the following steps to img
    # 1) Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # 2) Take the derivative in x or y given orient = 'x' or 'y'
    if orient == 'x':
        sobel = cv2.Sobel(gray, cv2.CV_64F, 1, 0)
    elif orient == 'y':
        sobel = cv2.Sobel(gray, cv2.CV_64F, 0, 1)
    elif orient == 'xy' :
        sobel = cv2.Sobel(gray, cv2.CV_64F, 1, 1)    
    else:
        sobel = None

    
    # 3) Take the absolute value of the derivative or gradient
    abs_sobel = np.absolute(sobel)

    # 4) Scale to 8-bit (0 - 255) then convert to type = np.uint8
    scaled_sobel = np.uint8(255*abs_sobel/np.max(abs_sobel))

    # 5) Create a mask of 1's where the scaled gradient magnitude 
    # is > thresh_min and < thresh_max
    binary_output = np.zeros_like(scaled_sobel)
    binary_output[(scaled_sobel >= thresh[0]) & (scaled_sobel <= thresh[1])] = 1
    
    # 6) Return this mask as your binary_output image
    return binary_output
    
