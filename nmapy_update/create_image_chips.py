import random
import os
import argparse
import time

import numpy as np
from osgeo import ogr
from osgeo import osr
from osgeo import gdal

def __parse_args():
    parser = argparse.ArgumentParser(description="""Script for generating square image chips that fall within
                                                    the boundaries of human generated training polygons. 
                                                    """)

    parser.add_argument('-inshp',
                        '--input_shapefile',
                        dest='training_shapefile',
                        required=True,
                        type=str)
    parser.add_argument('-imdir',
                        '--image_directory',
                        dest='image_dir',
                        required=True,
                        type=str)
    parser.add_argument('-o',
                        '--output_directory',
                        dest='out_dir',
                        required=True,
                        type=str)
    parser.add_argument('-cpf',
                        '--chips_per_feature',
                        dest='chips_per_feature',
                        default=1,
                        type=int)
    parser.add_argument('-d',
                        '--box_dimension',
                        dest='box_dim',
                        default=256,
                        type=int)
    parser.add_argument('-t',
                        '--trials',
                        dest='num_trials',
                        default=20,
                        type=int)
    parser.add_argument('-v',
                        '--verbose',
                        dest='verbose',
                        action='store_true',
                        default=True)
    args = parser.parse_args()

    if args.verbose:
        print("---------------- Input ----------------")
        print('input shapefile:\t' + args.training_shapefile)
        print('image directory:\t' + args.image_dir)
        print('output directory:\t' + args.out_dir)
        print('chips per feature:\t' + str(args.chips_per_feature))
        print('box dimension (pixels):\t' + str(args.box_dim))
        print('number of trials:\t' + str(args.num_trials))
        print("---------------------------------------")
        print()

    return args

def __check_args(args):
    return NotImplemented

def __create_random_box(training_geometry, geotransform, box_dim, num_trials):
    """
    creates a random dim x dim rectangular polygon within the given
    training geometry.
    
    Parameters:
    ------------
    training_geometry: ogr.geometry
        input geometry that the box will be created inside
    geotransform: gdal Dataset Geotransform
    box_dim: int
        the dimension in number of pixels. i.e. size of the chip (xdim, ydim)
        (default are set in the main() function)
    num_trials: int
        the number of times to try and find a random box that fits within the given
        training_geometry
        (defaults are set in the main() function)
    
    Returns:
    ---------
    box_info: list
        box_info[0] is a list that contains the origin coordinates of the random box. (upper left x, upper left y)
        box_info[1] is the box_dim
    """
    mbr = training_geometry.GetEnvelope()
    minx = mbr[0]
    maxx = mbr[1]
    miny = mbr[2]
    maxy = mbr[3]
    
    cell_width = geotransform[1]
    cell_height = geotransform[5]
    
    trial_num = 0
    while trial_num < num_trials: 
        rand_lx = random.uniform(minx, maxx) # left x
        rand_uy = random.uniform(miny, maxy) # upper y
        rx = rand_lx + (box_dim * cell_width) # right x
        ly = rand_uy + (box_dim * cell_height) # lower y (remember that cell height is negative)
        wkt_box = "POLYGON ((%f %f, %f %f, %f %f, %f %f, %f %f))" % (rand_lx, rand_uy, rand_lx, ly, rx, ly, rx, rand_uy, rand_lx, rand_uy)
        training_box_geom = ogr.CreateGeometryFromWkt(wkt_box)
        if training_geometry.Contains(training_box_geom):
            box_info = [[rand_lx, rand_uy], box_dim]
            return box_info
        trial_num += 1
    return None

