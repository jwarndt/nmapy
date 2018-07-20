import numpy as np
import gdal

from . import utilities

def get_se_set(sizes):
    """
    Parameters:
    -----------
    sizes: list
    
    Returns:
    --------
    se_set: ndarray (4D)
        se_set[0] gives the linear directional kernels for size
            at index zero
        se_set[1] gives the linear direction kernels for size at
            index 1
    """
    se_set = []
    for se_size in sizes:
        assert(se_size%2!=0)
        # create a structural element for the direction and size
        # directions are hardcoded to 4 for now. it generates 4
        # kernels with directions of 0, 45, 90, and 135
        se0 = np.zeros(shape=(se_size,se_size))
        se0[se_size//2,:] = 1
        se45 = np.diagflat(np.ones(shape=(se_size)))[::-1]
        se90 = np.zeros(shape=(se_size,se_size))
        se90[:,se_size//2] = 1
        se135 = np.diagflat(np.ones(shape=(se_size)))
        se_set.append([se0, se45, se90, se135])
    return se_set

def MBI_feature(image_name, postprocess=True):
    ds = gdal.Open(image_name)
    image = ds.ReadAsArray()
    ds = None
    image = np.moveaxis(image, 0, -1) # rows, columns, channels
    # calculate brightness as a local max
    brightness = calc_stat(image, "max", 2)
    # a set of linear structural elements
    # for the white tophat transformation
    # dirs = [45, 90, 135, 180]
    se_sizes = [5, 9, 13, 19, 23, 27]
    se_set = get_se_set(se_sizes)
    # 'white' top-hat transformation
    # in this case, white top-hat is the brightness image minus morphological opening
    mean_w_tophats = []
    for s in se_set: # for each size in the structural element set
        w_tophats = []
        for k in s: # for each direction kernel in the structural element set for this size
            # directional top hat transformation using linear SE
            w_tophats.append(white_tophat(brightness, k))
        mean_w_tophat = utilities.calc_stat(w_tophats, 'mean', 0)
        mean_w_tophats.append(mean_w_tophat)
    
    th_dmp = []
    th_idx = 0
    while th_idx + 1 < len(mean_w_tophats):
        th_dmp.append(np.absolute(mean_w_tophats[th_idx + 1] - mean_w_tophats[th_idx]))
        th_idx+=1
    mbi = utilities.calc_stat(np.array(th_dmp), 'mean', 0)
    if postprocess:
        mbi = np.where(mbi >= 50, 1, 0)
    return mbi, np.array(th_dmp), np.array(mean_w_tophats) 