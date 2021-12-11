# IMPORT SECTION
from polygon import Polygon
from imageCleaner import ImageCleaner
from imageAnalyzer import ImageAnalyzer
import os


# PARAMETER SECTION


# FUNCTION DEFINITION SECTION
def save_rectangle():
    """Stores nodes (=points, corners) of rectangle

    :return: None
    """
    r = Polygon()
    r.add_point(100, 100)
    r.add_point(100, 500)
    r.add_point(800, 500)
    r.add_point(800, 100)
    r.save_to_file()


def save_polygon(point_list, file="polygon.nsv"):
    """Stores nodes (=points, corners) of a polygon

    :param point_list: list with points which are tuples(x-coordinate, value of y-coordinate)
    :param file: path of file
    :return: None
    """
    polygon = create_polygon(point_list)
    polygon.save_to_file(file)


def create_polygon(point_list):
    """Creates nodes (=points, corners) of a polygon

    :param point_list: list with points which are tuples(x-coordinate, value of y-coordinate)
    :return: Polygon
    """
    if len(point_list) < 3:
        raise Exception('This is not a polygon. A polygon must have more than 2 points.\n'
                        'Number of points which were given in the list:' + str(len(point_list)))
    polygon = Polygon()
    for point in point_list:
        polygon.add_point(point[0], point[1])
    return polygon


def save_polygons():
    """Create and save a polygon with 2 inner polygons.

    :return: None
    """
    rectangle = create_polygon([(100, 100), (100, 500), (800, 500), (800, 100)])
    obstacle1 = create_polygon([(120, 150), (130, 110), (125, 170)])
    obstacle2 = create_polygon([(600, 270), (600, 350), (650, 350), (650, 270)])
    rectangle.add_inner_polygons(obstacle1)
    rectangle.add_inner_polygons(obstacle2)
    rectangle.save_to_file("polygon_with_inner_obstacles.nsv")


# EXECUTE SECTION

# Polygon-Class
# save_rectangle()
# save_polygons()

# ImageCleaner-Class

os.chdir('training_images')
for file_name in os.listdir(os.getcwd()):
    if file_name.lower().endswith('.png') or file_name.lower().endswith('.jpg'):
        ic = ImageCleaner(image_path=file_name)
        print(file_name)
        # ic.show_image(title='Original Image', wait_for_close=False)

        # IMAGE SIZING
        # ic.resize_image(1300, 610)
        # ic.snip_image(0, 1300, 0, 610)
        # ic.show_image(title='Adjusting the Image Size')

        # POINT OPERATIONS
        # ic.transform_colored_into_gray_img()
        # ic.show_image(title='Gray Image', wait_for_close=True)
        # ic.apply_simple_threshold(threshold=180)
        # ic.apply_adaptive_threshold(neighborhood_size=51)
        # ic.change_color_in_area(130, 170, 370, 430, 0, 128, 255)
        # ic.change_color_in_pixel(5, 5)
        # ic.show_image(title='Changed Color in Area', wait_for_close=True)

        # FILTERS
        # ic.add_gaussian_blur()
        # ic.add_average_blur()
        # ic.add_median_blur()
        # ic.add_bilateral_blur()
        # ic.show_image(title='Blurred Image')

        # EDGES
        # ic.apply_canny_filter()
        # ic.show_image(title='Canny Image', wait_for_close=True)

        # HISTOGRAM
        ia = ImageAnalyzer(ic.image)
        # ia.plot_histogram(show_hist=False)
        # ia.plot_histogram(mask=ia.create_round_mask(), show_hist=False)
        # ia.plot_histogram(ia.create_round_mask(center=(500, 700), radius=350))  # Dog-face
        ia.show_image()

# pFlowGRID: window_width = "1300" , window_height = "610"
