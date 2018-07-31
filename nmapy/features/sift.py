import os
import random

import numpy as np
from sklearn.cluster import KMeans
import skimage
from skimage.color import rgb2gray
from osgeo import gdal
from osgeo import osr
import cv2

"""
Sift extraction on 

def make_sift_codebook()
    write_sift_keypoint_desc
    get_keypoint_sample
    kmeans_sift_feat_vec
"""

def __image_coord_to_geo_coord(keypoints, geotran):
    x_coor = geotran[0] + keypoints[0] * geotran[1]
    y_coor = geotran[3] + keypoints[1] * geotran[5]
    return (x_coor, y_coor)

def write_sift_keypoint_desc(image_name, outdir):
    ds = gdal.Open(image_name)
    image = ds.ReadAsArray()
    geotran = ds.GetGeoTransform()
    ulx = geotran[0]
    uly = geotran[3]
    cell_width = geotran[1]
    cell_height = geotran[5]

    ds = None
    image = np.moveaxis(image, 0, -1)
    image = skimage.img_as_ubyte(rgb2gray(image))
    
    # find keypoints and compute descriptions
    sift = cv2.xfeatures2d.SIFT_create()
    kp, des = sift.detectAndCompute(image, None)
    kp_image_coords = [kp[n].pt for n in range(len(kp))]
    kp_geo_coords = np.apply_along_axis(__image_coord_to_geo_coord, 1, kp_image_coords, geotran)
    sift_des = np.concatenate((kp_geo_coords, des), axis=1)

    out_dat_file = os.path.join(outdir, os.path.basename(image_name)[:-4] + ".siftdat")
    sift_des.tofile(out_dat_file)

def get_rand_sift_feats(siftdat_dir, sample_num=100000):
    keypoints = []
    siftdat_files = [n for n in os.listdir(siftdat_dir) if n[-8:] == ".siftdat"]
    while len(keypoints) < sample_num:
        siftdat = np.fromfile(siftdat_files[random.randint(0, len(siftdat_files))]) # retrieve and open a random file
        keypoints.append(siftdat[random.randint(0, len(siftdat))][2:]) # read a random sift feature from the array and append only its description to keypoints
    return keypoints

def create_sift_codebook(image_dir, out_dir, n_clusters=32, rand_samp_num=100000):
    """
    Returns:
    --------
    codebook: sklearn kmeans class
        The cluster centers obtained by running kmeans on randomly
        sampled sift keypoint descriptions.
        Each cluster center is a vector of 128 features
    """
    image_names = [n for n in os.listdir(image_dir) if n[-4:] == ".tif"]
    out_codebook_file = os.path.join(outdir, 'sift_kmeans_codebook' + ".dat")
    for n in image_names:
        write_sift_keypoint_desc(n, out_dir)
    sift_feats = get_rand_sift_feats(out_dir, rand_samp_num)
    codebook = KMeans(n_clusters=n_clusters, random_state=42).fit(sift_feats)
    codebook.cluster_centers_.tofile(out_codebook_file)
    return codebook

def assign_codeword(siftdat_dir, codebook_file):
    siftdat_files = [n for n in os.listdir(siftdat_dir) if n[-8:] == ".siftdat"]
    codebook = np.fromfile(codebook_file) # get the cluster centers from kmeans. (an ndarray)
    for n in siftdat_files:
        siftdat = np.fromfile(n)
        coords = siftdat[:,:2]
        feats = siftdat[:,2:]



def sift_feature(image_name, block, scale, )

    image = 
    kmeans = KMeans(n_clusters=32, random_state=42).fit(X)
