import numpy as np
from osgeo import gdal
from osgeo import osr

from ..utilities.io import write_geotiff

def hist_feature(image_name, block, scale, output=None):
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
    
    bins = [n for n in range(33)] # bins for numpy histogram.
    
    out_image = []
    for i in range(0, image.shape[0], block):
        outrow = []
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
                    out = np.histogram(scale_arr, bins) # could do interesting things with density=True
                    outrow.append(out[0])
            out_image.append(outrow)
    out_image = np.array(out_image)
    out_image = np.moveaxis(out_image, -1, 0)
    if output:
        out_geotran = (out_ulx, out_cell_width, 0, out_uly, 0, out_cell_height)
        write_geotiff(output, out_image, out_geotran, out_srs_wkt)
    else:
        return np.array(out_image)