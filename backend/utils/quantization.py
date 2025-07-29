from sklearn.cluster import KMeans
import numpy as np
import cv2
import matplotlib.pyplot as plt
from collections import Counter
from skimage.color import rgb2lab, deltaE_cie76, lab2rgb
import os
from configs.parameters import BASIC_HSV_COLORS, HTML_HSV_COLORS, X11_HSV_COLORS
import plotly.express as px
import plotly.graph_objects as go

def plot_kmeans(points, labels, color_list): 
    height, width, _ = points.shape
    
    total_points_size = height*width
    num_pixels = int(total_points_size*0.1)

    # Seleciona pixels aleatórios
    random_coords = np.random.randint(0, [height, width], size=(num_pixels, 2))
    random_y, random_x = random_coords[:, 0], random_coords[:, 1]
    
    random_pixels = points[random_y, random_x]
    random_pixels_labels = labels[random_y * width + random_x]
    colors = np.array([color_list[label] for label in random_pixels_labels]) / 255

    r, g, b = random_pixels[:, 0], random_pixels[:, 1], random_pixels[:, 2]

    # Cria scatter plot interativo
    fig = go.Figure(data=[go.Scatter3d(
        x=r, y=g, z=b,
        mode='markers',
        marker=dict(size=2, color=colors, opacity=0.7)
    )])

    fig.update_layout(title="K-Means Clustering", scene=dict(
        xaxis_title="Red",
        yaxis_title="Green",
        zaxis_title="Blue"
    ))

    fig.show()  # Renderiza muito mais rápido

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
        response[smallest_diff_name] = center.tolist()
    return response

def RGB2HEX(color):
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))

def image_quantization(image: np.ndarray, number_of_colors: int):
    """
    Perform image quantization using KMeans clustering.

    Args:
        image (np.ndarray): Input image as a NumPy array (in BGR format).
        number_of_colors (int): Desired number of dominant colors to quantize to.

    Returns:
        modified_image_raw (np.ndarray): Resized version of the original image (600x400).
        quantized_image (np.ndarray): Image reconstructed using the quantized colors.
        name_quantColorRGB (dict): Dictionary mapping color names to their RGB values.
    """
    
    # Resize the image to reduce computation time
    modified_image_raw = cv2.resize(image, (600, 400), interpolation=cv2.INTER_AREA)

    # Reshape image to a 2D array of pixels (rows: pixels, columns: B, G, R)
    modified_image = modified_image_raw.reshape(-1, 3)

    # Apply KMeans clustering to find dominant colors
    clf = KMeans(n_clusters=number_of_colors, n_init='auto', random_state=42)
    labels = clf.fit_predict(modified_image)

    # Count number of pixels per cluster
    counts = Counter(labels)
    counts = dict(sorted(counts.items()))

    # Get cluster centers (i.e., dominant colors)
    center_colors = clf.cluster_centers_.astype(int)
    quant_colors = [center_colors[i] for i in counts.keys()]

    # Replace each pixel with the color of its cluster
    quantized_image = center_colors[labels]
    quantized_image = quantized_image.reshape(400, 600, 3).astype(np.uint8)

    # Map RGB values to their closest HTML HSV-based color names
    name_quantColorRGB = find_closest(quant_colors, HTML_HSV_COLORS)

    # Convert RGB colors to HEX format
    name_quantColorHEX = {k: RGB2HEX(v) for k, v in name_quantColorRGB.items()}

    return modified_image_raw, quantized_image, name_quantColorRGB