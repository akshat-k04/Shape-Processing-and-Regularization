import numpy as np
import io_process

def generate_circle(radius=1, num_points=500):
    theta = np.linspace(0, 2 * np.pi, num_points)
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    return np.column_stack((x, y))

def generate_ellipse(a=2, b=1, num_points=500):
    theta = np.linspace(0, 2 * np.pi, num_points)
    x = a * np.cos(theta)
    y = b * np.sin(theta)
    return np.column_stack((x, y))


def generate_rectangle(a=4, b=10, num_points=500):
    # Number of points per side
    points_per_side = num_points // 4
    remainder_points = num_points % 4
    
    # If the points are not evenly divisible, distribute the remainder points
    if remainder_points > 0:
        points_per_side += 1
    
    # Generate points for each side of the rectangle
    top_side = np.linspace(0, a, points_per_side, endpoint=False)
    right_side = np.linspace(0, b, points_per_side, endpoint=False)
    bottom_side = np.linspace(a, 0, points_per_side, endpoint=False)
    left_side = np.linspace(b, 0, points_per_side, endpoint=False)
    
    # Concatenate all points, ensuring the correct order
    x_coords = np.concatenate((top_side, np.full_like(right_side, a), bottom_side, np.full_like(left_side, 0)))
    y_coords = np.concatenate((np.full_like(top_side, 0), right_side, np.full_like(bottom_side, b), left_side))
    
    # Handle any remaining points
    if remainder_points > 0:
        extra_points = np.linspace(0, remainder_points * (a + b) / 4, remainder_points)
        if len(extra_points) > 0:
            x_coords = np.concatenate((x_coords, extra_points[:remainder_points]))
            y_coords = np.concatenate((y_coords, np.zeros(remainder_points)))
    
    # Return as an array of coordinates
    # io_process.plot(np.column_stack((x_coords, y_coords)))
    return np.column_stack((x_coords, y_coords))

def generate_line(length=1, num_points=500):
    """
    Generates points along a straight line segment.
    
    Parameters:
    - length (float): The length of the line segment.
    - num_points (int): The number of points to generate along the line segment.
    
    Returns:
    - numpy.ndarray: Array of shape (num_points, 2) containing the (x, y) coordinates of the line segment.
    """
    # Generate line segment points
    x_coords = np.linspace(0, length, num_points)
    y_coords = np.zeros(num_points)  # y-coordinate is zero for a horizontal line

    # Combine x and y coordinates
    return np.column_stack((x_coords, y_coords))


def generate_polygon(n_sides, num_points=500):
    """
    Generate points along the boundary of a polygon with n_sides.
    
    Parameters:
    - n_sides (int): Number of sides of the polygon.
    - num_points (int): Number of points to generate along the polygon boundary.
    
    Returns:
    - numpy.ndarray: Array of shape (num_points, 2) containing (x, y) coordinates of the polygon boundary.
    """
    if n_sides < 3:
        raise ValueError("Number of sides must be at least 3.")
    
    # Generate vertices of the polygon
    angles = np.linspace(0, 1, n_sides, endpoint=False)
    vertices = np.array([[np.cos(2 * np.pi*angle), np.sin(2 * np.pi*angle)] for angle in angles])
    
    # Interpolate points along the edges
    points = []
    edges = np.vstack([vertices, vertices[0]])  # Close the polygon by repeating the first vertex
    
    for i in range(n_sides):
        x0, y0 = edges[i]
        x1, y1 = edges[i + 1]
        edge_points = np.linspace([x0, y0], [x1, y1], num=int(num_points / n_sides), endpoint=False)
        points.extend(edge_points)
    # io_process.plot(np.array(points))
    return np.array(points)


def generate_star(num_points=500, num_vertices=5, inner_radius=1, outer_radius=2):
    """
    Generate points along the boundary of a star shape.
    
    Parameters:
    - num_points (int): Total number of points to generate along the star boundary.
    - num_vertices (int): Number of vertices of the star (typically 5 or 6).
    - inner_radius (float): Radius of the inner vertices of the star.
    - outer_radius (float): Radius of the outer vertices of the star.
    
    Returns:
    - numpy.ndarray: Array of shape (num_points, 2) containing (x, y) coordinates of the star boundary.
    """
    # Calculate the total number of points per side of the star
    points_per_side = num_points // (2 * num_vertices)
    
    # Create an array to hold the coordinates of the points
    star_coords = np.zeros((num_points, 2))
    
    for i in range(num_vertices):
        # Calculate the angle for the outer and inner vertices
        outer_angle = i * 2 * np.pi / num_vertices
        inner_angle = (i + 0.5) * 2 * np.pi / num_vertices
        
        # Compute the outer vertex
        outer_x = outer_radius * np.cos(outer_angle)
        outer_y = outer_radius * np.sin(outer_angle)
        
        # Compute the inner vertex
        inner_x = inner_radius * np.cos(inner_angle)
        inner_y = inner_radius * np.sin(inner_angle)
        
        # Generate points between the outer and inner vertices
        outer_points = np.linspace([outer_x, outer_y], [inner_x, inner_y], points_per_side, endpoint=False)
        star_coords[i * points_per_side * 2:(i * points_per_side * 2) + points_per_side] = outer_points
        
        if i < num_vertices - 1:
            next_outer_angle = (i + 1) * 2 * np.pi / num_vertices
            next_outer_x = outer_radius * np.cos(next_outer_angle)
            next_outer_y = outer_radius * np.sin(next_outer_angle)
        else:
            next_outer_x = outer_radius * np.cos(0)
            next_outer_y = outer_radius * np.sin(0)
        
        inner_points = np.linspace([inner_x, inner_y], [next_outer_x, next_outer_y], points_per_side, endpoint=False)
        star_coords[(i * points_per_side * 2) + points_per_side:(i + 1) * points_per_side * 2] = inner_points
    
    return star_coords