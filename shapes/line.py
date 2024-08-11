import numpy as np
from scipy.spatial.distance import cdist

def fit_line(points):
    # Compute the distance matrix between all pairs of points
    distances = cdist(points, points)
    
    # Find the indices of the two farthest points
    np.fill_diagonal(distances, 0)  # Set diagonal to zero to ignore self-pairing
    max_distance_index = np.unravel_index(np.argmax(distances), distances.shape)
    point1, point2 = points[max_distance_index[0]], points[max_distance_index[1]]
    
    return point1, point2

def line(points, num_points=100):
    # Find the two farthest points
    point1, point2 = fit_line(points)
    
    # Generate points evenly distributed between the two farthest points
    x_values = np.linspace(point1[0], point2[0], num=num_points)
    y_values = np.linspace(point1[1], point2[1], num=num_points)
    
    # Combine x and y values into a 2D array
    line_coords = np.column_stack((x_values, y_values))
    
    return line_coords