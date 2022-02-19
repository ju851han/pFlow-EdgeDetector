""" Experiment 9: Create Polygons - Part 1
    Implement and test Dijkstra Algorithm to create Polygons.
"""
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt

FLOOR_VALUE = 0
WALL_VALUE = 1
MAX_DISTANCE_CORNER = 0


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


def apply_customized_dijkstra(img, start_point=(0, 3), corner_list=[]):
    """Search for nearest corner by using Dijkstra Algorithm.

    :param img: image
    :param start_point: tuple of int
    :param corner_list: list of corners without start_point
    :return: tuple of int
    """
    point = (start_point[0], start_point[1], 1)    # x, y, cost
    cost_matrix = np.zeros(img.shape)
    job_list = [point]
    aim_point = None

    plt.imshow(img, cmap="gray")
    plt.plot(start_point[0], start_point[1], "ro")  # red o-marker
    for corner in corner_list:
        plt.plot(corner[0], corner[1], "go")  # red o-marker
    # Dijkstra:
    while len(job_list) > 0:    # FIFO = First In First Out = breadth-first search
        # print("Liste = {}".format(job_list))
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
        neighbors = get_neighbors(point)    # 4er neighborhood
        for neighbor in neighbors:
            try:
                if neighbor[0] < 0 or neighbor[1] < 0:
                    continue     # IndexOutOfBounds without Exception for negative values
                value = img[neighbor[1]][neighbor[0]]
                # print(value)
                if value == FLOOR_VALUE:
                    continue    # connections are only possible through wall
                elif value == WALL_VALUE:
                    if cost_matrix[neighbor[1]][neighbor[0]] > 0:
                        continue    # point already visited
                    else:
                        job_list.append((neighbor[0], neighbor[1], cost+1))
                else:
                    raise Exception("Unreachable Code.")
            except IndexError:  # ignore IndexOutOfBounds for positive values
                continue
    plt.figure("Cost Matrix")
    plt.imshow(cost_matrix, cmap="gray")
    plt.plot(start_point[0], start_point[1], "ro")  # red o-marker
    print(aim_point)
    if aim_point is not None:
        plt.plot([start_point[0], aim_point[0]], [start_point[1], aim_point[1]],  color="blue", linestyle="-", linewidth=2)
    for corner in corner_list:
        plt.plot(corner[0], corner[1], "go")  # green o-marker
    plt.show()
    return aim_point


def get_neighbors(point):
    """Returns 4 neighbors of the point.

    :param point: tuple of int
    :return: list of int-tuples
    """
    return [(point[0], point[1] - 1),
            (point[0] - 1, point[1]), (point[0] + 1, point[1]),
            (point[0], point[1] + 1)]


def simple_dijkstra():
    """Test method for apply_customized_dijkstra() with a simple image.

    :return: None
    """
    img = np.array([[0, 0, 1, 1, 1],
                    [0, 1, 1, 1, 1],
                    [1, 1, 0, 0, 1],
                    [1, 1, 1, 1, 1]])

    apply_customized_dijkstra(img)


def create_polygon_from_dijkstra():
    """Test method for apply_customized_dijkstra() with a bigger image and 3 corners.

    :return: None
    """
    img = np.array([[0, 0, 1, 1, 1, 1, 0],
                    [0, 1, 1, 0, 0, 1, 1],
                    [1, 1, 0, 0, 0, 1, 1],
                    [1, 1, 0, 0, 0, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1]])

    apply_customized_dijkstra(img, (0, 4), [(4, 0), (6, 4)])


if __name__ == '__main__':
    # simple_dijkstra()
    create_polygon_from_dijkstra()
