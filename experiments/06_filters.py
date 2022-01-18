import os

import imageAnalyzer
import imageCleaner

os.chdir('../training_images/floor_plan')


def analyze_every_filter_behavior():
    for file_name in os.listdir(os.getcwd()):
        if file_name.lower().endswith('.png'):
            images = []
            image = imageCleaner.transform_image_to_grayscale(file_name)
            images.append(imageCleaner.add_gaussian_blur(image, (5, 5)))
            # imageCleaner.apply_simple_threshold(130)
            # imageCleaner.apply_adaptive_threshold(neighborhood_size=81)
            images.append(imageCleaner.add_average_blur(image, kernel_size=(5, 5)))
            images.append(imageCleaner.add_bilateral_blur(image))
            images.append(imageCleaner.add_median_blur(image))
            images.append(imageCleaner.add_edge_preserving_filter(image))
            # images.append(imageCleaner.apply_laplacian(image))
            # images.append(imageCleaner.apply_sobel(image))
            # images.append(imageCleaner.apply_canny_filter(image))
            imageAnalyzer.show_images(plot_axis=False, number_cols=3, images=images, name="Bilder")


def apply_all_filter_to_one_image():
    for file_name in os.listdir(os.getcwd()):
        if file_name.lower().endswith('.png'):
            images = []
            image = imageCleaner.transform_image_to_grayscale(file_name)
            images.append(imageCleaner.add_gaussian_blur(image, (5, 5)))
            images.append(imageCleaner.add_average_blur(images[0], kernel_size=(5, 5)))
            images.append(imageCleaner.add_bilateral_blur(images[1]))
            images.append(imageCleaner.add_median_blur(images[2]))
            images.append(imageCleaner.add_edge_preserving_filter(images[3]))
            # images.append(imageCleaner.apply_laplacian(images[4]))
            # images.append(imageCleaner.apply_sobel(images[5]))
            # images.append(imageCleaner.apply_canny_filter(images[6]))
            imageAnalyzer.show_images(plot_axis=False, number_cols=3, images=images, name="Bilder")


# analyze_every_filter_behavior()
apply_all_filter_to_one_image()
