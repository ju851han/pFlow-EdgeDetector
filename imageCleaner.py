""" Methods for Loading and Processing Images (Pictures)

"""
import os.path
import cv2
import numpy as np

WINDOW_WIDTH = 1300
WINDOW_HEIGHT = 610
MIN_GRAY_VALUE = 0
MAX_GRAY_VALUE = 255


##########
# CHECKS #
##########

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
                        "Current red value:{}\n"
                        "Current data type of red: {}".format(red, type(red)))
    elif not isinstance(green, int):
        raise TypeError("Data type of green must be int.\n"
                        "Current green value: {}\n"
                        "Current data type of green: {}" .format(green, type(green)))
    elif not isinstance(blue, int):
        raise TypeError("Data type of blue must be int.\n"
                        "Current blue value: {}\n"
                        "Current data type of blue: {}".format(blue, type(blue)))
    elif red < MIN_GRAY_VALUE or red > MAX_GRAY_VALUE:
        raise ValueError("Value of Red is incorrect. Current red value: {}".format(red))
    elif green < MIN_GRAY_VALUE or green > MAX_GRAY_VALUE:
        raise ValueError("Value of Green is incorrect. Current green value:{}".format(green))
    elif blue < MIN_GRAY_VALUE or blue > MAX_GRAY_VALUE:
        raise ValueError("Value of Blue is incorrect. Current blue value:{}".format(blue))
    elif red == MIN_GRAY_VALUE and green == MIN_GRAY_VALUE and blue == MIN_GRAY_VALUE:
        raise AttributeError("The value of red, green and blue is 0.\n"
                             "At least one value of red, green or blue must be greater than zero.")


def __check_threshold(value):
    """ Checks if threshold value is in [0;255].

    :param value: int; threshold value
    :return: None
    """
    if not isinstance(value, int):
        raise TypeError("Data type of the threshold value must be int.\n"
                        "Current threshold value is: {} \n"
                        "Current data type of the threshold value is: {}".format(value, type(value)))
    elif value < MIN_GRAY_VALUE or value > MAX_GRAY_VALUE:
        raise ValueError("The threshold value is incorrect. It must be between 0 and 255. Current threshold value is: {}".format(value))


def __check_height(image, height):  #TODO WINDOW_HEIGHT
    """ Checks if the height is smaller or equals to image-height.

    Used for checking y-axis and kernel size.
    :param image: image
    :param height: int
    :return: None
    """
    if height > image.shape[0]:
        raise ValueError("The height value is incorrect. It must be smaller than the image height. Current height value is: {}".format(height))
    elif not isinstance(height, int):
        raise TypeError("Data type of the height must be int.\n"
                        "Current height is: {} \n"
                        "Current data type of height: {}".format(height, type(height)))


def __check_width(image, width):    #TODO WINDOW_WIDTH
    """ Checks if the width is smaller or equals to image-width.

    Used for checking x-axis and kernel size.
    :param image: image
    :param width: int
    :return: None
    """
    if width > image.shape[1]:
        raise ValueError(
            "The width value is incorrect. It must be smaller than the image width. Current width value is: {}".format(width))
    elif not isinstance(width, int):
        raise TypeError("Data type of the height must be int.\n"
                        "Current height is: {} \n"
                        "Current data type of height: {}".format(width, type(width)))


##########
# OTHERS #
##########

