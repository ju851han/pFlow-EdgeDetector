import cv2
from matplotlib import pyplot as plt

class ImageAnalyzer:
    def __init__(self, image):
        """Constructor

        """
        self.image = image
        if self.image is None:
            raise AttributeError("Image-file can't be found.")

    def plot_histogram(self):
        """ Displays intensity values from an image.

        :return:None
        """
        # Source : Program 3.1 Seite 49 Burge2015
        #     h = img.shape[1] # OR : np.size(img,0)    #source: https://stackoverflow.com/questions/13033278/image-size-python-opencv AND https://appdividend.com/2020/09/09/python-cv2-image-size-how-to-get-image-size-in-python/
        #     w = img.shape[0] # OR: np.size(img,1)
        #     hist = []
        #     for i in range(0,256):
        #         p.append(0)
        #     for height in range(0, h-1):
        #         for width in range(0, w-1):
        #             i = img[width, height]     #source: https://stackoverflow.com/questions/28981417/how-do-i-access-the-pixels-of-an-image-using-opencv-python
        #             hist[i]= hist[i] + 1
        hist = cv2.calcHist([self.image], [0], None, [256], [0, 256])
        plt.plot(hist)
        plt.show()