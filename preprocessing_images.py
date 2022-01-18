from typing import List

import imageAnalyzer
import os
import cv2


all_orig_images = []
all_blurred_images = []

image_path = 'training_images/floor_plan'


def find_kernel_size(file_size=100, factor=100000):
    tmp_k = int(file_size / factor)
    print(tmp_k)
    if tmp_k == 0:
        find_kernel_size(file_size, int(factor / 10))
    elif tmp_k % 2 == 0:
        find_kernel_size(file_size + (1 * factor), factor)
    return tmp_k


os.chdir(image_path)
for file_name in os.listdir(os.getcwd()):
    tmp = []

    if file_name.lower().endswith('.png') or file_name.lower().endswith('.jpg'):
        image = cv2.imread(filename=file_name, flags=0)
        all_orig_images.append(image)
        tmp.append(image)
        image_size = os.path.getsize(os.getcwd() + "/" + file_name)  # Output in Bytes
        print("| {} | {} |".format(file_name, image_size))
        k = find_kernel_size(image_size, 10000)     # TODO delete row later
        print("| {} | {} | {} |".format(file_name, image_size, k))
        blurred_image = cv2.blur(src=image, ksize=(k, k))
        all_blurred_images.append(blurred_image)
        tmp.append(blurred_image)
        canny_image = cv2.Canny(image=blurred_image, threshold1=125, threshold2=175)
        tmp.append(canny_image)
        imageAnalyzer.show_images(plot_axis=False, number_cols=3, images=tmp)

print("Anzahl geladener Bilder: {}".format(len(all_orig_images)))
# imageAnalyzer.show_images(plot_axis=False, number_cols=2, images=all_orig_images)
