import cv2


class ImageCleaner:
    """Class for Loading and Processing Images (Pictures)

    """

    def __init__(self, image_path):
        """Constructor

        flags=0 in cv2.imread()-method means that the passed image is transformed as a gray value image.
        If no flags have been set, the image is colored.
        :param image_path: str
        """
        self.image = cv2.imread(filename=image_path)  # , flags=0)
        if self.image is None:
            raise AttributeError("Image-file can't be found. The affected image-path is:" + image_path)

    def show_image(self, scale=1, title='Image', wait_for_close=False):
        """Displays a Picture.

        :param wait_for_close: bool; if this is True, then the window will be closed as soon a button is pressed
        :param title: str; text for window frame
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
            cv2.imshow(title, frame_resized)
            if wait_for_close:
                cv2.waitKey(0)

    ################
    # IMAGE SIZING #
    ################

    def resize_image(self, x, y):
        """ Changes the size of the image.

        :param x: int; size of the x-axis
        :param y: int; size of the y-axis
        :return: None
        """
        orig_width = int(self.image.shape[1])
        orig_height = int(self.image.shape[0])
        if x < orig_width or y < orig_height:
            self.image = cv2.resize(src=self.image, dsize=(x, y), interpolation=cv2.INTER_AREA)
        else:
            self.image = cv2.resize(src=self.image, dsize=(x, y),
                                    interpolation=cv2.INTER_CUBIC)  # TODO welche Interpolation ist besser? z80 oder z 81?
            self.image = cv2.resize(src=self.image, dsize=(x, y), interpolation=cv2.INTER_LINEAR)

    def snip_image(self, x_min, x_max, y_min, y_max):
        """ Cuts out an image. The result is a cropped image.

        :param x_min: int; start on the x-axis
        :param x_max: int; end on the x-axis
        :param y_min: int; start on the y-axis
        :param y_max: int; end on the y-axis
        :return: None
        """
        self.image = self.image[x_min:x_max, y_min:y_max]

    ####################
    # POINT OPERATIONS #
    ####################
    """
    Homogeneous point operations are independent of pixel coordinate.
    Non-homogeneous point operations depend on pixel coordinate.
    """

    def transform_colored_into_gray_img(self):
        """Homogeneous point operation: Changes a color image into a gray value image and overwrites the variable image.

        :return: None
        """
        self.image = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)

    def change_color_in_area(self, y_min, y_max, x_min, x_max, blue=0, green=0, red=0):
        """Non-homogeneous point operation: Changes color in an image area

        y_min, y_max: variables for y-axis; 0 is at top, max is at bottom
        x_min, x_max: variables for x-axis; 0 is in the left corner, max is on the right side
        :param y_min: int
        :param y_max: int
        :param x_min: int
        :param x_max: int
        :param blue: int
        :param green: int
        :param red: int
        :return: None
        """
        self.image[y_min:y_max, x_min:x_max] = blue, green, red
        cv2.imshow('Colorful Area', self.image)
        cv2.waitKey(0)

    def change_color_in_pixel(self, y, x, blue=0, green=0, red=0):
        """Non-homogeneous point operation: Changes color only in one pixel.

        :param y: int; variable for y-axis; 0 is at top, max is at bottom.
        :param x: int; variables for x-axis; 0 is in the left corner, max is on the right side.
        :param blue: int
        :param green: int
        :param red: int
        :return: None
        """
        self.image[y, x] = blue, green, red
        cv2.imshow('Colorful Pixel', self.image)
        cv2.waitKey(0)

    ###########
    # FILTERS #
    ###########

    def add_gaussian_blur(self, kernel_size=(3, 3)):
        """Smooth the image.

        ksize in cv2.GussianBlur() is an abbreviation for kernel size
        If the noise is also high, then a high ksize is recommended (e.g.: (7,7)).
        If the noise is also low, then a smaller ksize is recommended (e.g.: (3,3)).
        Hint: If the apply_canny_filter() is called after add_gussian_blur, then the noises are removed
        :param kernel_size: int; TODO
        :return: None
        """
        self.image = cv2.GaussianBlur(src=self.image, ksize=kernel_size, sigmaX=cv2.BORDER_DEFAULT)

    def add_average_blur(self, kernel_size=(3, 3)):
        """Calculates the average of the intensity values in the kernel

        :param kernel_size: tuple of int
        :return: None
        """
        self.image = cv2.blur(src=self.image, ksize=kernel_size)

    def add_median_blur(self, kernel_size=3):
        """

        :param kernel_size: tuple of int
        :return: None
        """
        self.image = cv2.medianBlur(src=self.image, ksize=kernel_size)

    def add_bilateral_blur(self, kernel_size=5):
        """

        :param kernel_size: tuple of int
        :return: None
        """
        self.image = cv2.bilateralFilter(src=self.image, d=kernel_size, sigmaSpace=15, sigmaColor=15)

    #########
    # EDGES #
    #########
    def apply_canny_filter(self):
        """Places a Filter according to the Canny Edge Algorithm over the image and overwrites the variable image.

        Hint: If a blurred image is passed, then fewer edges are detected
        :return: None
        """
        self.image = cv2.Canny(image=self.image, threshold1=125, threshold2=175)  # TODO threshhold bestimmen

    def dilating_image(self, kernel_size=(3, 3), number_of_iterations=1):
        """Expands Pixel

        :param kernel_size: int; TODO
        :param number_of_iterations: int; TODO
        :return: None
        """
        self.image = cv2.dilate(src=self.image, kernel=kernel_size, iterations=number_of_iterations)

    def eroding_image(self, kernel_size=(3, 3), number_of_iterations=1):
        """Reduces Pixel

        :param kernel_size: int; TODO
        :param number_of_iterations: int; TODO
        :return: None
        """
        self.image = cv2.erode(self.image, kernel=kernel_size, iterations=number_of_iterations)

    def identify_contours_and_hierarchies(self, mode='all hierarchic contours', method='CHAIN_APPROX_NONE'):
        """

        :param method:
        :param mode:
        :return: contours is list of all the contours which are found in the image
             hierarchies contains information about the image topology
        """
        if mode == 'all hierarchic contours':
            mode = cv2.RETR_TREE
        elif mode == 'all external contours':
            mode = cv2.RETR_EXTERNAL
        else:  # all contours
            mode = cv2.RETR_LIST

        if method == 'CHAIN_APPROX_SIMPLE':
            method = cv2.CHAIN_APPROX_SIMPLE
        else:  # method == 'CHAIN_APPROX_NONE'
            method = cv2.CHAIN_APPROX_NONE

        contours, hierarchies = cv2.findContours(image=self.image, mode=mode,
                                                 method=method)  # image should be a canny image
        return contours, hierarchies