def load_image(image_path):
    """Loads an image.

    :param image_path: str
    :return: rgb-image

    """
    if not image_path.lower().endswith('.png'):
        raise FileExistsError("Data type of the image must be a .png. Current image_path ist:{}".format(image_path))
    if type(image_path) == int:
        raise TypeError("Image path must be a str! Current image_path is:{}".format(image_path))
    if not os.path.exists(image_path):
        raise FileNotFoundError("File was not found. The searched image_path is: {}".format(image_path))
    image = cv2.imread(filename=image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    if image is None:
        raise AttributeError("Image-file can't be found. The affected image-path is:{}".format(image_path))
    return image


def show_image(image, scale=1, title='Image', wait_for_close=False):
    """Displays a Picture.

    :param image: image
    :param wait_for_close: bool; if this is True, then the window will be closed as soon a button is pressed
    :param title: str; text for window frame
    :param scale: int between [0,1]
    :return: None
    """
    if scale < 0 or scale > 1:
        raise ValueError("Scale must be between 0 and 1.\nCurrent value of the scale: {}".format(scale))
    else:
        width = int(image.shape[1] * scale)
        __check_width(image, width)
        height = int(image.shape[0] * scale)
        __check_height(image, height)
        dimensions = (width, height)
        frame_resized = cv2.resize(image, dimensions, interpolation=cv2.INTER_AREA)
        cv2.imshow(title, frame_resized)
        if wait_for_close:
            cv2.waitKey(0)


################
# IMAGE SIZING #
################

def resize_image(image, x=WINDOW_WIDTH, y=WINDOW_HEIGHT):
    """ Changes the size of the image.

        Default parameter values are the window width (x) and height (y) of pFlowGRID.
        :param image: image
        :param x: int; size of the x-axis
        :param y: int; size of the y-axis
        :return: image
        """
    orig_width = int(image.shape[1])
    __check_width(image, orig_width)
    orig_height = int(image.shape[0])
    __check_height(image, orig_height)
    if x < orig_width or y < orig_height:
        return cv2.resize(src=image, dsize=(x, y), interpolation=cv2.INTER_AREA)
    else:
        return cv2.resize(src=image, dsize=(x, y), interpolation=cv2.INTER_LINEAR)


def snip_image(image, x_min=0, x_max=WINDOW_WIDTH, y_min=0, y_max=WINDOW_HEIGHT):
    """ Cuts out an image. The result is a cropped image.

    Default parameters values are the window width (x) and height (y) of pFlowGRID.
    :param image: image
    :param x_min: int; start on the x-axis
    :param x_max: int; end on the x-axis
    :param y_min: int; start on the y-axis
    :param y_max: int; end on the y-axis
    :return: image
    """
    return image[x_min:x_max, y_min:y_max]


def rotate_image(image, rotation_degrees=45):
    """Turns an image by the given degrees of rotation around the center of the image.

    :param image: image
    :param rotation_degrees: int; = angle that indicates by how much the image is rotated
    :return: image
    """
    (height, weight) = image.shape[:2]
    (x, y) = (weight // 2, height // 2)
    __check_width(image, x)
    __check_height(image, y)
    matrix = cv2.getRotationMatrix2D((x, y), rotation_degrees, 1.0)
    return cv2.warpAffine(image, matrix, (weight, height))


####################
# POINT OPERATIONS #
####################
"""
Homogeneous point operations are independent of pixel coordinate.
Non-homogeneous point operations depend on pixel coordinate.
"""


def transform_file_into_grayscale_image(image_path):
    """Homogeneous point operation: Transforms an image to grayscale-image.

    flags=0 in cv2.imread()-method means that the passed image is transformed as a gray value image.
    If no flags have been set, the image is colored.
    :param image_path: str
    :return: image

    """
    if not image_path.lower().endswith('.png'):
        raise FileExistsError("Data type of the image must be a .png. Current image_path ist:{}".format(image_path))
    if type(image_path) == int:
        raise TypeError("Image path must be a str! Current image_path is:{}".format(image_path))
    if not os.path.exists(image_path):
        raise FileNotFoundError("File was not found. The searched image_path is: {}".format(image_path))
    image = cv2.imread(filename=image_path)  # , flags=0)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if image is None:
        raise AttributeError("Image-file can't be found. The affected image-path is:" + image_path)
    return image


def transform_colored_into_grayscale_image(image):
    """Homogeneous point operation: Changes a color image into a grayscale-image and overwrites the variable image.

    :param image: image
    :return: image
    """
    return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)


def apply_simple_threshold(image, threshold=150):
    """Homogeneous point operation: Binaries the image with the simple threshold method.

    Precondition: The image must be a grayscale-image. If the image shape has more than 2 channels (image.shape)
    then it is a color image.
    This Method compares each pixel value (=intensity value) of the image with the threshold.
    If the pixel value is below than threshold then the new pixel value is 0.
    If the pixel value is equals or higher than threshold then the new pixel value is 255.
    :param image: image
    :param threshold: int
    :return: image
    """
    __check_threshold(threshold)
    if len(image.shape) != 2:
        transform_colored_into_grayscale_image(image)

    _, thresh = cv2.threshold(src=image, thresh=threshold, maxval=255, type=cv2.THRESH_BINARY)
    return thresh


def apply_adaptive_threshold(image, neighborhood_size=11, offset=0, invert=False, adaptive_method_name='Mean'):
    """Homogeneous point operation: Finds the optimum threshold by itself and uses this threshold to binarize the image.

    Precondition: The image must be a gray scale image. If the image shape has more than 2 channels (image.shape)
    then it is a color image.
    :param image: image
    :param adaptive_method_name: str; valid strings are 'gaussian' and 'mean'
                                 (Lower- and Upper-case will be ignored)
    :param neighborhood_size: int; neighborhood size of the kernel size
                             (it is needed for calculating the adaptiveMethod for the optimal threshold value)
    :param offset: int; it is subtracted from the found threshold to fine tune the final threshold.
    :param invert: bool; Should black and white color be swapped? Yes -> True; No -> False
    :return: image
    """
    if len(image.shape) != 2:
        image = transform_colored_into_grayscale_image(image)

    if invert:
        thresh_type = cv2.THRESH_BINARY_INV
    else:
        thresh_type = cv2.THRESH_BINARY

    if adaptive_method_name.lower() == 'gaussian':
        adaptive_method = cv2.ADAPTIVE_THRESH_GAUSSIAN_C
    elif adaptive_method_name.lower() == 'mean':
        adaptive_method = cv2.ADAPTIVE_THRESH_MEAN_C
    else:
        raise AttributeError("The passed value for adaptiveMethod is not valid.\n Valid values are \'Gaussian or Mean\'. Current value is: {}".format(adaptive_method_name))

    return cv2.adaptiveThreshold(src=image, maxValue=MAX_GRAY_VALUE, adaptiveMethod=adaptive_method,
                                 thresholdType=thresh_type, blockSize=neighborhood_size, C=offset)


def invert_image(image):
    """Homogeneous point operation: Turns the image upside down.

    :param image: image
    :return:image
    """
    return cv2.rotate(image, cv2.ROTATE_180)


def change_color_in_area(image, y_min, y_max, x_min, x_max, blue=0, green=0, red=255):
    """Non-homogeneous point operation: Changes color in an image area

    y_min, y_max: variables for y-axis; 0 is at top, max is at bottom
    x_min, x_max: variables for x-axis; 0 is in the left corner, max is on the right side
    :param image: image
    :param y_min: int
    :param y_max: int
    :param x_min: int
    :param x_max: int
    :param blue: int
    :param green: int
    :param red: int
    :return: image
    """
    __check_rgb_values(red, green, blue)
    __check_width(image, x_min)
    __check_width(image, x_max)
    __check_height(image, y_min)
    __check_height(image, y_max)

    if 2 == len(image.shape):  # check if image is gray then only variable red is considered
        image[y_min:y_max, x_min:x_max] = red
    else:
        image[y_min:y_max, x_min:x_max] = red, green, blue
    return image


def change_color_in_pixel(image, y, x, blue=0, green=0, red=255):
    """Non-homogeneous point operation: Changes color only in one pixel.

    :param image: image
    :param y: int; variable for y-axis; 0 is at top, max is at bottom.
    :param x: int; variables for x-axis; 0 is in the left corner, max is on the right side.
    :param blue: int
    :param green: int
    :param red: int
    :return: image
    """
    __check_rgb_values(red, green, blue)
    __check_width(image, x)
    __check_height(image, y)
    image[y, x] = red, green, blue
    return image


###########
# FILTERS #
###########
# TODO edit description
"""
A filter smooths the image by adding a blur to it.  
One reason for using a filter is if the image contains a lot of noise because
applying the filter reduces the noises in the image.

The parameter ksize is an abbreviation for kernel size which is often used in the blurring methods.
The kernel size specifies how many pixel-rows and pixel-columns the kernel is large.
A kernel is a small matrix which is drawn over the image step by step. 
The hot spot is the middle pixel of the kernel.

The different blurring methods are described in the respective method.
"""


def add_gaussian_blur(image, kernel_size=(3, 3), sigma_x=2):
    """ Smoothing filter: Calculates the weight from the pixels in the kernel
        - how often the intensity values occur in the surrounding pixels and the hot spot at the kernel.
        The product of the weight is the new pixel value of the hot spot.

    The Gaussian Blur is the most popular blurring method.
    If the noise is also high, then a high kernel size is recommended (e.g.: (7,7)).
    If the noise is also low, then a smaller kernel size is recommended (e.g.: (3,3)).
    Hint: If the apply_canny_filter() is called after add_gaussian_blur(), then the noises are removed
    :param image: image
    :param kernel_size: tuple of int: (number_of_rows, number_of cols)
    :param sigma_x: int; width of the gaussian bell
            If the value is large, then the image is strongly smoothed.
            If the value is small, then the image is less smoothed.
    :return: image
    """
    __check_height(image, kernel_size[0])
    __check_width(image, kernel_size[1])
    return cv2.GaussianBlur(src=image, ksize=kernel_size, sigmaX=sigma_x)


def add_average_blur(image, kernel_size=(3, 3)):
    """Smoothing filter: Calculates the average of the intensity values from the pixels in the kernel.
    The result is the new pixel value of the hot spot.

    Synonym: box filter
    :param image: image
    :param kernel_size: tuple of int: (number_of_rows, number_of cols)
    :return: image
    """
    __check_height(image, kernel_size[0])
    __check_width(image, kernel_size[1])
    return cv2.blur(src=image, ksize=kernel_size)


def add_median_blur(image, kernel_size=3):
    """Ranking filter: Calculates the median of the intensity values from the pixels in the kernel.
    The result is the new pixel value of the hot spot.

    Hint: This method tends to be more effective in reducing noise in an image than average and gussian blur
    :param image: image
    :param kernel_size: tuple of int: (number_of_rows, number_of cols)
    :return: image
    """
    __check_height(image, kernel_size[0])
    __check_width(image, kernel_size[1])
    return cv2.medianBlur(src=image, ksize=kernel_size)


def add_bilateral_blur(image, kernel_size=5, sigma_color=15, sigma_space=15):
    """ Unlike the other methods this method also blurs the image, but it does not make the edges less sharp.

    Further Information: https://docs.opencv.org/4.x/d4/d86/group__imgproc__filter.html#ga9d7064d478c95d60003cf839430737ed
    https://machinelearningknowledge.ai/bilateral-filtering-in-python-opencv-with-cv2-bilateralfilter/
    :param image: image
    :param kernel_size: tuple of int: (number_of_rows, number_of cols)
    :param sigma_color: int; if it is a high number, then different colors are in the surrounding pixels
                        which are noted when applying bilateral blur.
    :param sigma_space: int; Larger values for this sigma space mean that pixels further away from the hot spot
                        affect the blur calculation.
    :return: image
    """
    __check_height(image, kernel_size)
    __check_width(image, kernel_size)
    return cv2.bilateralFilter(src=image, d=kernel_size, sigmaSpace=sigma_space, sigmaColor=sigma_color)


def add_edge_preserving_filter(image):  # TODO ggf. ansehen
    """Real-Time Edge-Preserving Denoising Filter: It is used for Non-Photorealistic Rendering.

    Further Information: https://docs.opencv.org/4.x/df/dac/group__photo__render.html#gafaee2977597029bc8e35da6e67bd31f7
    :param image: image
    :return: image
    """
    return cv2.edgePreservingFilter(src=image)


def apply_laplacian(image):
    """Edge Filter

    :param image: image
    :return: image
    """
    if len(image.shape) != 2:
        image = transform_colored_into_grayscale_image(image)

    lap = cv2.Laplacian(image, cv2.CV_64F)
    return np.uint8(np.absolute(lap))


def apply_sobel(image):
    """Edge Filter


    :param image: image
    :return:image
    """
    if len(image.shape) != 2:
        transform_colored_into_grayscale_image(image)

    sobel_x = cv2.Sobel(src=image, ddepth=cv2.CV_64F, dx=1, dy=0)
    sobel_y = cv2.Sobel(src=image, ddepth=cv2.CV_64F, dx=0, dy=1)
    combined_sobel = cv2.bitwise_or(sobel_x, sobel_y)
    return combined_sobel

#TODO add closing + opening

#############
# DETECTORs #
#############
"""

"""


def apply_canny_filter(image, threshold1=125, threshold2=175):
    """Edge Filter: Places a filter according to the Canny Edge Algorithm over the image and returns  an image.

    Further Information:  https://docs.opencv.org/3.4/da/d5c/tutorial_canny_detector.html
    Hint: If a blurred image is passed, then fewer edges are detected.
    :param threshold2: int
    :param threshold1: int
    :param image: image
    :return: image
    """
    __check_threshold(threshold1)
    __check_threshold(threshold2)
    if len(image.shape) != 2:
        image = transform_colored_into_grayscale_image(image)

    return cv2.Canny(image=image, threshold1=threshold1, threshold2=threshold2)  # TODO threshold bestimmen


def identify_contours_and_hierarchies(image, mode='all hierarchic contours', method='CHAIN_APPROX_NONE',
                                      canny_threshold1=125, canny_threshold2=175):
    """

    :param image: image
    :param canny_threshold2: int;
    :param canny_threshold1: int;
    :param method: str;
    :param mode: str;
    :return: contours is list of all the contours which are found in the image
         hierarchies contains information about the image topology
    """
    if mode == 'all hierarchic contours':
        mode = cv2.RETR_TREE
    elif mode == 'all external contours':
        mode = cv2.RETR_EXTERNAL
    else:  # all contours
        mode = cv2.RETR_LIST

    if method == 'CHAIN_APPROX_SIMPLE':  # compresses all the contours that are returned
        method = cv2.CHAIN_APPROX_SIMPLE
    else:  # method == 'CHAIN_APPROX_NONE'
        method = cv2.CHAIN_APPROX_NONE

    contours, hierarchies = cv2.findContours(
        image=apply_canny_filter(image=image, threshold1=canny_threshold1, threshold2=canny_threshold2), mode=mode,
        method=method)  # image should be a canny image
    return contours, hierarchies
