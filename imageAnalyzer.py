import cv2
from matplotlib import pyplot as plt
import numpy as np


class ImageAnalyzer:
    def __init__(self, image):
        """Constructor

        """
        self.image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        if self.image is None:
            raise AttributeError("Image-file can't be found.")

    def plot_grayscale_histogram(self, mask=None):
        """ Displays intensity values from an image.

        :return:None
        """
        hist = cv2.calcHist([self.image], [0], mask, [256], [0, 256])
        plt.figure()
        plt.title('Grayscale Histogram')
        plt.xlabel('Bins')
        plt.ylabel('Number of Pixels')
        plt.plot(hist)
        plt.xlim([0, 256])
        plt.show()

    def create_mask(self):
        """ circle in the middle of the image.

        :return: mask
        """
        blank = np.zeros(self.image.shape[:2], dtype='uint8')
        circle = cv2.circle(img=blank, center=(self.image.shape[1] // 2, self.image.shape[0] // 2), radius=100, color=2)
        return cv2.bitwise_and(src1=self.image, src2=self.image, mask=circle)

    def plot_color_histogram(self, mask=None):
        """

        :param mask:
        :return:
        """
        colors = ('b', 'g', 'r')
        for i, color in enumerate(colors):
            hist = cv2.calcHist([self.image], [i], mask, [256], [0, 256])
            plt.plot(hist, color)

        plt.figure()
        plt.title('Colorful Histogram')
        plt.xlabel('Bins')
        plt.ylabel('Number of Pixels')
        plt.xlim([0, 256])
        plt.show()
