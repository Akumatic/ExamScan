# SPDX-License-Identifier: MIT
# Copyright (c) 2019 Akumatic

import cv2, imutils, numpy
from . import utils

######################
# Contour operations #
######################

def find_contours (
        image: numpy.ndarray,
        mode: int = cv2.RETR_LIST,
        method: int = cv2.CHAIN_APPROX_SIMPLE
    ) -> list:
    """ Find all contours of the filtered image

    Args:
        image (ndarray):
            the filtered image

    Returns:
        A list containing contour data
    """
    cnts = cv2.findContours(image.copy(), mode, method)
    return imutils.grab_contours(cnts)

def find_boxes (
        contours: list,
        thres_area: int = 500,
        pad_ratio: float = 0.05
    ) -> (list, list):
    """ Find contours that resemble a box

    Args:
        contours (list):
            a list containing contour data

    Returns:
        A list containing the box contours
    """
    boxes = list()
    for c in contours:
        area = cv2.contourArea(c)
        perimeter = cv2.arcLength(c, True)
        shape_factor = utils.circularity(area, perimeter)

        if 0.7 < shape_factor < 0.85 and area >= thres_area:
            boxes.append(c)

    return boxes

def find_center (
        contours: list
    ) -> list:
    """ Find the center coordinates of all given contours.

    Args:
        contours (list):
            A list containing contour data

    Returns:
        A list containing the center coordinates and the contour as tuples
        (x, y, contour).
    """
    centers = []
    for contour in contours:
        m = cv2.moments(contour)
        try:
            x = int(m["m10"] / m["m00"])
            y = int(m["m01"] / m["m00"])
            centers.append((x, y, contour))
        except ZeroDivisionError:
            pass
    return centers

def filter_centers (
        coords: list,
        radius: int
    ):
    """ Removes all but one entry in circles given by coordinates and radius

    Args:
        coords (list):
            a list containing tuples of coordinates (x, y)
        radius (float):
            the radius around a center where no other center should be
    """
    a = 0

    while a < len(coords):
        b = a + 1
        while b < len(coords):
            if utils.distance(coords[a][:2], coords[b][:2]) <= radius:
                del coords[b]
            else:
                b += 1
        a += 1

def dist_center_topleft (
        contour: numpy.ndarray,
        center: tuple
    ) -> float:
    """ Calculates the distance from the center of a given contour to it's
        top left corner

    Args:
        contour (ndarray):
            The contour data
        center (tuple):
            A tuple containing the center coordinates (x, y)

    Returns:
        A float with the distance from center to the top left corner as value
    """
    x, y, _, _ = cv2.boundingRect(contour)
    return utils.distance((x, y), center[:2])
