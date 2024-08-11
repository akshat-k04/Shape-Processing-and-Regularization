import numpy as np
from numpy.linalg import lstsq
from scipy.spatial.distance import euclidean


def fit_ellipse(points):
    # Fit an ellipse to the given points using the least squares method
    x = points[:, 0]
    y = points[:, 1]
    
    # Design matrix
    D = np.array([x**2, x*y, y**2, x, y, np.ones_like(x)]).T
    S = np.dot(D.T, D)
    C = np.zeros([6, 6])
    C[0, 2] = 2
    C[1, 1] = -1
    C[2, 0] = 2
    
    # Solve the generalized eigenvalue problem
    E, V = np.linalg.eig(np.dot(np.linalg.inv(S), C))
    n = np.argmax(np.abs(E))
    a = V[:, n]
    
    # Parameters of the ellipse
    a, b, c, d, e, f = a
    return a, b, c, d, e, f

def ellipse_parameters(a, b, c, d, e, f):
    # Calculate ellipse parameters from the quadratic form coefficients
    num = b*b - 4*a*c
    if num >= 0:
        return None  # Not an ellipse
    x0 = (2*c*d - b*e) / num
    y0 = (2*a*e - b*d) / num
    
    term = np.sqrt((a-c)**2 + b**2)
    width = np.sqrt(2*(a*e*e+c*d*d+f*b*b-2*b*d*e-4*a*c*f)/((b*b-a*c)*(term-(a+c))))
    height = np.sqrt(2*(a*e*e+c*d*d+f*b*b-2*b*d*e-4*a*c*f)/((b*b-a*c)*(-term-(a+c))))
    
    angle = 0.5 * np.arctan(b/(a-c))
    
    return (x0, y0), width, height, angle

# def error_for_ellipse(centroid, width, height, ellipse_angle, points):
#     a = width / 2
#     b = height / 2
#     cx, cy = centroid
    
#     # Angle calculation
#     angle = np.arctan2(points[:,1] - cy, points[:,0] - cx)
#     relative_angle = angle - ellipse_angle
    
#     # Ellipse coordinates calculation
#     x_ellipse = cx + a * np.cos(relative_angle) * np.cos(ellipse_angle) - b * np.sin(relative_angle) * np.sin(ellipse_angle)
#     y_ellipse = cy + a * np.cos(relative_angle) * np.sin(ellipse_angle) + b * np.sin(relative_angle) * np.cos(ellipse_angle)
    
#     fraction = []
#     for i in range(len(points)):
#         dist_to_ellipse = euclidean([x_ellipse[i], y_ellipse[i]], points[i])
#         dist_to_centroid = euclidean(centroid, points[i])
#         fraction.append(dist_to_ellipse / dist_to_centroid)
    
#     return np.mean(fraction) 


def ellipse(polyline):
    points = np.vstack(polyline)
    coeffs = fit_ellipse(points)
    params = ellipse_parameters(*coeffs)
    
    if params is None:
        return None
    
    centroid, width, height, angle = params

    # Generate points on the ellipse
    num_points = 300
    theta = np.linspace(0, 2 * np.pi, num_points)
    a = width / 2
    b = height / 2
    cx, cy = centroid

    # Parametric equations for ellipse
    x = cx + a * np.cos(theta) * np.cos(angle) - b * np.sin(theta) * np.sin(angle)
    y = cy + a * np.cos(theta) * np.sin(angle) + b * np.sin(theta) * np.cos(angle)

    return np.column_stack((x, y))