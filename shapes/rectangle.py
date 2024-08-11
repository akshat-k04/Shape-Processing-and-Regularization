import numpy as np
from sklearn.decomposition import PCA

def rectangle(points, num_points=300):
    num_points = len(points) 
    def fit_rectangle(points):
        # Perform PCA to find the main axes
        pca = PCA(n_components=2)
        pca.fit(points)
        principal_components = pca.components_
        center = np.mean(points, axis=0)
        
        # Calculate the width and height
        projected_points = pca.transform(points)
        min_x, max_x = np.min(projected_points[:, 0]), np.max(projected_points[:, 0])
        min_y, max_y = np.min(projected_points[:, 1]), np.max(projected_points[:, 1])
        
        width = max_x - min_x
        height = max_y - min_y
        
        # Calculate rotation angle
        angle = np.arctan2(principal_components[1, 1], principal_components[1, 0])
        
        return center, width, height, np.degrees(angle)
    
    def generate_rectangle_points(center, width, height, angle, num_points):
        # Calculate the four corners of the rectangle
        cx, cy = center
        half_w, half_h = width / 2, height / 2
        
        # Corners of the rectangle before rotation
        corners = np.array([
            [cx - half_w, cy - half_h],
            [cx + half_w, cy - half_h],
            [cx + half_w, cy + half_h],
            [cx - half_w, cy + half_h]
        ])
        
        # Rotation matrix
        theta = np.radians(angle)
        cos_theta, sin_theta = np.cos(theta), np.sin(theta)
        rotation_matrix = np.array([
            [cos_theta, -sin_theta],
            [sin_theta, cos_theta]
        ])
        
        # Rotate corners
        rotated_corners = np.dot(corners - center, rotation_matrix) + center
        
        # Compute perimeter
        def distance(p1, p2):
            return np.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)
        
        side_lengths = [
            distance(rotated_corners[0], rotated_corners[1]),
            distance(rotated_corners[1], rotated_corners[2]),
            distance(rotated_corners[2], rotated_corners[3]),
            distance(rotated_corners[3], rotated_corners[0])
        ]
        perimeter = sum(side_lengths)
        
        # Generate points
        points = []
        segment_length = perimeter / num_points
        accumulated_length = 0
        
        def add_points_on_segment(p1, p2, num_points):
            nonlocal accumulated_length
            segment_dist = distance(p1, p2)
            segment_points = int(np.round(num_points * segment_dist / perimeter))
            for i in range(segment_points):
                t = i / segment_points
                x = p1[0] + t * (p2[0] - p1[0])
                y = p1[1] + t * (p2[1] - p1[1])
                points.append([x, y])
                accumulated_length += segment_length
        
        for i in range(4):
            p1, p2 = rotated_corners[i], rotated_corners[(i + 1) % 4]
            add_points_on_segment(p1, p2, num_points)
        
        return np.array(points)

    # Fit the rectangle to the points
    center, width, height, angle = fit_rectangle(points)
    
    # Generate points along the perimeter of the fitted rectangle
    return generate_rectangle_points(center, width, height, angle, num_points)
