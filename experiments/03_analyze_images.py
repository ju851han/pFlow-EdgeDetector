import imageCleaner
import imageAnalyzer
import os

os.chdir('../training_images/')


def analyze_images(folder=None):
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
            imageAnalyzer.show_image(image)
            if file_name == "Dog.png" and folder == "photos":
                imageAnalyzer.plot_histogram(image, imageAnalyzer.create_round_mask(image=image, center=(500, 700),
                                                                                    radius=350))  # Dog-face


analyze_images("photos")
analyze_images("floor_plan")
