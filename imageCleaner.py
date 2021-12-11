import cv2
from matplotlib import pyplot as plt


class ImageCleaner:
    """Class for Loading and Processing Images (Pictures)

    """

    def __init__(self, image_path):
        """Constructor

        flags=0 in cv2.imread()-method means that the passed image is transformed as a gray value image.
        If no flags have been set, the image is colored.
        :param image_path: str
        """
        if type(image_path) == int:
            raise TypeError("Image path must be a str! Current image_path is:" + str(image_path))
        self.image = cv2.imread(filename=image_path)  # , flags=0)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        if self.image is None:
            raise AttributeError("Image-file can't be found. The affected image-path is:" + image_path)

    ##########
    # CHECKS #
    ##########

    @staticmethod
    def __check_rgb_values(red, green, blue):
        """Checks if the value of red, green and blue is valid (int, [0,255]).

        Hint: If red, green and blue is 0 then it will throw an error
        because these values are used to mark something. If all these are 0 then marking is not possible

        :param red: int
        :param green: int
        :param blue: int
        :return: None
        """
        if not isinstance(red, int):
            raise TypeError("Data type of red must be int.\n"
                            "Current red value: " + str(red) + "\n"
                                                               "Current data type of red: " + str(type(red)))
        elif not isinstance(green, int):
            raise TypeError("Data type of green must be int.\n"
                            "Current green value: " + str(green) + "\n"
                                                                   "Current data type of green: " + str(type(green)))
        elif not isinstance(blue, int):
            raise TypeError("Data type of blue must be int.\n"
                            "Current blue value: " + str(blue) + "\n"
                                                                 "Current data type of blue: " + str(type(blue)))
        elif red < 0 or red > 255:
            raise ValueError("Value of Red is incorrect. Current red value: " + str(red))
        elif green < 0 or green > 255:
            raise ValueError("Value of Green is incorrect. Current green value: " + str(green))
        elif blue < 0 or blue > 255:
            raise ValueError("Value of Blue is incorrect. Current blue value: " + str(blue))
        elif red == 0 and green == 0 and blue == 0:
            raise AttributeError("The value of red, green and blue is 0.\n"
                                 "At least one value of red, green or blue must be greater than zero.")

        # TODO CHECK for ksize, x, y

    ##########
    # OTHERS #
    ##########

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

    def change_color_in_area(self, y_min, y_max, x_min, x_max, blue=0, green=0, red=255):
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
        self.__check_rgb_values(red, green, blue)
        self.image[y_min:y_max, x_min:x_max] = blue, green, red

    def change_color_in_pixel(self, y, x, blue=0, green=0, red=255):
        """Non-homogeneous point operation: Changes color only in one pixel.

        :param y: int; variable for y-axis; 0 is at top, max is at bottom.
        :param x: int; variables for x-axis; 0 is in the left corner, max is on the right side.
        :param blue: int
        :param green: int
        :param red: int
        :return: None
        """
        self.__check_rgb_values(red, green, blue)
        self.image[y, x] = blue, green, red

    def apply_simple_threshold(self, threshold=150):
        """Homogeneous point operations: Binaries the image with the simple threshold method.

        Precondition: The image must be a gray scale image. If the image shape has more than 2 channels (image.shape)
        then it is a color image.
        This Method compares each pixel value (=intensity value) of the image with the threshold.
        If the pixel value is below than threshold then the new pixel value is 0.
        If the pixel value is equals or higher than threshold then the new pixel value is 255.
        :return: None
        """
        if len(self.image.shape) != 2:
            self.transform_colored_into_gray_img()

        _, thresh = cv2.threshold(src=self.image, thresh=threshold, maxval=255, type=cv2.THRESH_BINARY)
        self.image = thresh

    def apply_adaptive_threshold(self, neighborhood_size=11, offset=0, invert=False, adaptive_method_name='Gussian'):
        """Homogeneous point operations: Finds the optimum threshold by itself and uses this threshold to binarize the image.

        :param adaptive_method_name: str; valid strings are 'gussian' and 'mean'
                                     (Lower- and Upper-case will be ignored)
        :param neighborhood_size: int; neighborhood size of the kernel size
                                 (it is needed for calculating the adaptiveMethod for the optimal threshold value)
        :param offset: int; it is subtracted from the found threshold to fine tune the final threshold.
        :param invert: bool; Should black and white color be swapped? Yes -> True; No -> False
        :return: None
        """
        if invert:
            thresh_type = cv2.THRESH_BINARY_INV
        else:
            thresh_type = cv2.THRESH_BINARY_INV

        if adaptive_method_name.lower() == 'gussian':
            adaptive_method = cv2.ADAPTIVE_THRESH_GAUSSIAN_C
        elif adaptive_method_name.lower() == 'mean':
            adaptive_method = cv2.ADAPTIVE_THRESH_MEAN_C
        else:
            raise AttributeError('The passed value for adaptiveMethod is not valid.\n'
                                 'Valid values are \'Gussian or Mean\'. Current value is:' + str(adaptive_method_name))

        self.image = cv2.adaptiveThreshold(src=self.image, maxValue=255, adaptiveMethod=adaptive_method,
                                           thresholdType=thresh_type, blockSize=neighborhood_size, C=offset)

    ###########
    # FILTERS #
    ###########
    """
    A filter smooths the image by adding a blur to it.
    One reason for using a filter is if the image contains a lot of noise because
    applying the filter reduces the noises in the image.
    
    The parameter ksize is an abbreviation for kernel size which is often used in the blurring methods.
    The ksize specifies how many pixel-rows and pixel-columns the kernel is large.
    A kernel is a small matrix which is drawn over the image step by step. 
    
    The different blurring methods are described in the respective method.
    """

    def add_gaussian_blur(self, kernel_size=(3, 3)):
        """

        If the noise is also high, then a high ksize is recommended (e.g.: (7,7)).
        If the noise is also low, then a smaller ksize is recommended (e.g.: (3,3)).
        Hint: If the apply_canny_filter() is called after add_gussian_blur, then the noises are removed
        :param kernel_size: tuple of int: (number_of_rows, number_of cols)
        :return: None
        """
        self.image = cv2.GaussianBlur(src=self.image, ksize=kernel_size, sigmaX=cv2.BORDER_DEFAULT)

    def add_average_blur(self, kernel_size=(3, 3)):
        """Calculates the average of the intensity values in the kernel

        :param kernel_size: tuple of int: (number_of_rows, number_of cols)
        :return: None
        """
        self.image = cv2.blur(src=self.image, ksize=kernel_size)

    def add_median_blur(self, kernel_size=3):
        """Calculates the median of the intensity values in the kernel

        :param kernel_size: tuple of int: (number_of_rows, number_of cols)
        :return: None
        """
        self.image = cv2.medianBlur(src=self.image, ksize=kernel_size)

    def add_bilateral_blur(self, kernel_size=5):
        """

        :param kernel_size: tuple of int: (number_of_rows, number_of cols)
        :return: None
        """
        self.image = cv2.bilateralFilter(src=self.image, d=kernel_size, sigmaSpace=15, sigmaColor=15)

    #########
    # EDGES #
    #########
    """
    
    """

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
