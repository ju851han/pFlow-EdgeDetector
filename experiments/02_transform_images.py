import os
import imageCleaner


os.chdir('../training_images')
for file_name in os.listdir(os.getcwd()):
    if file_name.lower().endswith('.png'):
        image = imageCleaner.transform_image_to_grayscale(file_name)
        imageCleaner.show_image(image=image, title=file_name, wait_for_close=True)
