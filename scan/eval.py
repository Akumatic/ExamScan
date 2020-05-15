# SPDX-License-Identifier: MIT
# Copyright (c) 2019 Akumatic

from . import utils

def evaluate (
        centers: list,
        n: int,
        radius: int
    ) -> list:
    """ Evaluates the given data

    Args:
        centers (list):
            contains tuples with coordinates and the black-pixel-ratio
                (x, y, ratio)
        n (int):
            the number of possible answers per question
        radius (int):
            the radius of the circle around a box

    Returns:
        A list containings lists with evaluated answers
    """
    start_of_file, _ = utils.find_closest_element(centers, (0,0))

    # detect distance to next field on the right side
    point_1 = start_of_file
    point_r = find_next(centers, point_1, 2* radius, "r")
    dist_r = utils.distance(point_1[:2], point_r[:2])
    
    # detect distance to next field below
    point_d = find_next(centers, point_1, 2 * radius, "d")
    dist_d = utils.distance(point_1[:2], point_d[:2])
    
    # detect distance to the next set of answers
    for i in range(n - 2):
        point_r = find_next(centers, point_r, dist_r, "r")

    point_3 = find_next(centers, point_r, 3 * radius, "r", max_dist=dist_r)
    if point_3 is not None:
        dist_set = utils.distance(start_of_file, point_3)
    else:
        dist_set = None

    answers = eval_set(start_of_file, centers, n, dist_r, dist_d)
    if dist_set is not None:
        cur = find_next(centers, start_of_file, dist_set, "r", max_dist = radius)
        while cur is not None:
            answers += eval_set(cur, centers, n, dist_r, dist_d)
            cur = find_next(centers, cur, dist_set, "r", max_dist = radius) 

    return answers

def eval_set (
        start: tuple,
        centers: list,
        n: int,
        dist_r: int,
        dist_d: int
    ) -> list:
    """ Evaluates a set of answers

    Args:
        start (tuple):
            Containing the coordinates of the top left answer of a set
        centers (list):
            contains tuples with coordinates and the black-pixel-ratio
                (x, y, ratio)
        n (int):
            the number of possible answers per question
        dist_r (int):
            the horizontal distance between two columns of answers
        dist_d (int):
            the vertical distance between two rows of answers

    Returns:
        A list containing all evaluated data
    """
    result = []
    result.append(eval_row(start, centers, n, dist_r))

    cur = start
    while cur != None:
        cur = find_next(centers, cur, dist_d, "d", max_dist=dist_r / 2)
        if cur is not None:
            result.append(eval_row(cur, centers, n, dist_r))
    return result

def eval_row (
        start: tuple,
        centers: int,
        n: int,
        dist_r: int
    ) -> list:
    """ Evaluates a row of a set of answers with length n
    
    Args:
        start (tuple):
            Containing the coordinates of the top left answer of a set
        centers (list):
            contains tuples with coordinates and the black-pixel-ratio
                (x, y, ratio)
        n (int):
            the number of possible answers per question
        dist_r (int):
            the horizontal distance between two columns of answers

    Returns:
        A list containing all evaluated answer data from a given row
    """
    result = []
    result.append(rate_black_pixel_ratio(start[2]))

    cur = start
    for i in range(n - 1):
        cur = find_next(centers, cur, dist_r, "r")
        result.append(rate_black_pixel_ratio(cur[2]))

    return result

def rate_black_pixel_ratio (
        ratio: int,
        thres_1: int = 20,
        thres_2: int = 50
    ) -> int:
    """ Evaluates the given black-pixel-ratio and returns the detected marking.

    Args:
        ratio (int):
            the ratio of black pixels compared to total pixels
        thres_1 (int):
            threshold for checked boxes
        thres_2 (int):
            threshold for corrected boxes

    Returns:
        -1 if a box is filled
        1 if a box is checked
        0 if a box is empty
    """
    if ratio >= thres_2:
        return -1 # corrected box
    if ratio >= thres_1:
        return 1 # checked
    else: # empty box
        return 0

def find_next (
    centers: list,
    cur: tuple,
    dist: int,
    dir: str,
    max_dist: int = None
    ):
    """ Finds the next point in a given direction with a given distance
    
    Args:
        centers (list):
            contains tuples with coordinates and the black-pixel-ratio
                (x, y, ratio)
        cur (tuple):
            the current point
        dist (int):
            approximated distance to the next point
        dir (str):
            direction of the distance. can be either "r" or "d"
        max_dist (int):
            max distance to be allowe

    Returns: 
        returns the next found point.
        if max_dist is given, returns None if distance > max_dist
    """
    if dir == "r":
        e, d = utils.find_closest_element(centers, (cur[0] + dist, cur[1]))

    elif dir == "d":
        e, d = utils.find_closest_element(centers, (cur[0], cur[1] + dist))

    if max_dist is None or d <= max_dist:
        return e
    return None

def compare(
        data_a: list,
        data_b: list
    ):
    """ Compares two sets of evaluated data with the same

    Args:
        data_a (list):
            data set A
        data_b (list):
            data set B
            
    Returns:
        A String "Correct/Total Answers" and the percentage
    """
    # asserts the number of questions is the same
    assert len(data_a) == len(data_b)
    cnt = 0
    for i in range(len(data_a)):
        if data_a[i] == data_b[i]:
            cnt += 1

    return (f"{cnt}/{len(data_a)}", cnt / len(data_a) * 100)