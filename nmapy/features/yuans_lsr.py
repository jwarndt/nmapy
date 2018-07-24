import math

import cv2
import gdal
import numpy as np

from . import _region_grow

def burns_lsr_feature(image_name, block, scale, mag):
    im = cv2.imread(image_name)
    # convert image to grayscale
    im = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)

    # calculate gradient orientation and magnitude
    mag, ang, dx, dy = __calc_mag_ang(image)
    mag_threshold = mag
    lsr_threshold = 20 # threshold for smallest line support region

    temp = mag + 180
    temp = np.where(temp < mag_threshold, -1, temp)
    lsr_m = region_grow.main(temp, 8, 30)


def yuans_lsr_feature(image_name, block, scale, mag):
    """
    Parameters:
    -----------
    image_name: str
    mag: int
        is 20 in the original matlab code
    
    Returns:
    
    
    """
    im = cv2.imread(image_name)
    # convert image to grayscale
    im = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)

    # calculate gradient orientation and magnitude
    im_mag, im_ang, dx, dy = __calc_mag_ang(im)
    mag_threshold = mag
    lsr_threshold = 20 # threshold for smallest line support region
    
    temp = im_ang #+ 180
    # tmp(edmim<magThreshold)=-1;
    # set every value in the edge orientation image to -1 if the edge magnitude is
    # less than the threshold.
    temp = np.where(im_mag < mag_threshold, -1, temp) 

    lsr_m = main(temp, 8, 30)
    
    # line_idx=unique(lsrM);
    line_idx = np.unique(lsr_m)
    
    # lsfarr = zeros(max(lsrM(:)),5);
    lsf_arr = np.zeros(np.max(lsr_m[:]), 5)
    
    count = 0

    l = 1
    for l in range(1, np.max(line_idx)):
        # idx=find(lsrM==l);
        idx = np.argwhere(lsr_m.ravel() == l) # returns an array of indices

        # eim = zeros(size(im));
        eim = np.zeros(shape=im.shape)

        # eim(idx) = 1;
        eim = np.where(lsr_m == l, 1, eim)

        # if (sum(eim(:)) <= lsrThreshold)
        if np.sum(eim) <= lsr_threshold: # ignore small line support region
            continue

        # ix_wi = dx(idx)
        # iy_wi = dy(idx)
        Ix_wi = dx.ravel()[idx] # extract elements in dx at index locations where lsr_m == l
        Iy_wi = dy.ravel()[idx]
        grd_wi = im_mag.ravel()[idx]
        
        # find major orientation
        ST = [[np.sum(Ix_wi**2), np.sum(Ix_wi*Iy_wi)],
              [np.sum(Ix_wi*Iy_wi), np.sum(Iy_wi**2)]]
        
        # V, D = eig(ST)
        # matlab returns returns diagonal matrix D of eigenvalues and matrix V whose columns are the corresponding right eigenvectors, so that A*V = V*D.
        D, V = np.linalg.eig(ST) # python's return of D is a 1D array, 
        D = np.diag(D) # make D on the diagonal to conform to matlab's procedure

        # if D(1,1)<D(2,2)
        #     lorn=atan(V(2,1)/V(1,1));
        # else
        #     lorn=atan(V(2,2)/V(1,2));
        # end 
        if D[0][0] < D[1][1]:
            # lorn=atan(V(2,1)/V(1,1));
            lorn = np.arctan(V[1][0]/V[0][0])
        else:
            # lorn=atan(V(2,2)/V(1,2));
            lorn = np.arctan(V[1][1]/V[0][1])

        # vote for r
        # [Ytmp,Xtmp]=ind2sub(size(im),idx);
        Ytmp, Xtmp = np.unravel_index(idx, im.shape)
        Ytmp+=1 # indices need += 1 for some indexing weirdness...
        Xtmp+=1
        # Raccm=round(Xtmp.*cos(lorn-pi/2)+Ytmp.*sin(lorn-pi/2));
        Raccm=np.round(Xtmp*math.cos(lorn-(math.pi/2))+Ytmp*math.sin(lorn-(math.pi/2)))
        rng=np.arange(Raccm.min(),Raccm.max()+1)
        accm=np.zeros(shape=(len(rng)))
        for k in range(len(idx)):
            rc = np.round(Xtmp[k]*math.cos(lorn-math.pi/2)+Ytmp[k]*math.sin(lorn-math.pi/2))
            accm[np.where(rng==rc)] = accm[np.where(rng==rc)] + grd_wi[k]

        mxid = np.argmax(accm)
        Xmx=max(Xtmp[np.where(Raccm==rng[mxid])])
        Xmn=min(Xtmp[np.where(Raccm==rng[mxid])])
        Ymx=max(Ytmp[np.where(Raccm==rng[mxid])])
        Ymn=min(Ytmp[np.where(Raccm==rng[mxid])])

        lmx = (Xmx+Xmn)/2
        lmy = (Ymx+Ymn)/2
        llen = math.sqrt((Xmx-Xmn)**2+(Ymx-Ymn)**2)
        lsfarr[count,0] = llen
        lsfarr[count,1] = lmx
        lsfarr[count,2] = lmy
        lsfarr[count,3] = lorn
        lcon=np.mean(grd_wi[(np.where(Raccm==rng[mxid]))])
        lsfarr[count,4] = lcon
        count+=1
        lsfarr = lsfarr[0:count,:]
    return lsfarr

