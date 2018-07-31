import time
import os
import pprint
from multiprocessing import Pool

from ..features.hog import *
from ..features.glcm import *
from ..features.lac import *
from ..features.mbi import *
from ..features.lbp import *
from .param_check import *

def execute(execution_parameters):
    p = Pool(int(execution_parameters["jobs"]))

    execution_parameters = validate_and_adjust_texture_params(execution_parameters)

    start_time = time.time()
    print('\nStart date & time --- (%s)\n' % time.asctime(time.localtime(time.time())))
    print("User Input:")
    print("-----------")
    pp = pprint.PrettyPrinter(indent=4,width=5)
    pp.pprint(execution_parameters)
    print()
    
    dir_processing = False
    if execution_parameters["input"][-4] != ".":
        dir_processing = True
        im_list = __get_tif_images(execution_parameters["input"])
        print("processing " + str(len(im_list)) + " images")
    else:
        im_list = [execution_parameters["input"]]
        print("processing 1 image")
    
    if execution_parameters["output"][:-4] == ".":
        if dir_processing:
            print("error: cannot read a directory of images and output them to a single image")
            print("you must also pass in a directory for the output location if you specify a ")
            print("directory as input")
            return
    
    # data parralelism
    feature_count = 0
    paramslist = []
    i = 0
    while i < len(im_list):
        # holds a nested list of execution parameters parameters. each nested list of parameters, corresponds to a single image
        # so it's like: [ [{image1 feat1parms}, {image1 feat12parms}], [image2 feat1parms, image2 feat12parms], ... ]
        feature_list = []
        s = 0
        while s < len(execution_parameters["scale"]):
            feature_list.append({"input":im_list[i],
                              "output":execution_parameters["output"],
                              "scale": execution_parameters["scale"][s],
                              "block":execution_parameters["block"],
                              "box_size":execution_parameters["box_size"],
                              "prop":execution_parameters["prop"],
                              "stat":execution_parameters["stat"],
                              "postprocess":execution_parameters["postprocess"],
                              "lac_type":execution_parameters["lac_type"],
                              "slide_style":execution_parameters["slide_style"],
                              "feature":execution_parameters["feature"],
                              "lbp_method":execution_parameters["lbp_method"],
                              "radius":execution_parameters["radius"],
                              "n_points":execution_parameters["n_points"]})
            s+=1
            feature_count+=1
        paramslist.append(feature_list)
        i+=1
    print("processing " + str(feature_count) + " features\n")
    if dir_processing:
        p.map(__process, paramslist)
    else:
        __process(paramslist[0])
    
    tot_sec = time.time() - start_time
    minutes = int(tot_sec // 60)
    sec = tot_sec % 60
    print('\nEnd data & time -- (%s)\nTotal processing time -- (%d min %f sec)\n' %
        (time.asctime(time.localtime(time.time())), minutes, sec))
    print("----------------------- End ------------------------------")


def __process(execution_parameters_list):
    pp = pprint.PrettyPrinter(indent=4,width=5)
    for execution_parameters in execution_parameters_list:
        input_im = execution_parameters["input"]
        if execution_parameters["output"][:-4] != ".":
            auto_output_naming = True
            outdir = execution_parameters["output"]
        s = time.time()
        
        if execution_parameters["feature"] == "HOG":
            if auto_output_naming:
                out_im_basename = os.path.basename(input_im)[:-4] + "_HOG_BK" + str(execution_parameters["block"]) + "_SC" + str(execution_parameters["scale"]) +"_ST" + str(execution_parameters["stat"]) +".tif"
                execution_parameters["output"] = os.path.join(outdir, out_im_basename)
            hog_feature(execution_parameters["input"],
                        execution_parameters["block"],
                        execution_parameters["scale"],
                        output=execution_parameters["output"],
                        stat=execution_parameters["stat"])
        
        elif execution_parameters["feature"] == "GLCM":
            if auto_output_naming:
                out_im_basename = os.path.basename(input_im)[:-4] + "_GLCM_BK" + str(execution_parameters["block"]) + "_SC" + str(execution_parameters["scale"]) + "_PRP" + str(execution_parameters["prop"]) + "_ST" + str(execution_parameters["stat"]) +".tif"
                execution_parameters["output"] = os.path.join(outdir, out_im_basename)
            glcm_feature(execution_parameters["input"],
                        execution_parameters["block"],
                        execution_parameters["scale"],
                        output=execution_parameters["output"],
                        prop=execution_parameters["prop"],
                        stat=execution_parameters["stat"])
        
        elif execution_parameters["feature"] == "Pantex":
            if auto_output_naming:
                out_im_basename = os.path.basename(input_im)[:-4] + "_PANTEX_BK" + str(execution_parameters["block"]) + "_SC" + str(execution_parameters["scale"]) + ".tif"
                execution_parameters["output"] = os.path.join(outdir, out_im_basename)
            pantex_feature(execution_parameters["input"],
                           execution_parameters["block"],
                           execution_parameters["scale"],
                           output=execution_parameters["output"])
        
        elif execution_parameters["feature"] == "Lacunarity":
            if auto_output_naming:
                out_im_basename = os.path.basename(input_im)[:-4] + "_LAC_BK" + str(execution_parameters["block"]) + "_SC" + str(execution_parameters["scale"]) +"_BXSZ" + str(execution_parameters["box_size"]) + "_SLD" + str(execution_parameters["slide_style"]) + "_TYP" + execution_parameters["lac_type"] +".tif"
                execution_parameters["output"] = os.path.join(outdir, out_im_basename)
            lac_feature(execution_parameters["input"],
                               execution_parameters["block"],
                               execution_parameters["scale"],
                               box_size=execution_parameters["box_size"],
                               output=execution_parameters["output"],
                               slide_style=execution_parameters["slide_style"],
                               lac_type=execution_parameters["lac_type"])
        
        elif execution_parameters["feature"] == "MBI":
            if auto_output_naming:
                out_im_basename = os.path.basename(input_im)[:-4] + "_MBI_PP" + str(execution_parameters["postprocess"]) + ".tif"
                execution_parameters["output"] = os.path.join(outdir, out_im_basename)
            mbi_feature(execution_parameters["input"],
                        output=execution_parameters["output"],
                        postprocess=execution_parameters["postprocess"])
        
        elif execution_parameters["feature"] == "LBP":
            if auto_output_naming:
                out_im_basename = os.path.basename(input_im)[:-4] + "_LBP_BK" + str(execution_parameters["block"]) + "_SC" + str(execution_parameters["scale"]) + "_ST" + str(execution_parameters["stat"]) +".tif"
                execution_parameters["output"] = os.path.join(outdir, out_im_basename)
            lbp_feature(execution_parameters["input"],
                        execution_parameters["block"],
                        execution_parameters["scale"],
                        output=execution_parameters["output"],
                        method=execution_parameters["lbp_method"],
                        radius=execution_parameters["radius"],
                        n_points=execution_parameters["n_points"],
                        stat=execution_parameters["stat"])
        
        tot_sec = time.time() - s
        minutes = int(tot_sec // 60)
        sec = tot_sec % 60
        print("---------- done with feature ----------")
        pp.pprint(os.path.basename(execution_parameters["output"]))
        print("Total processing time -- (%d min %f sec)\n" % (minutes, sec))

def __get_tif_images(directory):
    ims = []
    dir_contents = os.listdir(directory)
    for n in dir_contents:
        if n[-4:] == ".tif":
            ims.append(os.path.join(directory, n))
    return ims