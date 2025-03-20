import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from parameters import HTML_ACROMATIC_HSV_COLORS_RANGE, HTML_HSV_COLORS_RANGE

def faces_of_cube(lower_bound, upper_bound):
    x1,y1,z1 = lower_bound
    x2, y2, z2 = upper_bound
    # Define the cube vertices
    vertices = [
        [x1,y1,z1],  # Bottom-left-front
        [x2, y1, z1],  # Bottom-right-front
        [x2, y2, z1],  # Top-right-front
        [x1, y2, z1],  # Top-left-front
        [x1, y1, z2],  # Bottom-left-back
        [x2, y1, z2],  # Bottom-right-back
        [x2, y2, z2],  # Top-right-back
        [x1, y2, z2],  # Top-left-back
    ]
    
    # Define the six cube faces
    faces = [
        [vertices[0], vertices[1], vertices[2], vertices[3]],  # Front face
        [vertices[4], vertices[5], vertices[6], vertices[7]],  # Back face
        [vertices[0], vertices[1], vertices[5], vertices[4]],  # Bottom face
        [vertices[3], vertices[2], vertices[6], vertices[7]],  # Top face
        [vertices[0], vertices[3], vertices[7], vertices[4]],  # Left face
        [vertices[1], vertices[2], vertices[6], vertices[5]],  # Right face
    ]   
    
    return faces

# Create the figure
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Add the cube faces to the plot
for color, bounds in HTML_HSV_COLORS_RANGE.items():
    ax.add_collection3d(Poly3DCollection(faces_of_cube(bounds[0],bounds[1]), alpha=0.25, facecolors=color, edgecolors='black'))
# ax.add_collection3d(Poly3DCollection(faces_of_cube((0,50,0),(179,255,255)), alpha=0.25, facecolors="blue", edgecolors='black'))

# Set plot limits
ax.set_xlim([0, 200])
ax.set_ylim([0, 300])
ax.set_zlim([0, 300])

# Set labels
ax.set_xlabel('H-axis')
ax.set_ylabel('S-axis')
ax.set_zlabel('V-axis')

# Show the plot
plt.show()
