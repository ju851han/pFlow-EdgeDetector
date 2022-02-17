""" Experiment 6: Find out which filter is best for preprocessing.
    The goal is to find a filter that preserves the edges from the walls, but smooths the texts so that the most accurate detection of the edges occurs.
    Result: Gaussian Blur with kernel size = 21 and Edge Preserving Filter could be suitable for the preprocessing.
"""
import os
import matplotlib.pyplot as plt
import imageAnalyzer
import imageCleaner


titles = []


def create_titles():
    """ Saves titles in the title list which are used in  show_images()-method for showing the titles above the images in the plot.

    :return: None
    """
    titles.append("Grayscale Image")
    titles.append("Gaussian Blur")
    titles.append("Average Blur")
    titles.append("Bilateral Blur")
    titles.append("Median Blur")
    titles.append("Edge Preserving Filter")
    # titles.append("Laplace Filter")
    # titles.append("Sobel Filter")
    # titles.append("Canny Filter")


def analyze_every_filter_behavior(image_path, k_size=5, show_plt_now=True):
    """ Applies the filters to the image and shows the result.

    :param image_path: str; path or file name of the image
    :param k_size: int; size of the kernel (filter matrix)
    :param show_plt_now: bool;  If it is True, then the image is shown.
    :return: None
    """
    images = []
    image = imageCleaner.transform_file_into_grayscale_image(image_path)
    images.append(image)
    images.append(imageCleaner.add_gaussian_blur(image=image, kernel_size=(k_size, k_size)))
    images.append(imageCleaner.add_average_blur(image=image, kernel_size=(k_size, k_size)))
    images.append(imageCleaner.add_bilateral_blur(image))
    images.append(imageCleaner.add_median_blur(image=image, kernel_size=k_size))
    images.append(imageCleaner.add_edge_preserving_filter(image=image))
    # images.append(imageCleaner.apply_laplacian(image))
    # images.append(imageCleaner.apply_sobel(image))
    # images.append(imageCleaner.apply_canny_filter(image))
    imageAnalyzer.show_images(plot_axis=False, number_cols=3, images=images,
                              window_name="{} with kernel size {}".format(file_name, k_size), titles=titles,
                              show_now=show_plt_now)


def apply_all_filter_to_one_image():
    """ Applies all filters to one image at once.

    :return: None
    """
    for file in os.listdir(os.getcwd()):
        if file.lower().endswith('.png'):
            images = []
            image = imageCleaner.transform_file_into_grayscale_image(file)
            images.append(image)
            images.append(imageCleaner.add_gaussian_blur(image, (5, 5)))
            images.append(imageCleaner.add_average_blur(images[0], kernel_size=(5, 5)))
            images.append(imageCleaner.add_bilateral_blur(images[1]))
            images.append(imageCleaner.add_median_blur(images[2]))
            images.append(imageCleaner.add_edge_preserving_filter(images[3]))
            # images.append(imageCleaner.apply_laplacian(images[4]))
            # images.append(imageCleaner.apply_sobel(images[5]))
            # images.append(imageCleaner.apply_canny_filter(images[6]))
            imageAnalyzer.show_images(plot_axis=False, number_cols=3, images=images, window_name="Images",
                                      titles=titles)


os.chdir('../training_images/floor_plan')
create_titles()
# apply_all_filter_to_one_image()

for file_name in os.listdir(os.getcwd()):
    if file_name.lower().endswith('.png'):
        # image_size = os.path.getsize(os.getcwd() + "/" + file_name)  # Output in Bytes
        # print(image_size)
        for i in [3, 5, 7, 9, 11, 21]:
            analyze_every_filter_behavior(image_path=file_name, k_size=i, show_plt_now=False)
        plt.show()