def __extract_chip_and_write(im, out_dir, box_geom, city_fid_class_string):
    """
    extracts a chip from the image given the box_geom that was found by the
    create_random_box() function.
    
    Parameters:
    ------------
    im: np.ndarray
        the image array
    out_dir: string
        output directory for the image chips
    box_geom: list
        box_info[0] is a list that contains the origin coordinates of the random box. (upper left x, upper left y)
        box_info[1] is the box_dim
    city_fid_class_string: string
        the name of the image chip. fid, class, and city are derived
        from the shapefile feature's attributes
        
    Returns:
    ---------
    None
    """
    outname = os.path.join(out_dir, city_fid_class_string + ".tif")
    
    # read band to get the data type
    b1 = im.GetRasterBand(1)
    im_datatype = b1.DataType
    b1 = None
    
    geotran = im.GetGeoTransform()
    ulx = geotran[0]
    uly = geotran[3]
    cell_width = geotran[1]
    cell_height = geotran[5]
    box_x = box_geom[0][0]
    box_y = box_geom[0][1]
    box_dim = box_geom[1]
    # get the origin coordinates of the box in image space
    # convert from geo coordinates to image coordinates
    pixel_coord_x = int((box_x - ulx) / cell_width)
    pixel_coord_y = int((box_y - uly) / cell_height)
    
    data = im.ReadAsArray(pixel_coord_x, pixel_coord_y, box_dim, box_dim)
    
    cols = data.shape[2]
    rows = data.shape[1]
    bands = data.shape[0]
    
    driver = gdal.GetDriverByName('GTiff')
    out_im = driver.Create(outname, cols, rows, bands, im_datatype)
    out_im.SetGeoTransform((box_x, cell_width, 0, box_y, 0, cell_height))
    for n in range(bands):
        outband = out_im.GetRasterBand(n+1)
        outband.WriteArray(data[n])
        out_im_srs = osr.SpatialReference()
        # FIXME: get the srs from the input image rather than just set it
        # to WGS84
        out_im_srs.ImportFromEPSG(4326)
        out_im.SetProjection(out_im_srs.ExportToWkt())
        outband.FlushCache()  

def create_training_chips(training_shapefile, image_dir, out_dir, chips_per_feature=1, box_dim=256, num_trials=20):
    """
    creates square training image chips given a shapefile of polygons. 
    The polygons in the shapefile identify training classes. 
    The shapefile must have the following fields: FID, class_type, city, image_name. 
    The image_dir must contain the images that are identified in the image_name field 
    for each feature in the shapefile.
    
    Parameters:
    ------------
    training_shapefile: string
        file path to the shapefile that training chips will be made for
    image_dir: string
        the path to the directory that holds the images that training chips
        will be extracted from
    out_dir: string
        the path to the directory that the image chips will be saved to
    box_dim: int
        the x and y dimension in number of pixels for the training chips
    chips_per_feature: int
        the maximum number of image chips possible for each feature in the shapefile
    num_trials: int
        the number of attempts a random box will be created for each feature until
        moving onto the next. A random box must be Within() the training feature in
        order for it to be valid.
        
    Returns:
    ---------
    None
    """
    driver = ogr.GetDriverByName('ESRI Shapefile')
    dataset = driver.Open(training_shapefile, 0) # 0 means read-only. 1 means writeable.
    
    layer = dataset.GetLayer()
    for feature in layer:
        class_type = feature.GetField("class_type")
        fid = str(feature.GetFID())
        city = feature.GetField("city")
        im_name = feature.GetField("image_name")
        geom = feature.GetGeometryRef()
        image = gdal.Open(os.path.join(image_dir, im_name))
        geotran = image.GetGeoTransform()
        count = 0
        while count < chips_per_feature:
            city_fid_class_string = city + "_" + fid + "_" + str(count) + "_" + class_type
            training_box_geom = __create_random_box(geom, geotran, box_dim, num_trials)
            if training_box_geom is None: 
                print("INFO: NO BOX GEOM FOUND --> FID: " + fid + ", Chip Number: " + str(count))
            else:
                __extract_chip_and_write(image, out_dir, training_box_geom, city_fid_class_string)
            count += 1

def main():
    start_time = time.time()
    print('\nStart date & time --- (%s)\n' % time.asctime(time.localtime(time.time())))

    args = __parse_args()
    __check_args(args)
    create_training_chips(args.training_shapefile,
                          args.image_dir,
                          args.out_dir,
                          args.chips_per_feature,
                          args.box_dim,
                          args.num_trials)

    tot_sec = time.time() - start_time
    minutes = int(tot_sec // 60)
    sec = tot_sec % 60
    print('\nEnd data & time -- (%s)\nTotal processing time -- (%d min %f sec)\n' %
        (time.asctime(time.localtime(time.time())), minutes, sec))


if __name__ == "__main__":
    main()