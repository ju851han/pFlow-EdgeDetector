""" Experiment 7: Tests which settings are suitable for pre- and post-processing at canny-detector.

    Result:
    For Pre-processing are following settings recommended:
    * Gaussian Blur with kernel size=21 (for smoothing the text)
    * Closing with kernel size = 5 and kernel form = Ellipse (for filling the wall and smoothing the text better)
    For Post-Processing is the following setting recommended:
    * Closing with kernel size = 7 and kernel form = Rectangle (for filling the white corners in the wall)
"""
import cv2
import imageAnalyzer
import imageCleaner
# import os

# image_path = "../training_images/floor_plan/"
file_name = "../training_images/floor_plan/htwg_building_O/O_-1.png"

# os.chdir(image_path)
# for file_name in os.listdir(os.getcwd()):
#    if file_name.lower().endswith('.png'):
images = []
titles = []

image_gray = imageCleaner.transform_file_into_grayscale_image(file_name)
images.append(image_gray)
titles.append("Grayscale Image")

image_blur = imageCleaner.add_gaussian_blur(image=image_gray, kernel_size=(21, 21))
image_canny_orig = imageCleaner.apply_canny_filter(image=image_blur, threshold1=125, threshold2=175)
images.append(image_canny_orig)
titles.append("Gaussian Blur + Canny")

image_epf = imageCleaner.add_edge_preserving_filter(image=image_gray)
image_canny_epf = imageCleaner.apply_canny_filter(image=image_epf, threshold1=125, threshold2=175)
images.append(image_canny_epf)
titles.append("Edge Preserving Filter + Canny")

image_closing = cv2.morphologyEx(image_blur, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
image_closed_canny = imageCleaner.apply_canny_filter(image=image_closing, threshold1=125, threshold2=175)
images.append(image_closed_canny)
titles.append("Closing 5x5 + Gaussian Blur 5x5 + Canny")

image_closed_canny_closing = cv2.morphologyEx(image_closed_canny, cv2.MORPH_CLOSE,
                                              cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
images.append(image_closed_canny_closing)
titles.append("Closing 5x5 + Gaussian Blur 5x5 + Canny + Closing 5x5")

image_closed_canny_closing_biggest = cv2.morphologyEx(image_closed_canny, cv2.MORPH_CLOSE,
                                                      cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21)))
images.append(image_closed_canny_closing_biggest)
titles.append("Closing 5x5 + Gaussian Blur 5x5 + Canny + Closing Ellipse 21x21")

image_closed_canny_closing_big_e = cv2.morphologyEx(image_closed_canny, cv2.MORPH_CLOSE,
                                                    cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)))
images.append(image_closed_canny_closing_big_e)
titles.append("Closing 5x5 + Gaussian Blur 5x5 + Canny + Closing Ellipse 7x7")

image_closed_canny_closing_big = cv2.morphologyEx(image_closed_canny, cv2.MORPH_CLOSE,
                                                  cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7)))
images.append(image_closed_canny_closing_big)
titles.append("Closing 5x5 + Gaussian Blur 5x5 + Canny + Closing Rectangle 7x7")

imageAnalyzer.show_images(plot_axis=False, number_cols=2, images=images, titles=titles, window_name=file_name)
