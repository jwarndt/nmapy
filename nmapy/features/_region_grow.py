import math

import numpy as np

def quicksort(x, xi, xj, first, last):
    if first < last:
        pivot = first
        i = first
        j = last

        while i < j:
            while x[i] <= x[pivot] and i < last:
                i+=1
            while x[j] > x[pivot]:
                j-=1
            if i < j:
                temp = x[i]
                x[i] = x[j]
                x[j] = temp
                
                temp = xi[i]
                xi[i] = xi[j]
                xi[j] = temp
                
                temp = xj[i]
                xj[i] = xj[j]
                xj[j] = temp

        temp = x[pivot]
        x[pivot] = x[j]
        x[j] = temp

        temp = xi[pivot]
        xi[pivot] = xi[j]
        xi[j] = temp

        temp = xj[pivot]
        xj[pivot] = xj[j]
        xj[j] = temp

        quicksort(x, xi, xj, first, j-1)
        quicksort(x, xi, xj, j+1, last)


def expand(image, seg_res, out_m, tgt, tb, bb, lb, rb, ot, label_n, i, j):
    rows = image.shape[0]
    cols = image.shape[1]

    # c1 = abs(image[i + j * rows] - tgt)
    c1 = abs(image[i][j] - tgt)
    c2 = 360 - c1
    if c1 < c2:
        c = c1
    else:
        c = c2
    
    # if c > ot or image[i + j * rows] < 0 or seg_res[i + j * rows] > 0:
    if c > ot or image[i][j] < 0 or seg_res[i][j] > 0:
        return
    
    # seg_res[i + j * rows] = label_n
    seg_res[i][j] = label_n
    # out_m[i + j * rows] = 0
    out_m[i][j] = 0
    if i < tb:
        tb = i
    if i > bb:
        bb = i
    if j < lb:
        lb = j
    if j > rb:
        rb = j
    
    if i + 1 < rows:
        expand(image, seg_res, out_m, tgt, tb, bb, lb, rb, ot, label_n, i + 1, j)
    if j + 1 < rows:
        expand(image, seg_res, out_m, tgt, tb, bb, lb, rb, ot, label_n, i, j + 1)
    if i - 1 >= 0:
        expand(image, seg_res, out_m, tgt, tb, bb, lb, rb, ot, label_n, i - 1, j)
    if j - 1 >= 0:
        expand(image, seg_res, out_m, tgt, tb, bb, lb, rb, ot, label_n, i, j - 1)
    return image, seg_res, out_m, tgt, tb, bb, lb, rb, ot, label_n, i, j

def main(image, disThr, ortThr):
    # image is the edge orientation map
    rows = image.shape[0]
    cols = image.shape[1]

    dt = disThr
    ot = ortThr

    seg_res = np.zeros(shape=(rows, cols), dtype=float)

    out_m = np.ones(shape=(rows, cols), dtype=float)
    out_l = np.ones(shape=(rows * cols), dtype=int)
    out_li = np.ones(shape=(rows * cols), dtype=int)
    out_lj = np.ones(shape=(rows * cols), dtype=int)

    ws = dt * 2
    count = 0

    ii = 0
    while ii < rows:
        print("on row: " + str(ii))
        jj = 0
        while jj < cols:
            """
            if this value is above the magnitude threshold, then set
            tgti index (threshold greater than i) to ii, and set 
            tgtj index (threshold greater than k) to jj
            """
            # if image[ii + jj * rows] >= 0:
            if image[ii][jj] >= 0:
                tgti = ii
                tgtj = jj
                # top, left, bottom, right boundary?
                if tgti - ws > 0: # avoid indexing out of bounds of the top of the array
                    tb = tgti - ws
                else:
                    tb = 0

                if tgti + ws < rows - 1: # avoid indexing out of bounds of the bottom of the array
                    bb = tgti + ws
                else:
                    bb = rows - 1

                if tgtj - ws > 0: # avoid indexing out of bounds to the left of the array
                    lb = tgtj - ws
                else:
                    lb = 0

                if tgtj + ws < cols - 1: # avoid indexing out of bounds to the right of the array
                    rb = tgtj + ws
                else:
                    rb = cols - 1

                dstV = 0
                i = tb
                """
                Now iterate through a kernel which is a subset of the entire image
                the kernel is centered at pixel (ii, jj) and the kernel size when not
                near the boundary of the image is (32, 32). This size is defined by the 
                distance threshold (8) multiplied by 2 (ws = dt * 2).
                At each pixel in the kernel, measure its distance from the center,
                if this distance is less than the threshold, and the value of the pixel
                is greater than the magnitude threshold, 
                """
                while i <= bb:
                    j = lb
                    while j <= rb:
                        # the distance from the center of the kernel to pixel (i, j) in the kernel
                        d = math.sqrt((tgti-i)*(tgti-i)+(tgtj-j)*(tgtj-j)) 
                        # if d <= dt and image[i+j*rows] >= 0 and (i != tgti or j != tgtj):
                        if d <= dt and image[i][j] >= 0 and (i != tgti or j != tgtj):
                            # c1 = abs(image[tgti+tgtj*rows] - image[i+j*rows])
                            c1 = abs(image[tgti][tgtj] - image[i][j])
                            c2 = 360 - c1
                            if c1 < c2:
                                c = c1
                            else:
                                c = c2
                            if c < ot:
                                dstV += 1
                        j+=1
                    i+=1
                # out_m[ii+jj*rows] = dstV
                out_m[ii][jj] = dstV
                out_l[count] = dstV
                out_li[count] = ii
                out_lj[count] = jj
                count += 1
            jj+=1
        ii+=1
    
    # recursion depth issues with Python, using regular sort() for now...
    # quicksort(out_l, out_li, out_lj, 0, count - 1)
    out_l.sort()
    out_li.sort()
    out_lj.sort()

    label_n = 0
    k = count - 1
    while k >= 0:
        # if seg_res[out_li[k] + out_lj[k] * rows] == 0:
        if seg_res[out_li[k]][out_lj[k]] == 0:
            tgti = out_li[k]
            tgtj = out_lj[k]

            # if out_m[tgti + tgtj * rows] == 0:
            if out_m[tgti][tgtj] == 0:
                continue
            
            # tgt = image[tgti + tgtj * rows]
            tgt = image[tgti][tgtj]
            # out_m[tgti + tgtj * rows] = 0
            out_m[tgti][tgtj] = 0
            label_n+=1
            tb = tgti
            bb = tgti
            lb = tgtj
            rb = tgtj
            image, seg_res, out_m, tgt, tb, bb, lb, rb, ot, label_n, tgti, tgtj = expand(image, seg_res, out_m, tgt, tb, bb, lb, rb, ot, label_n, tgti, tgtj)
    return seg_res
