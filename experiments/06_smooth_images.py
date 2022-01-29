import os
import matplotlib.pyplot as plt
import imageAnalyzer
import imageCleaner

os.chdir('../training_images/floor_plan')

titles = []


def create_titles():
    titles.append("Grayscale Image")
    titles.append("Gaussian Blur")
    titles.append("Average Blur")
    titles.append("Bilateral Blur")
    titles.append("Median Blur")
    titles.append("Edge Preserving Filter")


def analyze_every_filter_behavior(image, ksize=5, show_plt_now=True):
            images = []
            image = imageCleaner.transform_file_into_grayscale_image(image)
            images.append(image)
            images.append(imageCleaner.add_gaussian_blur(image=image, kernel_size=(ksize, ksize)))
            # imageCleaner.apply_simple_threshold(130)
            # imageCleaner.apply_adaptive_threshold(neighborhood_size=81)
            images.append(imageCleaner.add_average_blur(image=image, kernel_size=(ksize, ksize)))
            images.append(imageCleaner.add_bilateral_blur(image))
            images.append(imageCleaner.add_median_blur(image=image, kernel_size=ksize))
            images.append(imageCleaner.add_edge_preserving_filter(image=image))
            # images.append(imageCleaner.apply_laplacian(image))
            # images.append(imageCleaner.apply_sobel(image))
            # images.append(imageCleaner.apply_canny_filter(image))
            imageAnalyzer.show_images(plot_axis=False, number_cols=3, images=images, window_name="{} with kernel size {}".format(file_name, ksize), titles=titles, show_now=show_plt_now)


def apply_all_filter_to_one_image():
    for file_name in os.listdir(os.getcwd()):
        if file_name.lower().endswith('.png'):
            images = []
            image = imageCleaner.transform_file_into_grayscale_image(file_name)
            images.append(image)
            images.append(imageCleaner.add_gaussian_blur(image, (5, 5)))
            images.append(imageCleaner.add_average_blur(images[0], kernel_size=(5, 5)))
            images.append(imageCleaner.add_bilateral_blur(images[1]))
            images.append(imageCleaner.add_median_blur(images[2]))
            images.append(imageCleaner.add_edge_preserving_filter(images[3]))
            # images.append(imageCleaner.apply_laplacian(images[4]))
            # images.append(imageCleaner.apply_sobel(images[5]))
            # images.append(imageCleaner.apply_canny_filter(images[6]))
            imageAnalyzer.show_images(plot_axis=False, number_cols=3, images=images, window_name="Bilder", titles=titles)


create_titles()
# apply_all_filter_to_one_image()

for file_name in os.listdir(os.getcwd()):
    if file_name.lower().endswith('.png'):
        # image_size = os.path.getsize(os.getcwd() + "/" + file_name)  # Output in Bytes
        # print(image_size)
        for i in [3, 5, 7, 9, 11, 21]:
            analyze_every_filter_behavior(image=file_name, ksize=i, show_plt_now=False)
        plt.show()

