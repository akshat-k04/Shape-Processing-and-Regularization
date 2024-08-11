import numpy as np
from scipy.ndimage import gaussian_filter1d
from scipy import stats

def regularize(coords,sigma = 1):
    # Extract x and y coordinates
    x = coords[:, 0]
    y = coords[:, 1]

    # Smooth the coordinates
    # sigma is Standard deviation for Gaussian kernel
    x_smooth = gaussian_filter1d(x, sigma=sigma)
    y_smooth = gaussian_filter1d(y, sigma=sigma)

    # Combine smoothed coordinates
    coords_smooth = np.column_stack((x_smooth, y_smooth))
    return coords_smooth




def remove_outliers(coordinates, threshold=3):
    """
    Removes outliers from a set of 2D coordinates based on the Z-score.
    
    Parameters:
    - coordinates: list of tuples [(x1, y1), (x2, y2), ...]
    - threshold: Z-score threshold to identify outliers (default is 3)
    
    Returns:
    - A list of coordinates with outliers removed.
    """
    # Convert coordinates to a numpy array
    data = np.array(coordinates)
    
    # Calculate Z-scores
    z_scores_x = np.abs(stats.zscore(data[:, 0]))
    z_scores_y = np.abs(stats.zscore(data[:, 1]))
    
    # Filter out coordinates with a Z-score greater than the threshold
    non_outliers = (z_scores_x < threshold) & (z_scores_y < threshold)
    
    return data[non_outliers]