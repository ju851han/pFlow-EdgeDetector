from typing import List

import imageAnalyzer
import os
import cv2


all_orig_images = []
all_blurred_images = []

image_path = 'training_images/floor_plan'

os.chdir(image_path)
for file_name in os.listdir(os.getcwd()):
    tmp = []

    if file_name.lower().endswith('.png') or file_name.lower().endswith('.jpg'):
        image = cv2.imread(filename=file_name, flags=0)
        all_orig_images.append(image)
        tmp.append(image)
        for k in [3, 5, 7, 11, 21]:
            blurred_image = cv2.blur(src=image, ksize=(k, k))
            all_blurred_images.append(blurred_image)
            # tmp.append(blurred_image)
            canny_image = cv2.Canny(image=blurred_image, threshold1=125, threshold2=175)
            tmp.append(canny_image)
        imageAnalyzer.show_images(plot_axis=False, number_cols=3, images=tmp)

print("Anzahl geladener Bilder: {}".format(len(all_orig_images)))
# imageAnalyzer.show_images(plot_axis=False, number_cols=2, images=all_orig_images)
