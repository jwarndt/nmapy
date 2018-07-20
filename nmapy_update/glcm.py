import skimage
from skimage.feature import greycomatrix, greycoprops
from skimage.color import rgb2gray
import gdal
import numpy as np

from .. import utilities

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
                if prop == "variance": # variance is not included in greycoprops
                    print('hi')
                else:
                    out = greycoprops(out, prop) # results 2d array [d, a] is the property for th d'th distance and a'th angle
                    if stat:
                        out = utilities.calc_stat(out, stat, None)
            else:
                if stat:
                    out = utilities.calc_stat(out, stat, None)
                else:
                    return out
            outrow.append(out)
        out_image.append(outrow)
    return np.array(out_image)

def pantex_feature(image_name, block, scale):
    return glcm_feature(image_name, block, scale, prop="contrast", stat="min")