import numpy as np
from sklearn.decomposition import PCA
from scipy.spatial.distance import cdist

def process_points(points, threshold=10):
    def find_symmetry_axis(points):
        # Perform PCA to get the principal components
        pca = PCA(n_components=2)
        pca.fit(points)
        components = pca.components_
        
        # The first principal component is the major axis
        major_axis = components[0]
        
        # Calculate the mean point (center of the shape)
        center = np.mean(points, axis=0)
        
        # The angle of the major axis
        angle_major = np.arctan2(major_axis[1], major_axis[0])
        
        return center, angle_major
    
    def reflect_across_line(points, angle, center):
        # Convert angle to radians
        theta = angle
        
        # Define the rotation matrix to align the symmetry axis with the x-axis
        rotation_matrix = np.array([
            [np.cos(theta), -np.sin(theta)],
            [np.sin(theta), np.cos(theta)]
        ])
        
        # Translate points to align the center with the origin
        translated_points = points - center
        
        # Rotate points to align symmetry axis with x-axis
        rotated_points = np.dot(translated_points, rotation_matrix.T)
        
        # Reflect across the x-axis
        reflected_points = np.array([
            [x, -y] for x, y in rotated_points
        ])
        
        # Rotate back and translate points
        reflected_points = np.dot(reflected_points, rotation_matrix)
        reflected_points += center
        
        return reflected_points
    
    def calculate_error(original_points, transformed_points):
        # Calculate the mean squared error between original and symmetric points
        distances = cdist(original_points, transformed_points)
        min_distances = np.min(distances, axis=1)
        return np.mean(min_distances)
    
    def adjust_for_symmetry(points, threshold=0.1):
        center, angle_major = find_symmetry_axis(points)
        
        # Reflect points across the major axis
        reflected_points = reflect_across_line(points, angle_major, center)
        
        # Calculate the error between original and reflected points
        error = calculate_error(points, reflected_points)
        
        if error <= threshold:
            return reflected_points
        else:
            return points
    
    # Check and adjust symmetry
    symmetric_points = adjust_for_symmetry(points, threshold)
    
    return symmetric_points

# Example usage
points = np.array([
    [1, 2], [2, 4], [4, 5], [6, 4], [5, 2], [3, 1]
])  # Replace this with your actual points
processed_points = process_points(points, threshold=0.1)
print("Processed points:")
print(processed_points)
