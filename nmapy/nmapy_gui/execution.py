import time
import os

from ..features.hog import *
from ..features.glcm import *
from ..features.lac import *
from ..features.mbi import *

def execute(execution_parameters):
    start_time = time.time()
    print('\nStart date & time --- (%s)\n' % time.asctime(time.localtime(time.time())))
    print("User Input:")
    print("-----------")
    print("input:\t\t" + execution_parameters["input"])
    print("output:\t\t" + execution_parameters["output"])
    print("feature:\t\t" + execution_parameters["feature"])
    print()
    if execution_parameters["input"][-4] != ".":
        im_list = get_tif_images(execution_parameters["input"])
        print("processing " + str(len(im_list)) + " images")
    else:
        im_list = [execution_parameters["input"]]
        print("processing 1 image")
    if execution_parameters["stat"] == "None":
        execution_parameters["stat"] = None
    if execution_parameters["prop"] == "None":
        execution_parameters["prop"] = None
    execution_parameters["postprocess"] = bool(execution_parameters["postprocess"])
    for input_im in im_list:
        print("processing:\t\t" + input_im)
        if execution_parameters["feature"] == "HOG":
            hog_feature(execution_parameters["input"],
                        execution_parameters["block"],
                        execution_parameters["scale"],
                        output=execution_parameters["output"],
                        stat=execution_parameters["stat"])
        elif execution_parameters["feature"] == "GLCM":
            glcm_feature(execution_parameters["input"],
                        execution_parameters["block"],
                        execution_parameters["scale"],
                        output=execution_parameters["output"],
                        prop=execution_parameters["prop"],
                        stat=execution_parameters["stat"])
        elif execution_parameters["feature"] == "Pantex":
            pantex_feature(execution_parameters["input"],
                           execution_parameters["block"],
                           execution_parameters["scale"],
                           output=execution_parameters["output"])
        elif execution_parameters["feature"] == "Lacunarity":
            lac_feature(execution_parameters["input"],
                               execution_parameters["block"],
                               execution_parameters["scale"],
                               box_size=execution_parameters["box_size"],
                               output=execution_parameters["output"],
                               slide_style=execution_parameters["slide_style"],
                               lac_type=execution_parameters["lac_type"])
        elif execution_parameters["feature"] == "MBI":
            mbi_feature(execution_parameters["input"],
                        output=execution_parameters["output"],
                        postprocess=execution_parameters["postprocess"])
    tot_sec = time.time() - start_time
    minutes = int(tot_sec // 60)
    sec = tot_sec % 60
    print('\nEnd data & time -- (%s)\nTotal processing time -- (%d min %f sec)\n' %
        (time.asctime(time.localtime(time.time())), minutes, sec))

def get_tif_images(directory):
    ims = []
    dir_contents = os.listdir(directory)
    for n in dir_contents:
        if n[-4:] == ".tif":
            ims.append(os.path.join(directory, n))
    return ims