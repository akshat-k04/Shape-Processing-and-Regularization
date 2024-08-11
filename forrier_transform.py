import numpy as np
from scipy.interpolate import interp1d

def compute_fourier_descriptors(coordinates):
    coordinates = np.vstack(coordinates) 
    # print(coordinates.size)
    complex_coords = coordinates[:, 0] + 1j * coordinates[:, 1]
    fourier_descriptors = np.fft.fft(complex_coords)
    return fourier_descriptors


# Normalize descriptors (optional step for invariance)
def normalize_descriptors(descriptors):
    # Ignore the first coefficient (DC component)
    descriptors = descriptors[1:]
    # Normalize by the magnitude of the first remaining descriptor
    descriptors /= np.abs(descriptors[0])
    return descriptors


