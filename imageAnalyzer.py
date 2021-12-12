import cv2
from matplotlib import pyplot as plt
import numpy as np


class ImageAnalyzer:
    def __init__(self, image):
        """Constructor

        If length of image shape is 2, then it is a gray scale image, else it is a color image.
        :param image: is an image, which is already read with cv2.imread()
        """
        self.gray = (len(image.shape) == 2)
        self.image = image

        if self.image is None:
            raise AttributeError("Image-file can't be found.")

    def show_image(self, name='Image', show_now=True, contrast_auto=False):
        """Displays a Picture.

        :param contrast_auto: bool; If it is True then the contrast is maximized.
        :param name: str; name of the window
        :param show_now: bool; If it is True, then the image is shown.
        :return: None
        """
        plt.figure(name)
        if self.gray:
            if contrast_auto:
                plt.imshow(X=self.image, cmap="gray")
            else:
                plt.imshow(X=self.image, cmap="gray", vmin=0, vmax=255)
        else:
            plt.imshow(X=self.image)
        if show_now:
            plt.show()

    def plot_histogram(self, mask=None, show_hist=True):
        """ Displays grayscale or rgb histogramm depending on the image

        :param show_hist: bool; True: firstly calculates histogram and secondly shows histogram(s).
                                False: Only calculates histogram
        :param mask: mask; The mask helps to find out which intensity values are in the selected area
        :return: None
        """
        if self.gray:
            self.__plot_grayscale_histogram(mask)
        else:
            self.__plot_rgb_histogram(mask)
        if show_hist:
            plt.show()

    def __plot_grayscale_histogram(self, mask=None):
        """ Displays intensity values from an image.

        :return:None
        """
        hist = cv2.calcHist([self.image], [0], mask, [256], [0, 256])
        plt.figure('Grayscale Histogram')    # create new window for histogram
        plt.title('Grayscale Histogram')
        plt.xlabel('Bins')
        plt.ylabel('Number of Pixels')
        plt.plot(hist, color='black')
        plt.xlim([0, 256])

    def __plot_rgb_histogram(self, mask=None):
        """ Displays the red, green, blue parts of the intensity values in an image.

        :param mask: mask; The mask helps to find out which intensity values are in the selected area
        :return: None
        """
        plt.figure('RGB Histogram')    # create new window for histogram
        plt.title('RGB Histogram')
        plt.xlabel('Bins')
        plt.ylabel('Number of Pixels')

        colors = ('r', 'g', 'b')
        for i, color in enumerate(colors):
            hist = cv2.calcHist(images=[self.image], channels=[i], mask=mask, histSize=[256], ranges=[0, 256])
            plt.plot(hist, color=color)

        plt.xlim([0, 256])

    def create_round_mask(self, center=None, radius=100):
        """ Creates a focus-circle in the middle of the image.

        Usage: The mask helps to find out which intensity values are in the circled area.
        :param center: tuple of int ( x-coordinate, y-coordinate) for mask
                        if it is None then the masked is placed in the middle of the image.
        :param radius: int; radius for mask
        :return: mask
        """
        if center is None:
            center = (self.image.shape[1] // 2, self.image.shape[0] // 2)

        blank = np.zeros(self.image.shape[:2], dtype='uint8')
        circle = cv2.circle(img=blank, center=center, radius=radius,
                            color=255, thickness=-1)
        # cv2.imshow('Mask', cv2.bitwise_and(src1=self.image, src2=self.image, mask=circle))
        # cv2.waitKey(0)
        plt.imshow(cv2.bitwise_and(src1=self.image, src2=self.image, mask=circle))
        plt.show()
        return circle
