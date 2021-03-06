""" Experiment 8: Finding Corners.

    At first, Harris Corner Detector was implemented.
    Next, in order to better extract the corners, the following approaches were tested:
    1. approach was to take the first corner per cluster which is described in get_coordinates_old().
    2. approach was to calculate averaged corner per cluster which is described in get_coordinates().
    Result: second approach reflects the positions of the actual corners better than in the first approach.

"""
import numpy as np
import cv2
from experiments import imageAnalyzer
import imageCleaner
import os
from math import sqrt
import matplotlib.pyplot as plt

image_path = "../training_images/simplified_floor_plan/"
file_name = 'O_0_1.png'
MAX_DISTANCE_CORNER = 20
images = []
titles = []


def apply_customized_canny(image):
    """ Applies Gaussian Blur, Closing and Canny Detector according to the experiment 7 (e07_canny_combinations.py).

    :param image: image
    :return: image
    """
    image_gray = imageCleaner.transform_file_into_grayscale_image(image)
    images.append(image_gray)
    titles.append("Grayscale Image")

    # Customized Canny
    image_blur = imageCleaner.apply_gaussian_blur(image=image_gray, kernel_size=(21, 21))
    image_closing = imageCleaner.apply_closing(image=image_blur, kernel_size=(5, 5), form="ellipse")
    image_canny = imageCleaner.apply_canny_detector(image=image_closing, threshold1=125, threshold2=175)
    image_canny_finished = imageCleaner.apply_closing(image=image_canny, kernel_size=(12, 12), form="rectangle")
    images.append(image_canny_finished)
    titles.append("Canny Image")
    return np.float32(image_canny_finished)


def apply_harris(orig_image, canny_image):
    """ Converts image in gray-scale, applies customized Canny Edge Detector and applies Harris Detector.

    :param orig_image: str; path of the image
    :param canny_image: image; image which was preprocessed with apply_customized_canny()
    :return: bool array; If the element is True, then it is a corner
    """

    image_rgb = imageCleaner.load_image(orig_image)
    # dst = cv2.cornerHarris(canny_image, 2, 3, 0.04)
    dst = cv2.cornerHarris(src=canny_image, blockSize=2, ksize=5, k=0.05)
    image_rgb[dst > 0.01 * dst.max()] = [0, 0, 255]
    images.append(image_rgb)
    titles.append("Harris Corner Image")

    return dst > 0.01 * dst.max()


def extract_corner_array(corner_array):
    """Converts a bool array into a list with tuples of the corner coordinates

    :param corner_array: bool array; If the element is True, then it is a corner
    :return: list with tuples of corner; e.g. [ (1,1), (2,4)]
    """
    all_corners = []
    # Collect and extract found corners
    for x_coordinate in range(corner_array.shape[1]):
        for y_coordinate in range(corner_array.shape[0]):
            if corner_array[y_coordinate, x_coordinate]:
                all_corners.append((x_coordinate, y_coordinate))
    print("Number of Corners: {}".format(len(all_corners)))
    return all_corners


def get_coordinates_old(corner_list):
    """ Sorts out unnecessary corners.

    Put first corner in the corner_list. If the next corner is far enough (MAX_DISTANCE) away from corners in the corner list, then the corner will be appended to the corner_list.
    :param corner_list: list with tuples of corner; e.g. [ (1,1), (2,4)]
    :return: list with tuples of corner; e.g. [ (1,1), (2,4)]
    """
    remaining_corners = []

    for corner in corner_list:
        already_there = False
        for c in remaining_corners:
            a = corner[0] - c[0]
            b = c[1] - corner[1]
            distance = sqrt(a ** 2 + b ** 2)
            if distance < MAX_DISTANCE_CORNER:
                already_there = True
        if not already_there:
            remaining_corners.append(corner)
        # else:
        #     print("Discarded Corners {}".format(corner))

    print("Number of Corners: {}".format(len(remaining_corners)))
    return remaining_corners


def get_coordinates(corner_list):
    """ Sorts out unnecessary corners.

    Build clusters with corners that are within a certain MAX_DISTANCE.
    The average value of the corners is calculated from the respective cluster and this is the new corner point.W
    :param corner_list: list with tuples of corner; e.g. [ (1,1), (2,4)]
    :return: list with tuples of corner; e.g. [ (1,1), (2,4)]
    """
    cluster_list = []
    for corner in corner_list:
        check_find = False
        for cluster in cluster_list:
            point = cluster[0]
            a = point[0] - corner[0]
            b = point[1] - corner[1]
            distance = sqrt(a ** 2 + b ** 2)
            if distance <= MAX_DISTANCE_CORNER:
                cluster.append(corner)
                check_find = True
                break
        if not check_find:
            cluster_list.append([corner])

    final_corners = []
    for cluster in cluster_list:
        x_coordinate, y_coordinate, number_of_points = 0, 0, 0
        # calculate mean for corner point coordinates
        for point in cluster:
            x_coordinate += point[0]
            y_coordinate += point[1]
            number_of_points += 1
        x_coordinate = int(x_coordinate / number_of_points)
        y_coordinate = int(y_coordinate / number_of_points)
        final_corners.append((x_coordinate, y_coordinate))

    return final_corners


if __name__ == '__main__':
    os.chdir(image_path)
    for file_name in os.listdir(os.getcwd()):
        if file_name.lower().endswith('.png'):
            images.clear()
            titles.clear()
            corners = apply_harris(file_name, apply_customized_canny(file_name))

            final_corners_v1 = get_coordinates_old(extract_corner_array(corners))
            final_corners_v1 = np.array(final_corners_v1)     # Transform list into Array
            x, y = final_corners_v1.T
            imageAnalyzer.show_images(plot_axis=False, number_cols=2, images=images, titles=titles, window_name=file_name, show_now=False)
            plt.subplot(2, 2, 3)
            plt.scatter(x, y, marker="*", color="red")

            final_corners_v2 = get_coordinates(extract_corner_array(corners))
            final_corners_v2 = np.array(final_corners_v2)     # Transform list into Array
            x, y = final_corners_v2.T
            plt.subplot(2, 2, 3)
            plt.scatter(x, y, marker=".", color="green")

            plt.show()
