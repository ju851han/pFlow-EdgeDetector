import numpy as np
import cv2
import imageAnalyzer
import imageCleaner
import os
from math import sqrt
import matplotlib.pyplot as plt

image_path = "../training_images/simplified_floor_plan/"
file_name = 'O_0_1.png'
MAX_DISTANCE_CORNER = 20
images = []
titles = []


def apply_harris(image):
    images.clear()
    titles.clear()
    image_rgb = imageCleaner.load_image(image)
    image_gray = imageCleaner.transform_image_to_grayscale(image)
    images.append(image_gray)
    titles.append("Grayscale Image")

    # Edited Canny
    image_blur = imageCleaner.add_gaussian_blur(image=image_gray, kernel_size=(21, 21))
    image_closing = cv2.morphologyEx(image_blur, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    image_canny = imageCleaner.apply_canny_filter(image=image_closing, threshold1=125, threshold2=175)
    image_canny_finished = cv2.morphologyEx(image_canny, cv2.MORPH_CLOSE,
                                            cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9)))
    images.append(image_canny_finished)
    titles.append("Canny Image")

    # Harris
    canny = np.float32(image_canny_finished)
    # dst = cv2.cornerHarris(canny, 2, 3, 0.04)
    dst = cv2.cornerHarris(src=canny, blockSize=2, ksize=5, k=0.07)
    # Threshold for an optimal value, it may vary depending on the image.
    image_rgb[dst > 0.01 * dst.max()] = [0, 0, 255]
    images.append(image_rgb)
    titles.append("Harris Corner Image")

    return dst > 0.01 * dst.max()


def get_coordinates(corner_array):
    all_corners = []
    remaining_corners = []

    # Collect found corners
    for x in range(corner_array.shape[1]):
        for y in range(corner_array.shape[0]):
            if corner_array[y, x]:
                all_corners.append((x, y))
    print("Anzahl Ecken: {}".format(len(all_corners)))

    # Sort out unnecessary corners
    for corner in all_corners:
        already_there = False
        for c in remaining_corners:
            a = corner[0] - c[0]
            b = c[1] - corner[1]
            distance = sqrt(a ** 2 + b ** 2)
            if distance < MAX_DISTANCE_CORNER:
                already_there = True
        if not already_there:
            remaining_corners.append(corner)
        # else:
        #     print("Verworfene Ecke {}".format(corner))

    print("Anzahl Ecken: {}".format(len(remaining_corners)))
    return remaining_corners


os.chdir(image_path)
# for file_name in os.listdir(os.getcwd()):
#     if file_name.lower().endswith('.png'):
corners = apply_harris(file_name)
remaining_corners = get_coordinates(corners)
remaining_corners = np.array(remaining_corners)     # Umwandeln von Liste zu Matrix
x, y = remaining_corners.T

imageAnalyzer.show_images(plot_axis=False, number_cols=2, images=images, titles=titles, window_name=file_name, show_now=False)
plt.subplot(2, 2, 3)    # TODO 3 statt 4
plt.scatter(x, y, marker="*", color="red")
plt.show()


