from math import sqrt
import os
import numpy as np
import matplotlib.pyplot as plt

import imageAnalyzer
from polygon import Polygon
from experiments import e09_dijkstra, e08_harris_detector

image_path = "../training_images/simplified_floor_plan/"
file_name = 'O_0_1.png'


def remove_tuple_from_list(corner_list: list, corner_tuple):
    for i in range(len(corner_list)):
        if corner_tuple[0] == corner_list[i][0] and corner_tuple[1] == corner_list[i][1]:
            corner_list.pop(i)
            return corner_list
    return corner_list


def create_polygon(img, corner_list):
    polygon = Polygon()
    start_corner = corner_list.pop(-1)
    polygon.add_point(start_corner[0], start_corner[1])

    while len(corner_list) > 0:
        start_corner = e09_dijkstra.apply_dijkstra(img=img, start_point=start_corner, corner_list=corner_list)
        if start_corner is not None:
            polygon.add_point(start_corner[0], start_corner[1])
            corner_list = remove_tuple_from_list(corner_list, start_corner)
        else:
            break
        print(corner_list)

    polygon.save_to_file()


def create_simple_polygon():
    """
    Renew e09_dijkstra.create_polygon_from_dijkstra()
    :return:
    """
    img = np.array([[0, 0, 1, 1, 1, 1, 0],
                    [0, 1, 1, 0, 0, 1, 1],
                    [1, 1, 0, 0, 0, 1, 1],
                    [1, 1, 0, 0, 0, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1]])
    corner_list = [(0, 4), (4, 0), (6, 4)]
    create_polygon(img, corner_list)


def main(img_path):
    e09_dijkstra.WALL_VALUE = 255
    e09_dijkstra.FLOOR_VALUE = 0
    e09_dijkstra.MAX_DISTANCE_CORNER = 3

    edges_img = e08_harris_detector.apply_customized_canny(img_path)
    corners = e08_harris_detector.apply_harris(img_path, edges_img)
    cleaned_corners = e08_harris_detector.get_coordinates(e08_harris_detector.extract_corner_array(corners))
    int_array = edges_img.astype(int)
    create_polygon(int_array, cleaned_corners)
    print("fertig")


if __name__ == '__main__':
    # create_simple_polygon()
    os.chdir(image_path)
    main(file_name)
