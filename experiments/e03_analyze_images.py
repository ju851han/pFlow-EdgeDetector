""" Experiment 3: Build methods for analyzing the images.

"""
import imageCleaner
from experiments import imageAnalyzer
import os

os.chdir('../training_images/')


def analyze_images(folder=None):
    """ Shows image and associated plot.

    :param folder: folder_path
    :return: None
    """
    try:
        if folder is not None:
            os.chdir(folder)
    except FileNotFoundError:
        os.chdir("../" + folder)

    for file_name in os.listdir(os.getcwd()):
        if file_name.lower().endswith('.png'):
            image = imageCleaner.load_image(file_name)
            # image = imageCleaner.transform_colored_into_grayscale_image(file_name)
            imageAnalyzer.plot_histogram(image, show_hist=False)
            imageAnalyzer.show_image(image=image, plot_axis=False, window_name=file_name)
            if file_name == "Dog.png" and folder == "photos":
                mask = imageAnalyzer.create_round_mask(image=image, center=(500, 700), radius=350)  # Dog-face
                imageAnalyzer.plot_histogram(image, mask)


analyze_images("photos")
analyze_images("floor_plan")
