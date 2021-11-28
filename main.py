# import section
from polygon import Polygon


# parameter section (class variables)


# function definition section
def save_rectangle():
    """
    Stores a rectangle
    :return: None
    """
    rectangle = Polygon()
    rectangle.add_point(100, 100)
    rectangle.add_point(100, 500)
    rectangle.add_point(800, 500)
    rectangle.add_point(800, 100)
    rectangle.save_to_file()


def save_polygon(point_list, file="polygon.nsv"):
    """
    Stores a polygon
    :param point_list: list with points which are tuples(x-coordinate, value of y-coordinate)
    :param file: path of file
    :return: None
    """
    polygon = Polygon()
    for point in point_list:
        polygon.add_point(point[0], point[1])
    polygon.save_to_file(file)


# execute section
# save_rectangle()
save_polygon([(20, 50), (30, 10), (25, 70)])


# window_width = "1300" , window_height = "610"
