""" Experiment 5: Executes different point operations: Thresholding, changing Colors and inverting images-

    Result of apply_threshold():
    adaptive_threshold-method is for natural images because the structure from the tree and dog (e.g. of the Dog.png) still intact .
    simple_threshold-method is good for floor_plans.
    Outlook: Canny Edge Detector uses a Hysterese Threshold which will be described in #TODO Ref
"""
import os
import imageCleaner

os.chdir('../training_images')


def apply_threshold(gray_image):
    """ Binaries the image. One time the simple and second time the adaptive threshold will be applied and the result will be displayed.

    :param gray_image: image
    :return: None
    """
    simple_thresh = imageCleaner.apply_simple_threshold(image=gray_image, threshold=180)
    imageCleaner.show_image(image=simple_thresh, title='Simple Threshold', wait_for_close=True)
    adaptive_thresh = imageCleaner.apply_adaptive_threshold(image=gray_image, neighborhood_size=51)
    imageCleaner.show_image(image=adaptive_thresh, title='Adaptive Threshold', wait_for_close=True)


def change_color(image):
    """Marking an area (pixel) of the image.

    :param image: image
    :return: None
    """
    colorful_image = imageCleaner.change_color_in_area(image, 130, 170, 370, 430, 0, 128, 255)
    # imageCleaner.change_color_in_pixel(image, 5, 5)
    imageCleaner.show_image(image=colorful_image, title='Changed Color in Area', wait_for_close=True)


for file_name in os.listdir(os.getcwd()):
    if file_name.lower().endswith('.png'):
        image = file_name

        image = imageCleaner.transform_file_into_grayscale_image(file_name)
        imageCleaner.show_image(image=image, title='Gray Image', wait_for_close=True)

        apply_threshold(image)

        change_color(image)

        imageCleaner.invert_image(image)
        imageCleaner.show_image(image=image, title='Inverted Image', wait_for_close=True)
