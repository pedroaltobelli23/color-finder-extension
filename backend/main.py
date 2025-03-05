from sklearn.cluster import KMeans
import numpy as np
import cv2
import matplotlib.pyplot as plt
from collections import Counter
from skimage.color import rgb2lab, deltaE_cie76, lab2rgb
import os
from parameters import BASIC_HSV_COLORS, HTML_HSV_COLORS, X11_HSV_COLORS

def hsv_to_rgb(code):
    h = code[0]
    s = code[1]
    v = code[2]
    hsv = np.uint8([[[h, s, v]]])  # OpenCV uses [0, 255] for S and V
    rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)    
    
    return rgb[0][0]

def find_closest(centers: list, hsv_colors: dict):
    lab_lookup = {k: rgb2lab(np.uint8(np.asarray([[hsv_to_rgb(v)]]))) for k, v in hsv_colors.items()}
    response = dict()
    for center in centers:
        lab_center = rgb2lab(np.uint8(np.asarray([[center]])))
        smallest_diff = 100_000_000
        smallest_diff_name = None
        for lookup_name, lookup in lab_lookup.items():
            diff = deltaE_cie76(lab_center, lookup)[0][0]
            if diff < smallest_diff:
                smallest_diff = diff
                smallest_diff_name = lookup_name
        response[smallest_diff_name] = center
    return response

def RGB2HEX(color):
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))

def image_quantization(image, number_of_colors):
    # Do the quantization of an image, using Kmeans. Return the quantizated image and all its colors
    modified_image_raw = cv2.resize(image, (600, 400), interpolation=cv2.INTER_AREA)
    modified_image = modified_image_raw.reshape(modified_image_raw.shape[0]*modified_image_raw.shape[1], 3)
    stop_loop = False
    while not stop_loop:
        clf = KMeans(n_clusters=number_of_colors, n_init='auto')
        labels = clf.fit_predict(modified_image)
        counts = Counter(labels)
        counts = dict(sorted(counts.items()))
        center_colors = clf.cluster_centers_.astype(int)
        
        quant_colors = [center_colors[i] for i in counts.keys()]
        quantized_image = center_colors[labels]
        
        # Reshape the quantized image back to the original dimensions
        quantized_image = quantized_image.reshape(400, 600, 3).astype(np.uint8)
        name_quantColorRGB = find_closest(quant_colors, HTML_HSV_COLORS)
        if len(name_quantColorRGB)<number_of_colors:
            # Repete o processo, diminuindo number_of_colors
            number_of_colors -= 1
            print(f"Repetindo o processo, porem agora com n_cluster = {number_of_colors}")
        else:
            stop_loop = True
            
    name_quantColorHEX = {k: RGB2HEX(v) for k, v in name_quantColorRGB.items()}

    return modified_image_raw, quantized_image, name_quantColorRGB

def main(img_path: os.path.abspath):
    image_raw = cv2.imread(img_path)
    image = cv2.cvtColor(image_raw, cv2.COLOR_BGR2RGB)
    print(f"The type of this input is {type(image)}")
    print(f"Shape: {image.shape}")
    print("Doing image quantizaion: ", end="\n")
    resized_image, quantized_image, name_quantColorRGB = image_quantization(image, 60)
    print(name_quantColorRGB)
    
    # plt.imshow(quantized_image)
    plt.imsave("result.png", quantized_image)
    # plt.imshow(resized_image)
    plt.imsave("resized.png", resized_image)
    plt.show()
    
    return 0

if __name__=="__main__":
    imgs_path = "/home/pedro/Documents/color-finder-extension/backend/a_imgs"
    
    for file in os.listdir(imgs_path):
        img_path = os.path.join(imgs_path, file)
        main(img_path)
