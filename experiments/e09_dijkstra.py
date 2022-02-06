""" Experiment 9: Create Polygons

"""
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt

FLOOR_VALUE = 0
WALL_VALUE = 1
MAX_DISTANCE_CORNER = 0


def check_for_corner(point, corner_list):
    """Checks if the point is a corner?

    :param point:
    :param corner_list: list of corners
    :return: bool; If it is a corner, then True is returned.
    """
    for corner in corner_list:
        a = point[0] - corner[0]
        b = point[1] - corner[1]
        distance = sqrt(a ** 2 + b ** 2)
        if distance <= MAX_DISTANCE_CORNER:
            return True
    return False


def apply_dijkstra(img, start_point=(0, 3), corner_list=[]):
    """

    :param img:
    :param start_point:
    :param corner_list: corner list without start_point
    :return:
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
        if check_for_corner(point, corner_list):
            aim_point = point
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
    return [(point[0], point[1] - 1),
            (point[0] - 1, point[1]), (point[0] + 1, point[1]),
            (point[0], point[1] + 1)]


def simple_dijkstra():
    img = np.array([[0, 0, 1, 1, 1],
                    [0, 1, 1, 1, 1],
                    [1, 1, 0, 0, 1],
                    [1, 1, 1, 1, 1]])

    apply_dijkstra(img)


def create_polygon_from_dijkstra():
    img = np.array([[0, 0, 1, 1, 1, 1, 0],
                    [0, 1, 1, 0, 0, 1, 1],
                    [1, 1, 0, 0, 0, 1, 1],
                    [1, 1, 0, 0, 0, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1]])

    apply_dijkstra(img, (0, 4), [(4, 0), (6, 4)])   #TODO pass cornerliste without startpoint


if __name__ == '__main__':
    # simple_dijkstra()
    create_polygon_from_dijkstra()
