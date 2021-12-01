import cv2


class ImageCleaner:
    """

    """

    def __init__(self, image_path):
        """Constructor

        flags=0 in cv2.imread()-method means that the passed image is transformed as a gray value image.
        If no flags have been set, the image is colored.
        """
        self.image = cv2.imread(filename=image_path)  # , flags=0)
        if self.image is None:
            raise AttributeError("Image-file can't be found. The affected image-path is:" + image_path)

    def show_image(self, scale=1):
        """Displays a Picture

        :param scale: int between [0,1]
        :return: None
        """
        if scale < 0 or scale > 1:
            raise ValueError("Scale must be between 0 and 1.\nCurrent value of the scale: " + str(scale))
        else:
            width = int(self.image.shape[1] * scale)
            height = int(self.image.shape[0] * scale)
            dimensions = (width, height)
            frame_resized = cv2.resize(self.image, dimensions, interpolation=cv2.INTER_AREA)
            cv2.imshow('Image', frame_resized)
            cv2.waitKey(0)

    def transform_colored_into_gray_img(self):
        """Changes a color image into a gray value image and overwrites the variable image.

        :return: None
        """
        self.image = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)

    def add_gaussian_blur(self, kernel_size=(3, 3)):
        """

        ksize in cv2.GussianBlur() is an abbreviation for kernel size
        If ksize is high (e.g.: (7,7)), then the noise is also high.
        If ksize is low (e.g.: (3,3)), then the noise is also low.
        Hint: If the apply_canny_filter() is called after add_gussian_blur, then the noises are removed
        :return: None
        """
        self.image = cv2.GaussianBlur(src=self.image, ksize=kernel_size, borderType=cv2.BORDER_DEFAULT)

    def apply_canny_filter(self):
        """Places a Filter according to the Canny Edge Algorithm over the image and overwrites the variable image.

        Hint: If a blurred image is passed, then fewer edges are detected
        :return: None
        """
        self.image = cv2.Canny(image=self.image, threshold1=125, threshold2=175)  # TODO threshhold bestimmen
