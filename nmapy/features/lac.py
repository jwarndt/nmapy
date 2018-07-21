import math

def lacunarity_feature_binary(arr, box_size, window_size, slide_style=0):
    return NotImplemented

def lacunarity_feature_grayscale(arr, box_size, window_size, slide_style=0):
    """
    differential box-counting algorithm

    Parameters:
    -----------
    arr: ndarray 2D
        the input array
    box_size: int
        the size of the cube (r x r x r)
    window_size: 
        the size of the window (w x w)
    slide_style: int
        how the boxes slide across the window
        glide: specify a slide_style of 0
        block: specify a slide_style of -1
        skip: specify the number of pixels to skip (i.e. a positive integer)

    Returns:
    --------
    out: ndarray
        the lacunarity image
    """
    assert(box_size < window_size)

    # move the window over the image
    i = 0
    while i < len(arr) - window_size + 1:
        j = 0
        while j < len(arr[0]) - window_size + 1:
            window = arr[i:window_size, j:window_size]
            # now slide the box over the window
            n_mr = {} # the number of gliding boxes of size r and mass m. a histogram
            # m = 0 # the mass of the grayscale image, the sum of the relative height of columns (n_ij)
            # masses = []
            total_boxes_in_window = 0
            ii = 0
            while ii < len(window):
                jj = 0
                while jj < len(window[0]):
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
            