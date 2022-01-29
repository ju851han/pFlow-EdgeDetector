""" Experiment 2: Load images and convert them in grayscale.
    The transformation of colored into grayscale-image is a homogeneous point operation.
    Result: The 2. Attempt will be used in the final version because canny and harris detector expect a grayscale-image.
"""
import os
import imageCleaner


os.chdir('../training_images')
for file_name in os.listdir(os.getcwd()):
    if file_name.lower().endswith('.png'):
        # 1. Attempt: 1. Load image, 2. Convert image to grayscale-image:
        # image = imageCleaner.load_image(file_name)
        # gray_image = imageCleaner.transform_colored_into_grayscale_image(image)
        # 2. Attempt: Load & convert image with only one command
        gray_image = imageCleaner.transform_file_into_grayscale_image(file_name)

        imageCleaner.show_image(image=gray_image, title=file_name, wait_for_close=True)
