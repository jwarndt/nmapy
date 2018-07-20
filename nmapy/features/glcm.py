import skimage
from skimage.feature import greycomatrix, greycoprops
from skimage.color import rgb2gray
import numpy as np
from osgeo import gdal
from osgeo import osr

from ..utilities.stats import *

MAX_SCALE = 150

def glcm_feature(image_name, block, scale, output=None, prop=None, stat=None):
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
    # FIXME: need a better fix for this.
    if len(image) >= 3:
        image = image[:3]
    geotran = ds.GetGeoTransform()
    ulx = geotran[0]
    uly = geotran[3]
    cell_width = geotran[1]
    cell_height = geotran[5]
    
    out_srs = osr.SpatialReference()
    out_srs.ImportFromEPSG(4326)
    out_srs_wkt = out_srs.ExportToWkt()
    out_cell_width = block * cell_width
    out_cell_height = block * cell_height
    
    ds = None
    image = np.moveaxis(image, 0, -1)
    image = skimage.img_as_ubyte(rgb2gray(image))
    
    pi = 3.14159265
    angles = [0., pi/6., pi/4., pi/3., pi/2., (2.*pi)/3., (3.*pi)/4., (5.*pi)/6.]
    # dist = [1, 2, 4, 8, 16, 32, 64, 128]
    dist = [10, 20]
    distances = [n for n in dist if n < scale]
    
    out_image = []
    for i in range(0, image.shape[0], block):
        outrow = []
        if i >= MAX_SCALE and i <= image.shape[0] - MAX_SCALE:
            for j in range(0, image.shape[1], block):
                if j >= MAX_SCALE and j <= image.shape[1] - MAX_SCALE:
                    block_arr = image[i:i+block,j:j+block]
                    center_i = int(i+block/2)
                    center_j = int(j+block/2)
                    if len(out_image) == 0 and len(outrow) == 0:
                        out_uly = uly + cell_height * (center_i - block)
                        out_ulx = ulx + cell_width * (center_j - block)
                    if block%2 != 0 and scale%2 == 0: # make sure the scale window is the correct size for the block
                        scale_arr = image[center_i-int(scale/2):center_i+int(scale/2),center_j-int(scale/2):center_j+int(scale/2)]
                    else:
                        scale_arr = image[center_i-int(scale/2):center_i+int(scale/2)+1,center_j-int(scale/2):center_j+int(scale/2)+1]      

                    out = greycomatrix(scale_arr, distances, angles)
                    if prop:
                        if prop == "variance": # variance is not included in greycoprops, so use a custom implementation
                            print('hi')
                        else:
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
    out_image = np.array(out_image)
    """for i in range(int(scale/2), image.shape[0] - int(scale/2), block):
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
                        out = calc_stat(out, stat, None)
            else:
                if stat:
                    out = calc_stat(out, stat, None)
                else:
                    return out
            outrow.append(out)
        out_image.append(outrow)"""
   
    if output:
        out_geotran = (out_ulx, out_cell_width, 0, out_uly, 0, out_cell_height)
        # this should be a standardized write geotiff function
        write_geotiff(output, out_image, out_geotran, out_srs_wkt)
    else:
        return np.array(out_image)
    
def pantex_feature(image_name, block, scale, output=None):
    if output:
        glcm_feature(image_name, block, scale, output=output, prop="contrast", stat="min")
    else:
        return glcm_feature(image_name, block, scale, prop="contrast", stat="min")