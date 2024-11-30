import fourier_transform
import generate_basic_shape
import numpy as np

def compute_error(known_descriptors, unknown_descriptors):
        # Ensure the descriptors are of the same length
        min_length = min(len(known_descriptors), len(unknown_descriptors))
        known_descriptors = known_descriptors[:min_length]
        unknown_descriptors = unknown_descriptors[:min_length]
    
        # Calculate the magnitude of the descriptors
        known_magnitude = np.abs(known_descriptors)
        unknown_magnitude = np.abs(unknown_descriptors)
    
        # Compute the Euclidean distance (error)
        error = np.linalg.norm(known_magnitude - unknown_magnitude)
        return error


class Shapes:
     
    def generate_shape(self,length,shapes):
        self.basic_shape_descriptors =[]
        for name in shapes:

            if name=="circle":
                coords = generate_basic_shape.generate_circle(num_points=length)
            elif name=="ellipse":
                coords = generate_basic_shape.generate_ellipse(num_points=length)
            elif name=="rectangle":
                coords = generate_basic_shape.generate_rectangle(num_points=length)
            elif name=="line":
                coords = generate_basic_shape.generate_line(num_points=length)
            elif name=="star":
                coords = generate_basic_shape.generate_star(num_points=length)
            elif name=="triangle":
                coords = generate_basic_shape.generate_polygon(n_sides=3,num_points=length)
            elif name=="square":
                coords = generate_basic_shape.generate_polygon(n_sides=4,num_points=length)
            elif name=="pentagon":
                coords = generate_basic_shape.generate_polygon(n_sides=5,num_points=length)
            elif name=="hexagon":
                coords = generate_basic_shape.generate_polygon(n_sides=6,num_points=length)
            # elif name=="heptagon":
            #     coords = generate_basic_shape.generate_polygon(n_sides=7,num_points=length)
            # elif name=="octagon":
            #     coords = generate_basic_shape.generate_polygon(n_sides=8,num_points=length)
            else:
                continue 
            descriptors =  fourier_transform.compute_fourier_descriptors(coords)
            normalized_descriptor = fourier_transform.normalize_descriptors(descriptors)
            self.basic_shape_descriptors.append(normalized_descriptor) 




    def check_shape(self,polyline,threshold = 0.3):
        shapes = ["circle","ellipse","rectangle","line","star","triangle","square","pentagon","hexagon"] #"heptagon","octagon"
        threshold_limits = [0.1,0.3,0.3,0.15,0.2,0.2,0.15,0.1,0.1]
        shape_descriptors = fourier_transform.compute_fourier_descriptors(polyline) 
        normalized_shape_descriptors = fourier_transform.normalize_descriptors(descriptors=shape_descriptors)

        self.generate_shape(len(polyline),shapes)


        # checking the error
        basic_shape_error =[] 
        # finding minimum error

        for i in range(len(self.basic_shape_descriptors)):
            temp = compute_error(normalized_shape_descriptors,self.basic_shape_descriptors[i]) 
            temp = np.round(temp,4)
            basic_shape_error.append([temp,shapes[i],threshold_limits[i]]) 


        basic_shape_error.sort()
        # print(basic_shape_error)

        for i in basic_shape_error:
            if i[1]=='pentagon' or i[1]== 'hexagon':
                continue 
            elif i[0]<=i[2]:
                return i[1] 
            
        for i in basic_shape_error:
            if i[0]<=i[2]:
                return i[1] 

        return "unknown"