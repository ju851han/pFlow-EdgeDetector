import numpy as np
from math import sqrt
import imageCleaner
from polygon import Polygon

image_path = "training_images/simplified_floor_plan/"
file_name = "training_images/simplified_floor_plan/O_0_1.png"
WALL_VALUE = 255  # gray-value can be used by dijkstra
FLOOR_VALUE = 0  # gray-value cannot be used by dijkstra
MAX_DISTANCE_CORNER = 20  # cluster-size for detected corners
GAUSSIAN_KERNEL_SIZE = (21, 21)  # kernel-size for blurring the image
CLOSING_BEFORE_KERNEL_SIZE = (5, 5)  # kernel-size for closing the artifacts
CLOSING_AFTER_KERNEL_SIZE = (12, 12)  # kernel-size for closing the walls


#############################
# Method for Edge-Detection #
#############################

def apply_customized_canny(image):
    """ Applies Gaussian Blur, Closing and Canny Detector according to the experiment 7 (e07_canny_combinations.py).

    :param image: image
    :return: image
    """
    image_gray = imageCleaner.transform_file_into_grayscale_image(image)
    image_blur = imageCleaner.apply_gaussian_blur(image=image_gray, kernel_size=GAUSSIAN_KERNEL_SIZE)
    image_closing = imageCleaner.apply_closing(image=image_blur, kernel_size=CLOSING_BEFORE_KERNEL_SIZE, form="ellipse")
    image_canny = imageCleaner.apply_canny_detector(image=image_closing, threshold1=125, threshold2=175)
    image_canny_finished = imageCleaner.apply_closing(image=image_canny, kernel_size=CLOSING_AFTER_KERNEL_SIZE,
                                                      form="rectangle")
    return np.float32(image_canny_finished)


################################
# Methods for Corner-Detection #
################################

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
    return all_corners


################################
# Methods for Creating Polygon #
################################

def remove_tuple_from_list(corner_list: list, corner_tuple):
    """Looks for given corner_tuple in corner_list and removes it.

    :param corner_list: list with tuples of corner; e.g. [ (1,1), (2,4)]
    :param corner_tuple: tuple of int; corner tuple to be removed from list
    :return: list of corner tuples
    """
    for i in range(len(corner_list)):
        if corner_tuple[0] == corner_list[i][0] and corner_tuple[1] == corner_list[i][1]:
            corner_list.pop(i)
            return corner_list
    return corner_list


def get_upper_right_corner(corner_list, x_step=1, y_step=1):
    """Searches the upper right corner in a given corner_list.

    :param corner_list: list with tuples of corner; e.g. [ (1,1), (2,4)]
    :param x_step: int, step-size in x-direction
    :param y_step: int, step-size in y-direction
    :return: tuple of int; tuple with coordinates of the upper right corner
    """
    x_max = 0
    y_min = 900000000000000000
    max_corner = None

    for corner in corner_list:
        x = int(corner[0] / x_step)
        y = int(corner[1] / y_step)
        if x > x_max:
            if y < y_min:
                x_max = x
                y_min = y
                max_corner = corner

    return max_corner


def check_for_corner(point, corner_list):
    """Checks if the point is close to a corner.

    :param point: tuple of int
    :param corner_list: list with tuples of corner; e.g. [ (1,1), (2,4)]
    :return: bool; If it is close to a corner, then True is returned.
    """
    for corner in corner_list:
        a = point[0] - corner[0]
        b = point[1] - corner[1]
        distance = sqrt(a ** 2 + b ** 2)
        if distance <= MAX_DISTANCE_CORNER:
            return corner
    return None


def get_neighbors(point):
    """Returns 4 neighbors of the point.

    :param point: tuple of int
    :return: list of int-tuples
    """
    return [(point[0], point[1] - 1),
            (point[0] - 1, point[1]), (point[0] + 1, point[1]),
            (point[0], point[1] + 1)]


def apply_customized_dijkstra(img, start_point=(0, 3), corner_list=[]):
    """Search for nearest corner by using Dijkstra Algorithm.

    :param img: image
    :param start_point: tuple of int
    :param corner_list: list of corners without start_point
    :return: tuple of int
    """
    point = (start_point[0], start_point[1], 1)  # x, y, cost
    cost_matrix = np.zeros(img.shape)
    job_list = [point]
    aim_point = None

    # Dijkstra:
    while len(job_list) > 0:  # FIFO = First In First Out = breadth-first search
        point = job_list.pop(0)
        cost = point[2]
        if cost_matrix[point[1]][point[0]] != 0:
            continue  # already done
        cost_matrix[point[1]][point[0]] = cost
        # Is current point a corner?
        found_corner = check_for_corner(point, corner_list)
        if found_corner is not None:
            aim_point = found_corner
            break
        neighbors = get_neighbors(point)  # 4er neighborhood
        for neighbor in neighbors:
            try:
                if neighbor[0] < 0 or neighbor[1] < 0:
                    continue  # IndexOutOfBounds without Exception for negative values
                value = img[neighbor[1]][neighbor[0]]
                if value == FLOOR_VALUE:
                    continue  # connections are only possible through wall
                elif value == WALL_VALUE:
                    if cost_matrix[neighbor[1]][neighbor[0]] > 0:
                        continue  # point already visited
                    else:
                        job_list.append((neighbor[0], neighbor[1], cost + 1))
                else:
                    raise Exception("Unreachable Code.")
            except IndexError:  # ignore IndexOutOfBounds for positive values
                continue
    return aim_point


def create_polygon(img, corner_list):
    """Creates polygon by using Dijkstra Algorithm.

    :param img: image
    :param corner_list: list with tuples of corner; e.g. [ (1,1), (2,4)]
    :return: Polygon
    """
    polygon = Polygon()
    start_corner = get_upper_right_corner(corner_list)
    corner_list = remove_tuple_from_list(corner_list, start_corner)
    polygon.add_point(start_corner[0], start_corner[1])

    while len(corner_list) > 0:
        start_corner = apply_customized_dijkstra(img=img, start_point=start_corner, corner_list=corner_list)
        if start_corner is not None:
            polygon.add_point(start_corner[0], start_corner[1])
            corner_list = remove_tuple_from_list(corner_list, start_corner)
        else:
            break
    return polygon


if __name__ == '__main__':
    # os.chdir(image_path)
    edges_img = apply_customized_canny(file_name)
    corners = imageCleaner.apply_harris_detector(edges_img)
    if len(corners) < 1:
        raise AttributeError(
            "No corners are detected. Make sure that the image is correct or change parameters.\n Current image_path value is: {}".format(
                image_path))
    cleaned_corners = get_coordinates(extract_corner_array(corners))
    int_array = edges_img.astype(int)
    polygon = create_polygon(int_array, cleaned_corners)
    while len(cleaned_corners) > 0:
        polygon.add_inner_polygons(create_polygon(int_array, cleaned_corners))
    polygon.save_to_file()
