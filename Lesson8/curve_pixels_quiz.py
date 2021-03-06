import numpy as np
import math

def generate_data(y_ratio, x_ratio):
    '''
    Generates fake data to use for calculating lane curvature.
    In your own project, you'll ignore this function and instead
    feed in the output of your lane detection algorithm to
    the lane curvature calculation.

    Arg:
        y_ratio: is the y in meters per pixel.
        x_ratio: is the x in meters per pixel.
    '''
    # Set random seed number so results are consistent for grader
    # Comment this out if you'd like to see results on different random data!
    np.random.seed(0)
    # Generate some fake data to represent lane-line pixels
    ploty = np.linspace(0, 719, num=720)# to cover same y-range as image
    quadratic_coeff = 3e-4 # arbitrary quadratic coefficient
    # For each y position generate random x position within +/-50 pix
    # of the line base position in each case (x=200 for left, and x=900 for right)
    leftx = np.array([200 + (y**2)*quadratic_coeff + np.random.randint(-50, high=51) 
                                    for y in ploty])
    rightx = np.array([900 + (y**2)*quadratic_coeff + np.random.randint(-50, high=51) 
                                    for y in ploty])

    leftx = leftx[::-1]  # Reverse to match top-to-bottom in y
    rightx = rightx[::-1]  # Reverse to match top-to-bottom in y


    # Fit a second order polynomial to pixel positions in each fake lane line
    left_fit = np.polyfit(y_ratio * ploty, x_ratio * leftx, 2)
    right_fit = np.polyfit(y_ratio * ploty, x_ratio * rightx, 2)

    return ploty, leftx, rightx, left_fit, right_fit

def generate_data_2 (y_ratio, x_ratio):
    '''
    Generates fake data to use for calculating lane curvature.
    In your own project, you'll ignore this function and instead
    feed in the output of your lane detection algorithm to
    the lane curvature calculation.

    Arg:
        y_ratio: is the y in meters per pixel.
        x_ratio: is the x in meters per pixel.
    '''
    # Set random seed number so results are consistent for grader
    # Comment this out if you'd like to see results on different random data!
    np.random.seed(0)
    # Generate some fake data to represent lane-line pixels
    ploty = np.linspace(0, 719, num=720)# to cover same y-range as image
    quadratic_coeff = 3e-4 # arbitrary quadratic coefficient
    # For each y position generate random x position within +/-50 pix
    # of the line base position in each case (x=200 for left, and x=900 for right)
    leftx = np.array([200 + (y**2)*quadratic_coeff + np.random.randint(-50, high=51) 
                                    for y in ploty])
    rightx = np.array([900 + (y**2)*quadratic_coeff + np.random.randint(-50, high=51)
                                    for y in ploty])

    leftx = leftx[::-1]  # Reverse to match top-to-bottom in y
    rightx = rightx[::-1]  # Reverse to match top-to-bottom in y


    # Fit a second order polynomial to pixel positions in each fake lane line
    left_fit = np.polyfit(ploty, leftx, 2)
    right_fit = np.polyfit(ploty, rightx, 2)

    # Convert in real world scale
    # x= mx / (my ** 2) *a*(y**2)+(mx/my)*b*y + mx*c
    left_fit  = x_ratio / (y_ratio ** 2) * left_fit [0], x_ratio / y_ratio * left_fit [1], x_ratio * left_fit [2]
    right_fit  = x_ratio / (y_ratio ** 2) * right_fit [0], x_ratio / y_ratio * right_fit [1], x_ratio * right_fit [2]
    

    return ploty * y_ratio, leftx * x_ratio, rightx * x_ratio, left_fit, right_fit

def calculate_curvature (lin_fit, y):
    # for equation f(x) = ay^2 + by + c which is the 2nd order polynomial passed in the line_fit
    a, b, c = lin_fit[0], lin_fit[1], lin_fit[2]

    y1 = 2*a*y + b
    y2 = 2*a

    r_curv = math.pow (1 + y1**2, 1.5) / abs (y2)

    return r_curv

def measure_curvature_pixels():
    '''
    Calculates the curvature of polynomial functions in pixels.
    '''
    # Start by generating our fake example data
    # Make sure to feed in your real data instead in your project!
    # ploty, leftx, rightx, left_fit, right_fit = generate_data(ym_per_pix, xm_per_pix)
    ploty, leftx, rightx, left_fit, right_fit = generate_data (1, 1)
    
    # Define y-value where we want radius of curvature
    # We'll choose the maximum y-value, corresponding to the bottom of the image
    y_eval = np.max(ploty)     # convert to real world
    
    ##### TO-DO: Implement the calculation of R_curve (radius of curvature) #####
    left_curverad = calculate_curvature (left_fit, y_eval)
    right_curverad =calculate_curvature (right_fit, y_eval)
    
    return left_curverad, right_curverad


def measure_curvature_real():
    '''
    Calculates the curvature of polynomial functions in pixels.
    '''
    # Define conversions in x and y from pixels space to meters
    ym_per_pix = 30/720 # meters per pixel in y dimension
    xm_per_pix = 3.7/700 # meters per pixel in x dimension
    
    # Start by generating our fake example data
    # Make sure to feed in your real data instead in your project!
    # ploty, leftx, rightx, left_fit, right_fit = generate_data(ym_per_pix, xm_per_pix)
    ploty, leftx, rightx, left_fit, right_fit = generate_data_2 (ym_per_pix, xm_per_pix)
    
    # Define y-value where we want radius of curvature
    # We'll choose the maximum y-value, corresponding to the bottom of the image
    # y_eval = np.max(ploty) * ym_per_pix     # convert to real world
    y_eval = np.max(ploty)

    ##### TO-DO: Implement the calculation of R_curve (radius of curvature) #####
    left_curverad = calculate_curvature (left_fit, y_eval)
    right_curverad =calculate_curvature (right_fit, y_eval)
    
    return left_curverad, right_curverad


# Calculate the radius of curvature in pixels for both lane lines
# left_curverad, right_curverad = measure_curvature_pixels()

# print(left_curverad, right_curverad)
# Should see values of 1625.06 and 1976.30 here, if using
# the default `generate_data` function with given seed number