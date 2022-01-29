import imageCleaner
import os


def sizing_images():
    os.chdir('../training_images')
    for file_name in os.listdir(os.getcwd()):
        if file_name.lower().endswith('.png'):
            image = imageCleaner.transform_file_into_grayscale_image(file_name)
            image = imageCleaner.resize_image(image, 1300, 610)
            # image = imageCleaner.snip_image(image, 0, 1300, 0, 610)
            image = imageCleaner.rotate_image(image, rotation_degrees=45)
            imageCleaner.show_image(image, 1, 'Adjusting the Image Size', True)


def rotate_floor_plan():
    floor_plan = imageCleaner.transform_file_into_grayscale_image("../training_images/floor_plan/005_wry.png")
    floor_plan = imageCleaner.rotate_image(floor_plan, 43-90)
    imageCleaner.show_image(floor_plan, 1, 'Rotated Floor Plan', True)


rotate_floor_plan()
