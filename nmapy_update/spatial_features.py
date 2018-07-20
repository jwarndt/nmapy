import time

import matplotlib.pyplot as plt
import skimage
from skimage.feature import hog, greycomatrix, greycoprops
from skimage.color import rgb2gray
import gdal
import numpy as np

def hog_feature(image_name, block, scale):
    """
    Parameters:
    ----------
    image_name: str
    block: int
    scale: int
    
    Returns:
    --------
    out_image: 3D ndarray
    """
    ds = gdal.Open(image_name)
    image = ds.ReadAsArray()
    ds = None
    image = np.moveaxis(image, 0, -1) # expects an image in rows, columns, channels
    out_image = []
    for i in range(int(scale/2), image.shape[0] - int(scale/2), block):
        outrow = []
        for j in range(int(scale/2), image.shape[1] - int(scale/2), block):
            block_arr = image[i:i+block,j:j+block]
            center_i = int(i+block/2)
            center_j = int(j+block/2)
            if block%2 != 0 and scale%2 == 0: # make sure the scale window is the correct size for the block
                scale_arr = image[center_i-int(scale/2):center_i+int(scale/2),center_j-int(scale/2):center_j+int(scale/2)]
            else:
                scale_arr = image[center_i-int(scale/2):center_i+int(scale/2)+1,center_j-int(scale/2):center_j+int(scale/2)+1]      
            fd = hog(scale_arr, orientations=8, pixels_per_cell=(scale_arr.shape[0], scale_arr.shape[1]), cells_per_block=(1, 1), multichannel=True, feature_vector=False)
            outrow.append(fd.flatten())
        out_image.append(outrow)
    return np.array(out_image)

def glcm_feature(image_name, block, scale, prop=None, stat=None, full=False):
    """
    Parameters:
    -----------
    image_name: str
    block: int
    scale: int
    prop: str
    stat: str
    
    Returns:
    --------
    out_image: 2D or 3D ndarray (depends on the input)
    """
    ds = gdal.Open(image_name)
    image = ds.ReadAsArray()
    ds = None
    image = np.moveaxis(image, 0, -1)
    image = skimage.img_as_ubyte(rgb2gray(image))
    out_image = []
    
    pi = 3.14159265
    angles = [0., pi/6., pi/4., pi/3., pi/2., (2.*pi)/3., (3.*pi)/4., (5.*pi)/6.]
    # dist = [1, 2, 4, 8, 16, 32, 64, 128]
    dist = [10, 20]
    distances = [n for n in dist if n < scale]
    if full:
        out = greycomatrix(image, distances, angles)
        return out
    
    for i in range(int(scale/2), image.shape[0] - int(scale/2), block):
        outrow = []
        for j in range(int(scale/2), image.shape[1] - int(scale/2), block):
            block_arr = image[i:i+block,j:j+block]
            center_i = int(i+block/2)
            center_j = int(j+block/2)
            if block%2 != 0 and scale%2 == 0: # make sure the scale window is the correct size for the block
                scale_arr = image[center_i-int(scale/2):center_i+int(scale/2),center_j-int(scale/2):center_j+int(scale/2)]
            else:
                scale_arr = image[center_i-int(scale/2):center_i+int(scale/2)+1,center_j-int(scale/2):center_j+int(scale/2)+1]      
            
            out = greycomatrix(scale_arr, distances, angles)
            
            if prop:
                out = greycoprops(out, prop) # results 2d array [d, a] is the property for th d'th distance and a'th angle
                if stat:
                    out = calc_stat(out, stat, None)
            else:
                if stat:
                    out = calc_stat(out, stat, None)
                else:
                    return out
            outrow.append(out)
        out_image.append(outrow)
    return np.array(out_image)
    
def pantex_feature(image_name, block, scale):
    return glcm_feature(image_name, block, scale, prop="contrast", stat="min")

def textons_feature(image_name, block, scale):
    return NotImplemented

def line_support_regions_feature(image_name, block, scale):
    kernelx = np.array([[-1, 1],
                        [-1, 1]])
    kernely = np.array([[-1, -1],
                        [1, 1]])
    

def calc_stat(arr, stat_name, axis=None):
    """
    Parameters:
    -----------
    arr: ndarray
        the input array
    stat_name: str
        the name of the statistics.
        "max", "min", "mean", "var", "std"
    axis: int, optional
        the axis over which the statistics is calculated
        
    Returns:
    --------
    out: ndarray
    """
    if stat_name == "min":
        out = np.amin(arr, axis)
    if stat_name == "max":
        out = np.amax(arr, axis)
    if stat_name == "var":
        out = np.var(arr, axis)
    if stat_name == "mean":
        out = np.mean(arr, axis)
    if stat_name == "std":
        out = np.std(arr, axis)
    return out