# create_hsv_bounds(HTML_HSV_COLORS)

import numpy as np
import cv2 as cv
 
img = cv.imread('bird.jpg')
Z = img.reshape((-1,3))
 
# convert to np.float32
Z = np.float32(Z)
 
# define criteria, number of clusters(K) and apply kmeans()
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
K = 8
ret,label,center=cv.kmeans(Z,K,None,criteria,10,cv.KMEANS_RANDOM_CENTERS)
 
# Now convert back into uint8, and make original image
center = np.uint8(center)

res = center[label.flatten()]
res2 = res.reshape((img.shape))

cv2.imwrite("result.jpg",res2)
for rgb_c in center:
    hsv_c = rgb_to_hsv(tuple(rgb_c))
    print(hsv_c)

hsv = cv2.cvtColor(res2, cv2.COLOR_BGR2HSV)

for color,bounds in HTML_HSV_COLORS_RANGE.items():
    mask = cv2.inRange(hsv, tuple(bounds[0]), tuple(bounds[1]))
    result = cv2.bitwise_and(res2, res2, mask=mask)
    cv2.imwrite(f"folder/mask_{color}.jpg", mask)
