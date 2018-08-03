import math

import numpy as np
from scipy import ndimage as ndi
from skimage.filters import gabor_kernel


def create_gabor_bank(thetas, sigma, frequencies):
    filterbank = []
    for theta in thetas:
        theta = theta / float(len(thetas)) * math.pi
        for sigma in sigmas:
            for frequency in frequencies:
                kernel = np.real(gabor_kernel(frequency, theta=theta,
                                              sigma_x=sigma, sigma_y=sigma))
                filterbank.append(kernel)

def convolve_gabors():
    return NotImplemented