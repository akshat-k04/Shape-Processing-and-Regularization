import numpy as np
from scipy.spatial.distance import euclidean

def fit_circle(points):
    # Fit a circle to the given points using the least squares method
    x = points[:, 0]
    y = points[:, 1]
    
    # Design matrix
    A = np.c_[x, y, np.ones(points.shape[0])]
    b = x**2 + y**2
    
    # Solve the normal equation
    coeffs, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
    
    # Parameters of the circle
    cx = coeffs[0] / 2
    cy = coeffs[1] / 2
    radius = np.sqrt(coeffs[2] + cx**2 + cy**2)
    
    return cx, cy, radius



def circle(polyline):
    # Convert polylines to a numpy array for easier manipulation
    points = np.vstack(polyline)

    # Fit a circle to the points
    cx, cy, radius = fit_circle(points)


    # Generate angles
    angles = np.linspace(0, 2 * np.pi, len(polyline), endpoint=False)

    # Compute coordinates
    x = cx + radius * np.cos(angles)
    y = cy + radius * np.sin(angles)

    # Combine into a 2D array
    circle_coords = np.column_stack((x, y))
    return circle_coords