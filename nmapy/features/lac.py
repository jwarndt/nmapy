import math

from ..utilities.stats import *
from .global_vars import *

def lacunarity_feature_grayscale(image_name, block, scale, box_size, slide_style=0, lac_type='grayscale'):
    """
    differential box-counting algorithm for computing lacunarity

    Parameters:
    -----------
    image_name: str
        the input image
    block: int
        the size of the block in pixels
    scale: int
        the window size in pixels for computing lacunarity (w x w). window and scale are synonomous
    box_size: int
        the size of the cube (r x r x r)
    slide_style: int
        how the boxes slide across the window
        for glide: specify a slide_style of 0
        for block: specify a slide_style of -1
        for skip: specify the number of pixels to skip (i.e. a positive integer)
    lac_type: str
        two options are available: grayscale or binary
        lacunarity calculations are slightly different for these

    Returns:
    --------
    out: ndarray
        the lacunarity image
    """
    assert(box_size < scale)

    ds = gdal.Open(image_name)
    image = ds.ReadAsArray()
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

    # move the window (scale) over the image block by block
    for i in range(0, image.shape, block):
        if i >= MAX_SCALE and i <= image.shape[0] - MAX_SCALE:
            for j in range(0, image.shape[1], block):
                if j >= MAX_SCALE and j <= image.shape[1] - MAX_SCALE:
                    block_arr = image[i:i+block,j:j+block]
                    center_i = int(i+block/2)
                    center_j = int(j+block/2)
                    # catch the origin coordinates for writing the output
                    if len(out_image) == 0 and len(outrow) == 0:
                        out_uly = uly + cell_height * (center_i - block)
                        out_ulx = ulx + cell_width * (center_j - block)
                    if block%2 != 0 and scale%2 == 0: # make sure the scale window is the correct size for the block
                        scale_arr = image[center_i-int(scale/2):center_i+int(scale/2),center_j-int(scale/2):center_j+int(scale/2)]
                    else:
                        scale_arr = image[center_i-int(scale/2):center_i+int(scale/2)+1,center_j-int(scale/2):center_j+int(scale/2)+1]
                    
                    window = image[i:window_size, j:window_size]
                    # now slide the box over the window
                    n_mr = {} # the number of gliding boxes of size r and mass m. a histogram
                    # m = 0 # the mass of the grayscale image, the sum of the relative height of columns (n_ij)
                    # masses = []
                    total_boxes_in_window = 0
                    ii = 0
                    while ii < len(scale):
                        jj = 0
                        while jj < len(scale[0]):
                            total_boxes_in_window += 1
                            box = window[ii:box_size,jj:box_size]
                            max_val = max(box)
                            min_val = min(box)
                            u = math.ceil(min_val / box_size) # box with minimum pixel value
                            v = math.ceil(max_val / box_size) # box with maximum pixel value
                            n_ij = v - u + 1 # relative height of column at ii and jj
                            
                            # masses.append(n_ij)
                            # m += n_ij

                            # so n_mr is the number of boxes of size r and mass m
                            # use a dictionary and count the number of boxes in this image
                            if n_ij not in n_mr:
                                n_mr[n_ij] = 1
                            else:
                                n_mr[n_ij] += 1
                            # move the box based on the glide_style
                            if glide_style == 0: # glide
                                jj+=1
                            elif glide_stype == -1: # block
                                jj+=box_size
                            else: # skip
                                jj+=box_size+glide_style
                if glide_style == 0: # glide
                    ii+=1
                elif glide_stype == -1: # block
                    ii+=box_size
                else: # skip
                    ii+=box_size+glide_style
            num = 0
            denom = 0
            for masses in n_mr:
                # the probability function which is the number of boxes
                # of size r and mass m divided by the total number of boxes
                q_mr = n_mr[masses] / total_boxes_in_window 
                num += (masses*masses) * q_mr
                denom += masses * q_mr
            denom = denom**2
            lac = num / denom
            j+=1
        i+=1