import math

def __dbc(arr, box_size, window_size, slide_style=0):
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
        the lacunarity
    """
    assert(box_size < window_size)

    # move the window over the image
    i = 0
    while i < len(arr) - window_size + 1:
        j = 0
        while j < len(arr[0]) - window_size + 1:
            window = arr[i:window_size, j:window_size]
            # now slide the box over the window
            n_mr = 0 # the number of gliding boxes of size r in the window of size w
            ii = 0
            while ii < len(window):
                jj = 0
                while jj < len(window[0]):
                    n_mr += 1
                    box = window[ii:box_size,jj:box_size]
                    max_val = max(box)
                    min_val = min(box)
                    u = math.ceil(min_val / box_size) # box with minimum pixel value
                    v = math.ceil(max_val / box_size) # box with maximum pixel value
                    n_ij = v - u + 1 # relative height of comumn at i and j
                    m = 
                    q_mr = # the probability function
                    # move the box based on the glide_style
                    if glide_style == -1:
                        

            j+=1

        i+=1
            