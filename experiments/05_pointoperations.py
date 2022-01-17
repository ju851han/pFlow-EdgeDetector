import os
import imageCleaner

os.chdir('../training_images')


def apply_threshold(image):
    simple_thresh = imageCleaner.apply_simple_threshold(image=image, threshold=180)
    imageCleaner.show_image(image=simple_thresh, title='Changed Color in Area', wait_for_close=True)
    adaptive_thresh = imageCleaner.apply_adaptive_threshold(image=image, neighborhood_size=51)
    imageCleaner.show_image(image=adaptive_thresh, title='Changed Color in Area', wait_for_close=True)


def change_color(image):
    colorful_image = imageCleaner.change_color_in_area(image, 130, 170, 370, 430, 0, 128, 255)
    # imageCleaner.change_color_in_pixel(image, 5, 5)
    imageCleaner.show_image(image=colorful_image, title='Changed Color in Area', wait_for_close=True)


for file_name in os.listdir(os.getcwd()):
    if file_name.lower().endswith('.png'):
        image = file_name

        image = imageCleaner.transform_image_to_grayscale(image)
        imageCleaner.show_image(image=image, title='Gray Image', wait_for_close=True)

        apply_threshold(image)

        change_color(image)

        imageCleaner.invert_image(image)
        imageCleaner.show_image(image=image, title='Inverted Image', wait_for_close=True)