def __calc_mag_ang_sobel(im):
    dx = cv2.Sobel(np.float32(im), cv2.CV_32F, 1, 0, ksize=7)
    dy = cv2.Sobel(np.float32(im), cv2.CV_32F, 0, 1, ksize=7)
    mag, ang = cv2.cartToPolar(dx, dy, angleInDegrees=1)
    return mag, ang, dx, dy

def __calc_mag_ang(im):
    # these kernels were obtained from the output of the matlab functions
    # they are the same kernels used in the original paper/code. The filtering 
    # in opencv might be implemented differently than the filtering in Matlab and so
    # results might be slightly different
    
    # f1=fspecial('gaussian',[7,7],1.2);
    # guassian_kernel = np.array([[0.0002, 0.0012, 0.0035, 0.0049, 0.0035, 0.0012, 0.0002],
    #                             [0.0012, 0.0069, 0.0196, 0.0277, 0.0196, 0.0069, 0.0012],
    #                             [0.0035, 0.0196, 0.0555, 0.0785, 0.0555, 0.0196, 0.0035],
    #                             [0.0049, 0.0277, 0.0785, 0.1111, 0.0785, 0.0277, 0.0049],
    #                             [0.0035, 0.0196, 0.0555, 0.0785, 0.0555, 0.0196, 0.0035],
    #                             [0.0012, 0.0069, 0.0196, 0.0277, 0.0196, 0.0069, 0.0012],
    #                             [0.0002, 0.0012, 0.0035, 0.0049, 0.0035, 0.0012, 0.0002]])
    # # hy = fspecial('prewitt');
    # prewitt_y = np.array([[1, 1, 1],
    #                       [0, 0, 0],
    #                       [-1, -1, -1]])

    # output of filtering the gaussian with a prewitt_y
    # hy1 = cv2.filter2d(f1, hy)
    hy1 = np.array([[-0.0081,-0.0277,-0.0542,-0.0669,-0.0542,-0.0277,-0.0081],
                    [-0.0216,-0.0736,-0.1440,-0.1777,-0.1440,-0.0736,-0.0216],
                    [-0.0245,-0.0834,-0.1632,-0.2013,-0.1632,-0.0834,-0.0245],
                    [0,0,0,0,0,0,0],
                    [ 0.0245,0.0834,0.1632,0.2013,0.1632,0.0834,0.0245],
                    [0.0216,0.0736,0.1440,0.1777,0.1440,0.0736,0.0216],
                    [0.0081,0.0277,0.0542,0.0669,0.0542,0.0277,0.0081]])
    # hx = hy1'
    hx = hy1.transpose()

    # dy = imfilter(im, hy1, 'replicate');
    # dx = imfilter(im, hx, 'replicate');
    dy = cv2.filter2D(np.float32(im), -1, hy1)
    dx = cv2.filter2D(np.float32(im), -1, hx)

    # eo = rad2deg(atan2(dy,(dx+1e-5)));
    # em = sqrt(dx.^2+dy.^2);
    # mag, ang = cv2.cartToPolar(dx, dy, angleInDegrees=1)

    # eo = rad2deg(atan2(dy,(dx+1e-5)));
    ang = np.rad2deg(np.arctan2(dy,(dx+1e-5)))
    ang+=180
    # em = sqrt(dx.^2+dy.^2);
    mag = np.sqrt(dx**2 + dy**2)
    return mag, ang, dx, dy
