"""Performance test for searching the triangle in which given points are."""

import numpy as np
import time

from point_generator import import_mesh

nodes = []
triangles = []
random_points = []


def start_up():
    global nodes, triangles, random_points

    nodes, triangles = import_mesh()
    random_points = read_random_points()
    pass


# ToDo define file on top
#def read_random_points(path='random_points/middle_points.txt'):
def read_random_points(path='random_points/random_points_random_triangles.txt'):
    """Function to read files with random points"""
    points = []
    with open(path, "r") as f:
        while True:
            split_line = f.readline().split("\t")

            # if end of file is reached
            if len(split_line) < 2:
                break

            points.append((float(split_line[0]), float(split_line[1])))

    return points


def test():
    point_triangle_mapping = []

    print('Test Starting!')
    start_time = int(time.time() * 1000)

    for i in range(len(random_points)):
        point_triangle_mapping.append(find_triangle(random_points[i]))

    end_time = int(time.time() * 1000)
    print('Test finished')
    print(str(end_time - start_time) + ' ms')
    print(str((end_time - start_time) / 1000) + ' s')

    pass


def find_triangle(point):
    for current_tri_number in range(len(triangles)):
        tri = triangles[current_tri_number]

        # calculate area of tri
        tri_copy = tri.copy()
        # ToDo Change set to List, see screenshot
        p1 = tri_copy.pop()
        p2 = tri_copy.pop()
        p3 = tri_copy.pop()

        a = nodes[p1]
        b = nodes[p2]
        c = nodes[p3]
        area = np.round(calculate_triangle_area(a, b, c), 4)

        # calculate 3 areas of tri with middle point and add them
        area1 = calculate_triangle_area(a, b, point)
        area2 = calculate_triangle_area(a, point, c)
        area3 = calculate_triangle_area(point, b, c)

        # ToDo Get rid of round and make it with a smart threshhold
        area_sum = np.round(area1 + area2 + area3, 4)

        # see if area equals
        if area_sum == area:
            return current_tri_number

    print('Error: Could find a fitting triangle for point P(' + str(point[0]) + ',' + str(point[1]) + ').')
    return -1


def calculate_triangle_area(a, b, c):
    """Calculates the performance optimized area of a triangle with given points a, b and c. Points ned to be
    a two tuple with x and y coordinates."""
    ab = (b[0] - a[0], b[1] - a[1])
    ac = (c[0] - a[0], c[1] - a[1])
    # Cross product
    area = (ab[0] * ac[1]) - (ac[0] * ab[1])

    if area < 0:
        return -area
    return area


def clean_up():
    pass


def main():
    start_up()
    test()
    clean_up()


if __name__ == "__main__":
    main()

