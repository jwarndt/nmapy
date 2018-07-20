import time

from skimage.feature import hog
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