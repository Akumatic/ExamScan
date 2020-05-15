# SPDX-License-Identifier: MIT
# Copyright (c) 2019 Akumatic

import cv2, imutils, numpy

def threshold (
        image: numpy.ndarray,
        threshold: int = 200,
    ) -> numpy.ndarray:
    """ Converts given image to black and white

    Args:
        image (ndarray):
            the image to be processed
        threshold (int):
            the threshold at which every pixel value should be set to 255
    """
    _, img_binary = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
    return img_binary

def blur (
        image: numpy.ndarray,
        kernel_size: int = 7
    ) -> numpy.ndarray:
    """ Filters the given picture by converting it to gray scale and
        applying gaussian blur filter

    Args:
        image (ndarray):
            the image to be processed
        kernel_size (int):
            the size of the kernel for the gaussian blur

    Returns:
        A ndarray containing the filtered image
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)

def edge_detection (
        image: numpy.ndarray
    ) -> numpy.ndarray:
    """ Applies canny edge detection on a given image

    Args:
        image (ndarray):
            the image to be processed

    Returns:
        A ndarray containing the image after canny detection
    """
    return imutils.auto_canny(image)

def draw_circles (
        image: numpy.ndarray,
        centers: list,
        color: tuple,
        radius: int = 3,
        thickness: int = 2
    ) -> numpy.ndarray:
    """ Draws the centers of given contures with the given color,
        (size, thickness)

    Args:
        image (ndarray): 
            the image to be modified
        centers (list):
            a list containing the center coordinates as tuples (x, y)
        color (tuple):
            the color coded in BGR color scale
        radius (int):
            size of the circles to be drawn
        thickness (int):
            thickness of the borders of all circles to be drawn
    """
    for center in centers:
        cv2.circle(img=image, center=center[:2], radius=radius,
            color=color,thickness=thickness)

    return image

def draw_contours (
        image: numpy.ndarray,
        contours: list,
        color: tuple
    ) -> numpy.ndarray:
    """ Draws the given contours in the given picture with the given color.
    Args:
        image (ndarray):
            the image to be modified
        contours (list):
            A list containing contour data
        color (tuple):
            the color coded in BGR color scale

    Returns:
        the modified image as a multidimensional array
    """
    img = cv2.drawContours(image, contours, -1, color, 3)
    return img
    

def ratio_black (
        image: numpy.ndarray,
        center: tuple,
        radius: int,
    ) -> int:
    """ Calculates the ratio of black pixels in a given square area.

    Args:
        image (ndarray):
            the image 
        center (tuple):

        radius (int):


    Returns:
        The ratio of black pixels to all pixels
    """
    cnt_black = 0
    cnt_pixel = 0
    for x in range(center[0] - radius, center[0] + radius):
        for y in range(center[1] - radius, center[1] + radius):
            if image[y, x] == 0:
                cnt_black += 1
            cnt_pixel += 1

    return int(cnt_black / cnt_pixel * 100)

def eval_image (
        image: numpy.ndarray,
        data: list,
        radius: int
    ) -> numpy.ndarray:

    checked = [d[:2] for d in data if d[2] >= 20]
    corrected = [d[:2] for d in data if d[2] >= 50]

    draw_circles(image, checked, (0,255,0), radius, thickness=4)
    draw_circles(image, corrected, (255,0,0), radius, thickness=4)
    
    return image
