import numpy as np
from scipy.spatial.distance import cdist

def generate_star(num_points=500, num_vertices=5, inner_radius=1, outer_radius=2):
    points_per_side = num_points // (2 * num_vertices)
    star_coords = np.zeros((num_points, 2))
    
    for i in range(num_vertices):
        outer_angle = i * 2 * np.pi / num_vertices
        inner_angle = (i + 0.5) * 2 * np.pi / num_vertices
        
        outer_x = outer_radius * np.cos(outer_angle)
        outer_y = outer_radius * np.sin(outer_angle)
        
        inner_x = inner_radius * np.cos(inner_angle)
        inner_y = inner_radius * np.sin(inner_angle)
        
        outer_points = np.linspace([outer_x, outer_y], [inner_x, inner_y], points_per_side, endpoint=False)
        star_coords[i * points_per_side * 2:(i * points_per_side * 2) + points_per_side] = outer_points
        
        next_outer_angle = (i + 1) * 2 * np.pi / num_vertices
        next_outer_x = outer_radius * np.cos(next_outer_angle)
        next_outer_y = outer_radius * np.sin(next_outer_angle)
        
        inner_points = np.linspace([inner_x, inner_y], [next_outer_x, next_outer_y], points_per_side, endpoint=False)
        star_coords[(i * points_per_side * 2) + points_per_side:(i + 1) * points_per_side * 2] = inner_points
    
    return star_coords

def rotate_points(points, angle):
    angle_rad = np.radians(angle)
    rotation_matrix = np.array([
        [np.cos(angle_rad), -np.sin(angle_rad)],
        [np.sin(angle_rad), np.cos(angle_rad)]
    ])
    rotated_points = np.dot(points, rotation_matrix.T) 
    return rotated_points

def fit_star_to_points(points):
    # Calculate the center of the points
    center = np.mean(points, axis=0)
    
    # Calculate the maximum distance between any two points (diameter of the enclosing circle)
    distances = cdist(points, points)
    max_distance = np.max(distances)
    
    # Estimate the outer and inner radius
    outer_radius = max_distance / 2
    inner_radius = outer_radius * 0.4
    return 5, inner_radius, outer_radius, center

def brute_force_star_rotation(points, num_points=500, num_vertices=5, inner_radius=1, outer_radius=2):
    best_angle = 0
    min_error = float('inf')
    
    center = np.mean(points, axis=0)
    star_coords = generate_star(num_points=num_points, num_vertices=num_vertices, inner_radius=inner_radius, outer_radius=outer_radius)
    
    for angle in range(0, 360, 72):  # Brute-force from 0° to 360° with step 72°
        rotated_star_coords = rotate_points(star_coords, angle)
        distances = cdist(points, rotated_star_coords)
        error = np.mean(np.min(distances, axis=1))
        
        if error < min_error:
            min_error = error
            best_angle = angle
    
    return best_angle

def star(points, num_points=500):
    # Fit the star parameters
    
    
    num_vertices, inner_radius, outer_radius, center = fit_star_to_points(points)

    for i in range(len(points)):
        points[i] = [points[i][0]-center[0],points[i][1]-center[1]]

    # Get the best rotation angle
    best_angle = brute_force_star_rotation(points, num_points=num_points, num_vertices=num_vertices, inner_radius=inner_radius, outer_radius=outer_radius)
    
    # Generate the star shape with the found parameters
    star_coords = generate_star(num_points=num_points, num_vertices=num_vertices, inner_radius=inner_radius, outer_radius=outer_radius)
    
    # Rotate the star coordinates to match the best angle
    rotated_star_coords = rotate_points(star_coords, best_angle)

    for i in range(len(rotated_star_coords)):
        rotated_star_coords[i] = rotated_star_coords[i] + center 
    
    
    return rotated_star_coords
