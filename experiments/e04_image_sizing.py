""" Experiment 4: Sizing, snipping and rotating images for displaying in pFlowGRID.

"""
import os
import imageCleaner

WINDOW_WIDTH = 1300
WINDOW_HEIGHT = 610


def resize_image(image_path):
    """ Resizes the image with distortion.

    :return: image
    """
    image = imageCleaner.transform_file_into_grayscale_image(image_path)
    image = imageCleaner.resize_image(image)
    imageCleaner.show_image(image, 1, 'Adjusting the Image Size', True)
    return image


def resize_image_without_distortion(image_path):
    """ Resizes the image so that it can be displayed in pFlowGRID.

    :param image_path: str
    :return: image
    """
    image = imageCleaner.transform_file_into_grayscale_image(image_path)
    return imageCleaner.resize_image_without_distortion(image)


def snip_image(image_path):
    """ Snips the image so that it can be displayed in pFlow_Grid.

    :type image_path: str
    :return: image
    """
    image = imageCleaner.transform_file_into_grayscale_image(image_path)
    image = imageCleaner.snip_image(image, 0, 500, 0, 250)
    imageCleaner.show_image(image, 1, 'Snipped Image', True)
    return image


def rotate_floor_plan():
    """ Rotates the image.

    :return: None
    """
    try:
        floor_plan = imageCleaner.transform_file_into_grayscale_image("../training_images/floor_plan/005_wry.png")
    except FileNotFoundError: 
        floor_plan = imageCleaner.transform_file_into_grayscale_image("005_wry.png")

    floor_plan = imageCleaner.rotate_image(floor_plan, 43 - 90)
    imageCleaner.show_image(floor_plan, 1, 'Rotated Floor Plan', True)


os.chdir('../training_images/floor_plan')
for file_name in os.listdir(os.getcwd()):
    if file_name.lower().endswith('.png'):
        # sized_image = resize_image(file_name)
        sized_image = resize_image_without_distortion(file_name)
        imageCleaner.show_image(sized_image, 1, 'sized image', True)
        # cut_image = snip_image(file_name)

rotate_floor_plan()
