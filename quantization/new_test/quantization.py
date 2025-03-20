# Quantization will be made. With HTML_HSV_COLOR, find for each HSV in the center list, the nearest HSV color code

import numpy as np
import scipy
import cv2
from utils import rgb_to_hsv, find_closest
from parameters import HTML_HSV_COLORS
import matplotlib.pyplot as plt
import math
import re
 
def find_colors_quantizited_img(float32_img:np.float32, n_clusters:int):
    # Create the quantizited image. Also show hsv value and color name
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 5000, 0.5)
    continue_loop = True
    prev_label = None
    rgb_centers = None
    
    # This loop was made to make unique clusters. WIthout this loop, with a large n_cluster size, some colors name can repeat and
    # wouldn't make sense
    while continue_loop:
        ret,label,rgb_centers=cv2.kmeans(float32_img,n_clusters,None,criteria,10,cv2.KMEANS_PP_CENTERS)
        
        # Now convert back into uint8, and make original image
        rgb_centers = np.uint8(rgb_centers)

        res = rgb_centers[label.flatten()]
        res2 = res.reshape((img.shape))
        
        hsv_centers = [rgb_to_hsv(rgb_c) for rgb_c in rgb_centers]

        colors = find_closest(hsv_centers,HTML_HSV_COLORS)
        printed = []
        repetidas = []
        for c in colors:
            c_no_num = re.sub(r'\d', '', c)
            if c_no_num not in printed:
                printed.append(c_no_num)
            else:
                repetidas.append(c_no_num)
        
        if len(repetidas)>0:
            n_clusters-=1
            print(f"Trying again with {n_clusters} clusters.")
        else:
            hsv_res2 = cv2.cvtColor(res2,cv2.COLOR_RGB2HSV)
            return hsv_res2, colors

def point_colors(quant_img, colors:dict, kernel_size:int):
    resized = cv2.resize(quant_img, (quant_img.shape[0]*2, quant_img.shape[1]*2)) 

    borderType = cv2.BORDER_CONSTANT
    top = int(0.5 * resized.shape[0])
    bottom = top
    left = int(0.5 * resized.shape[1])
    right = left
    # Copy with borders where the name of the color will be placed
    image_res = cv2.copyMakeBorder(resized, top, bottom, left, right, borderType, None, value=(255,255,255))
    
    # with np.printoptions(threshold=np.inf):
    #     print(quant_img)
        
    for color, hsv_code in colors.items():
        lower_code = [hsv_code[0]-1,hsv_code[1]-1,hsv_code[2]-1]
        upper_code = [hsv_code[0]+1,hsv_code[1]+1,hsv_code[2]+1]
        
        mask = cv2.inRange(quant_img, tuple(lower_code), tuple(upper_code))
        # kernel = np.ones((kernel_size, kernel_size), np.uint8)
        # dilated = cv2.dilate(mask, kernel, iterations=1) 
        # erode = cv2.erode(dilated,(8, 8), iterations=1)
        
        num_labels, labels_img = cv2.connectedComponents(mask)
        output_img = np.zeros((mask.shape[0], mask.shape[1], 3), dtype=np.uint8)

        # Assign a random color to each label (skip the background, label 0)
        for label in range(1, num_labels):
            cor = np.random.randint(0, 255, size=3)
            output_img[labels_img == label] = cor
            
        # result = cv2.bitwise_and(quant_img,quant_img,mask = mask)
        print(num_labels-1)
        cv2.imwrite(f"folder/mask_{color}.jpg", mask)
        cv2.imwrite(f"folder/result_{color}.jpg", cv2.cvtColor(output_img,cv2.COLOR_HSV2BGR))

    return quant_img

if __name__=="__main__":
    # Variaveis: N clusters 
    N_CLUSTERS = 6
    KERNEL_SIZE = 5
    img = cv2.imread('bird.jpg')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    Z = img.reshape((-1,3))
    Z = np.float32(Z)
    
    quantizited_img, colors = find_colors_quantizited_img(Z, N_CLUSTERS)
    output_name = "result.jpg"
    # res_img = point_colors(quantizited_img, colors, KERNEL_SIZE)
    # cv2.imwrite(output_name,cv2.cvtColor(res_img,cv2.COLOR_HSV2BGR))
    print(f"The only colors in the image {output_name} are: {colors}")
    plt.imshow(quantizited_img)
    plt.show()