import math
import cv2
from matplotlib import pyplot as plt
import numpy as np

MIN_GRAY_VALUE = 0
MAX_GRAY_VALUE = 255


def check_gray(image):
    """ Checks if the image is grayscale.

    :param image: image
    :return: bool; If it is True, then the image is grayscale.
    """
    return 2 == len(image.shape)


def show_image(image, window_name='Image', title=None, show_now=True, contrast_auto=False, plot_axis=False):
    """ Displays an image.

    :param title: str; Headline of the Image
    :param image: image
    :param contrast_auto: bool; If it is True then the contrast is maximized.
    :param window_name: str; name of the window
    :param show_now: bool; If it is True, then the image is shown.
    :param plot_axis: bool;  If it is True, then the axis are shown.
    :return: None
    """
    plt.figure(window_name)
    if title is not None:
        plt.title(title)
    if plot_axis:
        plt.xlabel('Number of Pixels')
        plt.ylabel('Bins')
    plt.axis(plot_axis)
    if check_gray(image):
        if contrast_auto:
            plt.imshow(X=image, cmap="gray")
        else:
            plt.imshow(X=image, cmap="gray", vmin=0, vmax=255)
    else:
        plt.imshow(X=image)
    if show_now:
        plt.show()


def show_images(plot_axis=True, number_cols=2, images=[], titles=None, window_name="Image", show_now=True):
    """ Displays images in only one window.

    :param titles: str or list of str or None; title of the image
    :param number_cols: int
    :param window_name: str
    :param plot_axis: bool;  If it is True, then the axis are shown.
    :param images: list of images
    :param show_now: bool; If it is True, then the image is shown.
    :return: None;
    """
    if images is None:
        images = []
    number_rows = int(math.ceil(len(images) / number_cols))
    plt.figure(window_name)
    plt.subplots_adjust(hspace=0.1, wspace=0.1)
    for i in range(len(images)):
        plt.subplot(number_rows, number_cols, i+1)
        plt.axis(plot_axis)
        if titles is None:
            plt.title("{} {}".format(window_name, i))
        else:
            plt.title(titles[i])
        plt.imshow(images[i], cmap="gray")
    if show_now:
        plt.show()
    # TODO show images + plots


def plot_histogram(image, mask=None, show_hist=True):
    """ Displays grayscale or rgb histogram depending on the image.

    :param image: image
    :param show_hist: bool; True: firstly calculates histogram and secondly shows histogram(s).
                            False: Only calculates histogram
    :param mask: mask; The mask helps to find out which intensity values are in the selected area
    :return: None
    """
    if check_gray(image):
        __plot_grayscale_histogram(image, mask)
    else:
        __plot_rgb_histogram(image, mask)
    if show_hist:
        plt.show()


def __plot_grayscale_histogram(image, mask=None):
    """ Displays intensity values from an image.

    :param image: image
    :param mask: mask; The mask helps to find out which intensity values are in the selected area
    :return: None
    """
    hist = cv2.calcHist([image], [0], mask, [MAX_GRAY_VALUE], [MIN_GRAY_VALUE, MAX_GRAY_VALUE])
    plt.figure('Grayscale Histogram')  # create new window for histogram
    plt.title('Grayscale Histogram')
    plt.xlabel('Bins')
    plt.ylabel('Number of Pixels')
    plt.plot(hist, color='black')
    plt.xlim([MIN_GRAY_VALUE, MAX_GRAY_VALUE])


def __plot_rgb_histogram(image, mask=None):
    """ Displays the red, green, blue parts of the intensity values in an image.

    :param image: image
    :param mask: mask; The mask helps to find out which intensity values are in the selected area
    :return: None
    """
    plt.figure('RGB Histogram')  # create new window for histogram
    plt.title('RGB Histogram')
    plt.xlabel('Bins')
    plt.ylabel('Number of Pixels')

    colors = ('r', 'g', 'b')
    for channels, color in enumerate(colors):
        hist = cv2.calcHist(images=[image], channels=[channels], mask=mask, histSize=[MAX_GRAY_VALUE], ranges=[MIN_GRAY_VALUE, MAX_GRAY_VALUE])
        plt.plot(hist, color=color)

    plt.xlim([MIN_GRAY_VALUE, MAX_GRAY_VALUE])


def create_round_mask(image, center=None, radius=100):
    """ Creates a focus-circle in the middle of the image.

    Usage: The mask helps to find out which intensity values are in the circled area.
    :param image: image
    :param center: tuple of int ( x-coordinate, y-coordinate) for mask
                    if it is None then the masked is placed in the middle of the image.
    :param radius: int; radius for mask
    :return: mask; The mask helps to find out which intensity values are in the selected area
    """
    if center is None:
        center = (image.shape[1] // 2, image.shape[0] // 2)

    blank = np.zeros(image.shape[:2], dtype='uint8')
    circle = cv2.circle(img=blank, center=center, radius=radius,
                        color=255, thickness=-1)
    if check_gray(image):
        plt.imshow(cv2.bitwise_and(src1=image, src2=image, mask=circle), cmap="gray")
    else:
        plt.imshow(cv2.bitwise_and(src1=image, src2=image, mask=circle))
    return circle
