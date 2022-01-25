import numpy as np
import cv2
import imageAnalyzer
import imageCleaner
import os

image_path = "../training_images/simplified_floor_plan/"
file_name = 'O_0_1.png'


def apply_harris(image):
    images = []
    titles = []
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
    dst = cv2.cornerHarris(canny, 2, 3, 0.04)
    # result is dilated for marking the corners, not important
    dst = cv2.dilate(dst, None)
    # Threshold for an optimal value, it may vary depending on the image.
    image_rgb[dst > 0.01 * dst.max()] = [0, 0, 255]
    images.append(image_rgb)
    titles.append("Harris Corner Image")

    imageAnalyzer.show_images(plot_axis=False, number_cols=2, images=images, titles=titles, window_name=image)

    return dst > 0.01 * dst.max()


os.chdir(image_path)
for file_name in os.listdir(os.getcwd()):
    if file_name.lower().endswith('.png'):
        corners = apply_harris(file_name)

