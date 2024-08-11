import numpy as np
from sklearn.decomposition import PCA

def polygon(points, num_sides=None, num_points=300):
    num_points = len(points) 
    def fit_polygon(points, num_sides):
        # Perform PCA to find the main axes
        pca = PCA(n_components=2)
        pca.fit(points)
        principal_components = pca.components_
        center = np.mean(points, axis=0)
        
        # Calculate the width and height of the bounding box
        projected_points = pca.transform(points)
        min_x, max_x = np.min(projected_points[:, 0]), np.max(projected_points[:, 0])
        min_y, max_y = np.min(projected_points[:, 1]), np.max(projected_points[:, 1])
        
        width = max_x - min_x
        height = max_y - min_y
        
        # Calculate rotation angle
        angle = np.arctan2(principal_components[1, 1], principal_components[1, 0])
        
        return center, width, height, np.degrees(angle)
    
    def generate_polygon_points(center, width, height, angle, num_sides, num_points):
        # Radius of the circumscribed circle of the polygon
        radius = min(width, height) / 2
        
        # Generate points of a regular polygon
        theta = np.linspace(0, 2 * np.pi, num_sides, endpoint=False)
        polygon_points = np.array([
            [radius * np.cos(t), radius * np.sin(t)]
            for t in theta
        ])
        
        # Rotate and translate the polygon
        rotation_matrix = np.array([
            [np.cos(np.radians(angle)), -np.sin(np.radians(angle))],
            [np.sin(np.radians(angle)), np.cos(np.radians(angle))]
        ])
        
        rotated_polygon = np.dot(polygon_points, rotation_matrix.T) + center
        
        # Compute perimeter and generate points
        def distance(p1, p2):
            return np.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)
        
        def interpolate(p1, p2, num_points):
            return np.linspace(p1, p2, num_points, endpoint=False)
        
        # Generate points along the perimeter of the polygon
        all_points = []
        num_points_per_side = num_points // num_sides
        
        for i in range(num_sides):
            p1 = rotated_polygon[i]
            p2 = rotated_polygon[(i + 1) % num_sides]
            all_points.extend(interpolate(p1, p2, num_points_per_side))
        
        return np.array(all_points)
    
    if num_sides is None:
        raise ValueError("Number of sides must be specified.")
    
    # Fit the polygon to the points
    center, width, height, angle = fit_polygon(points, num_sides)
    
    # Generate points along the perimeter of the fitted polygon
    return generate_polygon_points(center, width, height, angle, num_sides, num_points)
