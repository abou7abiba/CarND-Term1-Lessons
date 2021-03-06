import numpy as np
import cv2


class SlidingWindow:
    def __init__(self, image, nwindows=9, margin=100, minpix=50):
        self.image = image
        self.out_img = np.dstack((image, image, image)) # Create an output image to draw on and visualize the result

        self.nwindows = nwindows
        self.margin = margin
        self.minpix = minpix

        # Note: numpy.nonzero(a) Return the indices of the elements that are non-zero
        # https://numpy.org/doc/stable/reference/generated/numpy.nonzero.html
        nonzero = image.nonzero()
        self.nonzeroy = np.array(nonzero[0])
        self.nonzerox = np.array(nonzero[1])
        self._left_fit = None    #Initialize with None in frame 0
        self._right_fit = None
        self._leftx, self._lefty = [], []
        self._rightx, self._righty = [], []  
        self._current_window = 0

    def get_left_lane_poly (self):
        return self._left_fit

    def get_right_lane_poly (self):
        return self._right_fit
        
    def get_histogram(self):
        """Get the histogram values of the y axis for the given image.

            This is done by getting the sum of all the values of the y axis
        Args:
            img ([type]): input image to get the histogram for

        Returns:
            array: for the sum of the values of the axis = 0
        """
        img = self.image
        # Grab only the bottom half of the image
        # Lane lines are likely to be mostly vertical nearest to the car
        bottom_half = img[img.shape[0]//2:, :]

        # TO-DO: Sum across image pixels vertically - make sure to set `axis`
        # i.e. the highest areas of vertical lines should be larger values
        histogram = np.sum(bottom_half, axis=0)

        return histogram

    def find_pixels_in_window(self, x):
        """Find pixels in the current window.
        We first calculate the dimensions of the current window in which
        window_height = image height / number of windows given in the parameters
        and this is the sliding factor.

        Then we find the none zero x & y in the given window which indicate the good indexes

        Finally increment the current window to indicate the following window.

        Args:
            x (int): the center x of the window which used to calculate the width
            in this case width is 2 * self.margin and x is in the middle.

        Returns:
            win_x_low, win_y_low, win_x_high, win_y_high:  the position of the window corners 
            good_inds (array): The nonzero points of x and y in the window
        """        
        image_height = self.image.shape[0]
        window_height = np.int(image_height // self.nwindows)

        # Identify window boundaries in x and y (and right and left)
        win_y_low = image_height - (self._current_window + 1) * window_height
        win_y_high = image_height - self._current_window * window_height
        ### TO-DO: Find the four below boundaries of the window ###
        win_x_low = x - self.margin
        win_x_high = x + self.margin

        ### TO-DO: Identify the nonzero pixels in x and y within the window ###
        good_inds = ((self.nonzeroy >= win_y_low) & (self.nonzeroy < win_y_high) &
                     (self.nonzerox >= win_x_low) & (self.nonzerox < win_x_high)).nonzero()[0]

        # Increment the current window
        self._current_window = self._current_window + 1
        return win_x_low, win_y_low, win_x_high, win_y_high, good_inds


    def find_x_base (self, left_line=True):

        # Take a histogram of the bottom half of the image
        histogram = self.get_histogram()

        # Find the peak of the left and right halves of the histogram
        # These will be the starting point for the left and right lines
        midpoint = np.int(histogram.shape[0]//2)

        if left_line:
            x_base = np.argmax(histogram[:midpoint])
        else:
            x_base = np.argmax(histogram[midpoint:]) + midpoint

        # Current positions to be updated later for each window in nwindows
        return int(x_base)


    def find_lane_pixels(self, left_line=True):
        """
        Find the lane pixels in the given image using the sliding window technique. 

        Returns:
            tuple:sequence of arrays
                4 arrays of the all Xs and Ys of both the left and right lane lines plus
                the image showing the output image with the windows drawn on it.
        """
        # Current positions to be updated later for each window in nwindows
        x_current = self.find_x_base (left_line)

        # Create empty lists to receive left and right lane pixel indices
        lane_inds = []

        # Step through the windows one by one
        for window in range(self.nwindows):

            # Find the left lane indices within the window.
            win_x_low, win_y_low, win_x_high, win_y_high, good_inds = self.find_pixels_in_window(
                x_current)
            # # Draw the windows on the visualization image
            cv2.rectangle(self.out_img, (win_x_low, win_y_low),
                          (win_x_high, win_y_high), (0, 255, 0), 2)

            # Append these indices to the lists
            lane_inds.append(good_inds)

            ### TO-DO: If you found > minpix pixels, recenter next window ###
            ### (`right` or `leftx_current`) on their mean position ###
            if len(good_inds) > self.minpix:
                x_current = np.int(np.mean(self.nonzerox[good_inds]))

        # Concatenate the arrays of indices (previously was a list of lists of pixels)
        try:
            lane_inds = np.concatenate(lane_inds)
        except ValueError:
            # Avoids an error if the above is not implemented fully
            pass

        # Extract left and right line pixel positions
        x = self.nonzerox[lane_inds]
        y = self.nonzeroy[lane_inds]

        return x, y

    def fit_polynomial(self):
        """
            Find the points representing the left and right lane lines and draw them 
            over the given image.

        Returns:
            [type]: [description]
        """
        # Find our lane pixels first
        self._leftx, self._lefty = self.find_lane_pixels()
        self._current_window = 0; # Reset the counter of the sliding window to start for the right lane.
        self._rightx, self._righty = self.find_lane_pixels(left_line=False)

        ### TO-DO: Fit a second order polynomial to each using `np.polyfit` ###
        self._left_fit = np.polyfit(self._lefty, self._leftx, 2)
        self._right_fit = np.polyfit(self._righty, self._rightx, 2)
        

    def draw_lanes(self):
        # Generate x and y values for plotting
        ploty = np.linspace(0, self.image.shape[0]-1, self.image.shape[0])
        try:
            left_fitx = self._left_fit[0]*ploty**2 + self._left_fit[1]*ploty + self._left_fit[2]
            right_fitx = self._right_fit[0]*ploty**2 + \
                self._right_fit[1]*ploty + self._right_fit[2]
        except TypeError:
            # Avoids an error if `left` and `right_fit` are still none or incorrect
            print('The function failed to fit a line!')
            left_fitx = 1*ploty**2 + 1*ploty
            right_fitx = 1*ploty**2 + 1*ploty

        ## Visualization ##
        # Colors in the left and right lane regions
        self.out_img[self._lefty, self._leftx] = [255, 0, 0]
        self.out_img[self._righty, self._rightx] = [0, 0, 255]

        # Draw the polynomial of the left line
        draw_points = (np.asarray([left_fitx, ploty]).T).astype(
            np.int32)   # needs to be int32 and transposed
        # args: image, points, closed, color
        cv2.polylines(self.out_img, [draw_points], False,
                      (255, 255, 0), thickness=3)

        # Draw the polynomial of the right line
        draw_points = (np.asarray([right_fitx, ploty]).T).astype(
            np.int32)   # needs to be int32 and transposed
        # args: image, points, closed, color
        cv2.polylines(self.out_img, [draw_points], False,
                      (255, 255, 0), thickness=3)

        return self.out_img



# if __name__ == '__main__':    
#     binary_warped = mpimg.imread('test_images/warped-example.jpg')
#     slider = SlidingWindow (binary_warped)
#     out_img = slider.fit_polynomial()
#     print (out_img)
# out_img = fit_polynomial(binary_warped)

# plt.imshow(out_img)
