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
    image = image[0:5000,0:5000]
    
    # find keypoints and compute descriptions
    sift = cv2.xfeatures2d.SIFT_create()
    kp, des = sift.detectAndCompute(image, None)
    kp_image_coords = [kp[n].pt for n in range(len(kp))]
    kp_geo_coords = np.apply_along_axis(__image_coord_to_geo_coord, 1, kp_image_coords, geotran)
    sift_des = np.concatenate((kp_geo_coords, des), axis=1)

    out_dat_file = os.path.join(outdir, os.path.basename(image_name)[:-4] + ".siftdat")
    sift_des.tofile(out_dat_file)
    return sift_des

def get_rand_sift_feats(siftdat_dir, sample_num=100000):
    keypoints = []
    siftdat_files = [n for n in os.listdir(siftdat_dir) if n[-8:] == ".siftdat"]
    rand_file_idx = [random.randint(0, len(siftdat_files)-1) for n in range(sample_num)]
    rand_file_idx.sort()
    count = 0
    cur_file = None
    while len(keypoints) < sample_num:
        if cur_file != siftdat_files[rand_file_idx[count]]:
            cur_file = siftdat_files[rand_file_idx[count]]
            siftdat = np.fromfile(os.path.join(siftdat_dir, cur_file)) # retrieve and open a random file
            siftdat = siftdat.reshape(-1,130) # reshape into a 2D array of (n_samples, n_features). 128 features plus and x and y coord for a total of 130 features. 
        rand_kp = random.randint(0, len(siftdat)-1)
        keypoints.append(siftdat[rand_kp,2:]) # read a random sift feature from the array and append only its description to keypoints
        count+=1
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
    image_names = [os.path.join(image_dir,n) for n in os.listdir(image_dir) if n[-4:] == ".tif"]
    out_codebook_file = os.path.join(outdir, 'sift_kmeans_codebook' + ".dat")
    for n in image_names:
        write_sift_keypoint_desc(n, out_dir)
    sift_feats = get_rand_sift_feats(out_dir, rand_samp_num)
    codebook = KMeans(n_clusters=n_clusters, random_state=42).fit(sift_feats)
    codebook.cluster_centers_.tofile(out_codebook_file)
    return codebook

def restore_codebook(codebook_filename):
    """
    reads the cluster_centers from the codebook file
    and restores a kmeans model to use for prediction
    """
    cluster_centers = np.fromfile(codebook_filename).reshape(-1,128)
    n_clusters = len(cluster_centers)
    codebook = KMeans(n_clusters=n_clusters, random_state=42)
    codebook.cluster_centers_ = cluster_centers
    return codebook

def assign_codeword(siftdat_dir, codebook_file):
    siftdat_files = [os.path.join(siftdat_dir,n) for n in os.listdir(siftdat_dir) if n[-8:] == ".siftdat"]
    codebook = restore_codebook(codebook_file) # get the cluster centers from kmeans. (an ndarray)
    for n in siftdat_files:
        siftdat = np.fromfile(n).reshape(-1, 130)
        coords = siftdat[:,:2]
        feats = siftdat[:,2:]
        pred = codebook.predict(feats)
        return pred



def sift_feature(image_name, block, scale, )

    image = 
    kmeans = KMeans(n_clusters=32, random_state=42).fit(X)
