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
from sklearn.metrics import silhouette_score

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

def image_quantization(image: np.ndarray, range_n_clusters=[5, 10, 15]):
    """
    Perform image quantization using KMeans clustering and select best number of clusters using silhouette score.
    """
    
    # Step 1: Resize image to 600x400 to reduce computation
    modified_image_raw = cv2.resize(image, (600, 400), interpolation=cv2.INTER_AREA)

    # Step 2: Flatten image
    array_modified_image = modified_image_raw.reshape(-1, 3)

    # Step 3: Sample pixels
    sample_size = 10000
    if array_modified_image.shape[0] > sample_size:
        sample_indices = np.random.choice(array_modified_image.shape[0], size=sample_size, replace=False)
        sampled_array = array_modified_image[sample_indices]
    else:
        sampled_array = array_modified_image

    # Step 4: Find best n_clusters using silhouette score
    best_n_clusters = None
    best_score = -1
    best_kmeans = None

    for n_clusters in range_n_clusters:
        kmeans = KMeans(n_clusters=n_clusters, n_init='auto', random_state=42)
        labels = kmeans.fit_predict(sampled_array)
        score = silhouette_score(sampled_array, labels)
        print(f"n_clusters = {n_clusters}, silhouette_score = {score:.4f}")
        if score > best_score:
            best_score = score
            best_n_clusters = n_clusters
            best_kmeans = kmeans

    print(f"Best number of clusters: {best_n_clusters} with score: {best_score:.4f}")

    # Step 5: Fit KMeans on the full array with best cluster count
    final_kmeans = KMeans(n_clusters=best_n_clusters, n_init='auto', random_state=42)
    final_labels = final_kmeans.fit_predict(array_modified_image)

    # Step 6: Reconstruct quantized image
    center_colors = final_kmeans.cluster_centers_.astype(int)
    quantized_image = center_colors[final_labels].reshape(modified_image_raw.shape).astype(np.uint8)

    # Step 7: Count colors and generate name map
    counts = dict(Counter(final_labels))
    counts = dict(sorted(counts.items()))

    quant_colors = [center_colors[i] for i in counts.keys()]
    name_quantColorRGB = find_closest(quant_colors, HTML_HSV_COLORS)
    name_quantColorHEX = {k: RGB2HEX(v) for k, v in name_quantColorRGB.items()}

    return modified_image_raw, quantized_image, name_quantColorRGB