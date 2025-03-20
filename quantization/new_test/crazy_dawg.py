# The input is a list of (H,S,V) values. The output is the name of the color that is the closest to that coordinate
import math

HTML_HSV_COLORS = {
    "red": [0, 255, 255],
    "cyan": [90, 255, 255],
    "blue": [120, 255, 255],
    "darkblue": [120, 255, 139],
    "lightblue": [97, 63, 230],
    "purple": [150, 255, 128],
    "yellow": [30, 255, 255],
    "lime": [60, 255, 255],
    "magenta": [150, 255, 255],
    "pink": [174, 63, 255],
    "orange": [19, 255, 255],
    "brown": [0, 190, 165],
    "maroon": [0, 255, 128],
    "green": [60, 255, 128],
    "olive": [30, 255, 128],
    "aquamarine": [79, 128, 255],
}

def find_nearest(input_hsv_list):
    # Create the ranges, brute force style
    res = {key: [[255,255,255],[0,0,0]] for key in HTML_HSV_COLORS}
    
    def hsv_distance(hsv1, hsv2):
        """Calculate the Euclidean distance between two HSV points."""
        return math.sqrt(
            (hsv1[0] - hsv2[0]) ** 2 +
            (hsv1[1] - hsv2[1]) ** 2 +
            (hsv1[2] - hsv2[2]) ** 2
        )

    for hsv in input_hsv_list:
        closest_color = None
        min_distance = float('inf')
        for color_name, color_hsv in HTML_HSV_COLORS.items():
            distance = hsv_distance(hsv, color_hsv)
            if distance < min_distance:
                min_distance = distance
                closest_color = color_name
        
        if hsv[0]<=res[closest_color][0][0]:
            res[closest_color][0][0]=hsv[0]
        
        if hsv[0]>res[closest_color][1][0]:
            res[closest_color][1][0]=hsv[0]
        
        if hsv[1]<=res[closest_color][0][1]:
            res[closest_color][0][1]=hsv[1]
        
        if hsv[1]>res[closest_color][1][1]:
            res[closest_color][1][1]=hsv[1]
        
        if hsv[2]<=res[closest_color][0][2]:
            res[closest_color][0][2]=hsv[2]
        
        if hsv[2]>res[closest_color][1][2]:
            res[closest_color][1][2]=hsv[2]
            
    return res

start = (0, 20, 20)
end = (179, 255, 255)

# Ficou bom
# start = (0, 50, 50)
# end = (179, 255, 255)

step_hue = 1
step_saturation = 1
step_value = 1

points = [
    (h, s, v)
    for h in range(start[0], end[0] + 1, step_hue)
    for s in range(start[1], end[1] + 1, step_saturation)
    for v in range(start[2], end[2] + 1, step_value)
]

print(f"Generated {len(points)} points.")

response = find_nearest(points)

print("{")
for c, bound in response.items():
    print(f'    "{c}":{bound},')
print("}")
