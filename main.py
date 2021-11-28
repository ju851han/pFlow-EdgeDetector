# import section
from polygon import Polygon


# parameter section (class variables)


# function definition section
def save_rectangle():
    """
    Stores nodes (=points, corners) of rectangle
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
    Stores nodes (=points, corners) of a polygon
    :param point_list: list with points which are tuples(x-coordinate, value of y-coordinate)
    :param file: path of file
    :return: None
    """
    polygon = create_polygon(point_list)
    polygon.save_to_file(file)


def create_polygon(point_list):
    """
    Creates nodes (=points, corners) of a polygon
    :param point_list: list with points which are tuples(x-coordinate, value of y-coordinate)
    :return: Polygon
    """
    polygon = Polygon()
    for point in point_list:
        polygon.add_point(point[0], point[1])
    return polygon


# execute section
# save_rectangle()
rectangle = create_polygon([(100, 100), (100, 500), (800, 500), (800, 100)])
obstacle1 = create_polygon([(120, 150), (130, 110), (125, 170)])
obstacle2 = create_polygon([(600, 270), (600, 350), (650, 350), (650, 270)])
rectangle.add_inner_polygons(obstacle1)
rectangle.add_inner_polygons(obstacle2)
rectangle.save_to_file("polygon_with_inner_obstacles.nsv")

# window_width = "1300" , window_height = "610"
