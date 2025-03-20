import cv2
import numpy as np
from parameters import HTML_HEX_COLORS
import math
from skimage.color import hsv2rgb, rgb2lab, deltaE_cie76

# Hexadecimal string to rgb
def hex_to_rgb(value: str):
    value = value.lstrip("#")
    lv = len(value)
    return tuple(int(value[i : i + lv // 3], 16) for i in range(0, lv, lv // 3))

def rgb_to_hsv(rgb: list):
    normal_rgb = tuple(v / 255 for v in rgb)
    red = normal_rgb[0]
    green = normal_rgb[1]
    blue = normal_rgb[2]
    H_value = 0
    S_value = 0
    V_value = 0
    maximo = max(normal_rgb)
    minimo = min(normal_rgb)

    if maximo != minimo:
        if maximo == red:
            if green >= blue:
                H_value = 60 * (green - blue) / (maximo - minimo)
            else:
                H_value = 360 + 60 * (green - blue) / (maximo - minimo)
        elif maximo == green:
            H_value = 120 + 60 * (blue - red) / (maximo - minimo)
        else:
            H_value = 240 + 60 * (red - green) / (maximo - minimo)
    else:
        H_value = 0

    if maximo > 0:
        S_value = (maximo - minimo) / maximo
    else:
        S_value = 0

    V_value = maximo
    H_value = H_value // 2
    return [int(H_value), int(S_value * 255), int(V_value * 255)]

def print_html_hsv_colors():
    print("{")
    for k, v in HTML_HEX_COLORS.items():
        print('    "' + k + '"' + ":" + str(rgb_to_hsv(hex_to_rgb(v))) + ",")
    print("}")
    return None

def find_closest(hsv_list:list, lookup_dict:dict):
    # Return the closest match from the dict
    def hsv_distance(hsv1, hsv2):
        rgb1 = hsv2rgb(hsv1)
        lab1 = rgb2lab(rgb1)
        rgb2 = hsv2rgb(hsv2)
        lab2 = rgb2lab(rgb2)
        print(deltaE_cie76(lab1, lab2))
        
        """Calculate the Euclidean distance between two HSV points."""
        return math.sqrt(
            (hsv1[0] - hsv2[0]) ** 2 +
            (hsv1[1] - hsv2[1]) ** 2 +
            (hsv1[2] - hsv2[2]) ** 2
        )
    res = dict()
    for hsv in hsv_list:
        closest_color = None
        min_distance = float('inf')
        for color_name, color_hsv in lookup_dict.items():
                distance = hsv_distance(hsv, color_hsv)
                if distance < min_distance:
                    min_distance = distance
                    closest_color = color_name
        if closest_color not in res.keys():
            res[closest_color] = hsv
        else:
            closest_color_reptition = closest_color+str(len(res.keys()))
            print(f"{closest_color} already in the dict and will be saved as {closest_color_reptition}")
            res[closest_color_reptition] = hsv
    return res

if __name__=="__main__":
    print_html_hsv_colors()