# SPDX-License-Identifier: MIT
# Copyright (c) 2019 Akumatic

import math

def distance (
        p: tuple,
        q: tuple
    ) -> float:
    """ Calculates direct distance between two points given as tuples.

    Args:
        p (tuple):
            A tuple containing x and y coordinates
        q (tuple):
            A tuple containing x and y coordinates

    Returns:
        A float with the distance between given points as value
    """
    return math.sqrt((p[0] - q[0])**2 + (p[1] - q[1])**2)

def find_closest_element (
        points: list,
        point: tuple
    ) -> tuple:
    """ Finds the closes element to a given point

    Args:
        points (list):
            A list containing tuples of coordinates (x, y)
        point (tuple):
            The (x, y) coordinates of the given point

    Returns:
        the tuple of the closest point and the distance
        between the given and closest point
    """
    start, min_dist = None, None
    for p in points:
        dist = distance(p[:2], point)
        if min_dist is None or dist < min_dist:
            start, min_dist = p, dist

    return start, min_dist


def circularity (
        area: float,
        perimeter: float
    ) -> float:
    """ Calculates the circularity shape factor with given area and perimeter.

    Args:
        area (float):
            area of a shape
        perimeter (float):
            length of the perimeter of a shape

    Returns:
        A float with the circularity shape factor as value
    """
    if perimeter == 0:
        return 0.0
    return (4 * math.pi * area) / (perimeter ** 2)