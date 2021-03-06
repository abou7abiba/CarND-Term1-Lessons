# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # Find the lines using Sliding Window Class
# 
# We can use the two highest peaks from our histogram as a starting point for determining where the lane lines are, and then use sliding windows moving upward in the image (further along the road) to determine where the lane lines go.
# 
# ## Example
# ![image.png](attachment:image.png)
# 
# We call the function definition defined in the [sliding_window.py](sliding_window.py)

# %%
import cv2
# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg

# %% [markdown]
# Import funntion implemented from [sliding_window.py](sliding_window.py)

# %%
import os
import sys
sys.path.append(os.path.abspath("sliding_window.py"))

from sliding_window import * 

# %% [markdown]
# Read in an image and grayscale it

# %%
print (os.getcwd())
image_path = "Lesson8//test_images//warped-example.jpg"
print (os.path.exists(image_path))
binary_warped = cv2.imread(image_path)
binary_warped = cv2.cvtColor(binary_warped, cv2.COLOR_RGB2GRAY)
# self._blurred_image = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
# binary_warped = mpimg.imread('test_images/warped-example.jpg')

# %% [markdown]
# Run the function

# %%
#out_img = fit_polynomial(binary_warped)
#out_img = fit_polynomial(binary_warped, nwindows=20, margin=50, minpix=50)
slider = SlidingWindow (binary_warped)
slider.fit_polynomial()
print (slider.get_left_lane_poly())
print (slider.get_right_lane_poly())
out_img = slider.draw_lanes ()
cv2.imshow('image window',out_img)
cv2.waitKey(0)
# plt.plot(out_img)

# %% [markdown]
# Plot the result

# %%
# f, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 9))
# f.tight_layout()
# ax1.imshow(binary_warped, cmap='gray')
# ax1.set_title('Original Image', fontsize=50)
# ax2.imshow(out_img)
# ax2.set_title('Showing Windows', fontsize=50)
# plt.subplots_adjust(left=0., right=1, top=0.9, bottom=0.)

# %% [markdown]
# The following includes examples to explain usage of both [numpy.nonzero][1] [numpy.linspace()][2]
# 
# [1]:https://numpy.org/doc/stable/reference/generated/numpy.nonzero.html?highlight=nonzero#numpy.nonzero
# [2]:https://numpy.org/doc/stable/reference/generated/numpy.linspace.html?highlight=numpy%20linspace#numpy.linspace

# %%
input = np.array([[1, 2, 0, 0, 3], [0, 0, 1, 1, 0]])
out = input.nonzero()
print (out)
print (input.shape)
print (out[0].shape)
length = 50
ploty = np.linspace(0, length-1, length )
print (ploty)


# %%



