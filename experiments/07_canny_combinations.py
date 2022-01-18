import cv2

import imageAnalyzer
import imageCleaner
import os

image_path = "training_images/floor_plan/"
file_name = "O_-1.png"
images = []
titles = []

os.chdir(image_path)
image_gray = imageCleaner.transform_image_to_grayscale(file_name)
images.append(image_gray)
titles.append("Grayscale Image")

image_blur = imageCleaner.add_gaussian_blur(image=image_gray, kernel_size=(21, 21))
image_canny_orig = imageCleaner.apply_canny_filter(image=image_blur, threshold1=125, threshold2=175)
images.append(image_canny_orig)
titles.append("Canny Original")

image_epf = imageCleaner.add_edge_preserving_filter(image=image_gray)
image_canny_epf = imageCleaner.apply_canny_filter(image=image_epf, threshold1=125, threshold2=175)
images.append(image_canny_epf)
titles.append("Edge Preserving + Canny")

image_closing = cv2.morphologyEx(image_blur, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
image_closed_canny = imageCleaner.apply_canny_filter(image=image_closing, threshold1=125, threshold2=175)
images.append(image_closed_canny)
titles.append("Closing + Gauss + Canny")

image_closed_canny_closing = cv2.morphologyEx(image_closed_canny, cv2.MORPH_CLOSE,
                                              cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
images.append(image_closed_canny_closing)
titles.append("Closing + Gauss + Canny + Closing 5x5")

image_closed_canny_closing_biggest = cv2.morphologyEx(image_closed_canny, cv2.MORPH_CLOSE,
                                                      cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21)))
images.append(image_closed_canny_closing_biggest)
titles.append("Closing + Gauss + Canny + Closing Ellipse 21x21")

image_closed_canny_closing_big_e = cv2.morphologyEx(image_closed_canny, cv2.MORPH_CLOSE,
                                                    cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)))
images.append(image_closed_canny_closing_big_e)
titles.append("Closing + Gauss + Canny + Closing Ellipse 7x7")

image_closed_canny_closing_big = cv2.morphologyEx(image_closed_canny, cv2.MORPH_CLOSE,
                                                  cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7)))
images.append(image_closed_canny_closing_big)
titles.append("Closing + Gauss + Canny + Closing Rectangle 7x7")

imageAnalyzer.show_images(plot_axis=False, number_cols=3, images=images, titles=titles)
