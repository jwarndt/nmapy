import time
import os
from multiprocessing import Pool

from ..features.hog import *
from ..features.glcm import *
from ..features.lac import *
from ..features.mbi import *

def old_execute(execution_parameters):
    start_time = time.time()
    print('\nStart date & time --- (%s)\n' % time.asctime(time.localtime(time.time())))
    print("User Input:")
    print("-----------")
    print("input:   " + execution_parameters["input"])
    print("output:  " + execution_parameters["output"])
    print("feature: " + execution_parameters["feature"])
    print()
    
    dir_processing = False
    if execution_parameters["input"][-4] != ".":
        dir_processing = True
        im_list = __get_tif_images(execution_parameters["input"])
        print("processing " + str(len(im_list)) + " images")
    else:
        im_list = [execution_parameters["input"]]
        print("processing 1 image")
    
    if execution_parameters["output"][:-4] != ".":
        auto_output_naming = True
        outdir = execution_parameters["output"]
    else:
        if dir_processing:
            print("error: cannot read a directory of images and output them to a single image")
            print("you must also pass in a directory for the output location if you specify a ")
            print("directory as input")
            return
    
    if execution_parameters["stat"] == "None":
        execution_parameters["stat"] = None
    if execution_parameters["prop"] == "None":
        execution_parameters["prop"] = None
    execution_parameters["postprocess"] = bool(execution_parameters["postprocess"])
    
    count = 0
    # params = [execution_parameters for n in im_list]
    # for n in im_list:
    #     params["input"] = n

    for input_im in im_list:
        execution_parameters["input"] = input_im
        s = time.time()
        print("input: " + input_im)
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
                out_im_basename = os.path.basename(input_im)[:-4] + "_GLCM_BK" + str(execution_parameters["block"]) + "_SC" + str(execution_parameters["scale"]) + "PRP" + execution_parameters["prop"] + "_ST" + str(execution_parameters["stat"]) +".tif"
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
        count+=1
        tot_sec = time.time() - s
        minutes = int(tot_sec // 60)
        sec = tot_sec % 60
        print("done with image " + str(count) + " of " + str(len(im_list)))
        print("Total processing time -- (%d min %f sec)\n" % (minutes, sec))
    tot_sec = time.time() - start_time
    minutes = int(tot_sec // 60)
    sec = tot_sec % 60
    print('\nEnd data & time -- (%s)\nTotal processing time -- (%d min %f sec)\n' %
        (time.asctime(time.localtime(time.time())), minutes, sec))
    print("----------------------- End ------------------------------")

def __multi_process(execution_parameters):
    input_im = execution_parameters["input"]
    if execution_parameters["stat"] == "None":
        execution_parameters["stat"] = None
    if execution_parameters["prop"] == "None":
        execution_parameters["prop"] = None
    execution_parameters["postprocess"] = bool(execution_parameters["postprocess"])
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
            out_im_basename = os.path.basename(input_im)[:-4] + "_GLCM_BK" + str(execution_parameters["block"]) + "_SC" + str(execution_parameters["scale"]) + "PRP" + execution_parameters["prop"] + "_ST" + str(execution_parameters["stat"]) +".tif"
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
    tot_sec = time.time() - s
    minutes = int(tot_sec // 60)
    sec = tot_sec % 60
    print("input: " + input_im)
    print("done with image " + str(execution_parameters["count"]) + " of " + str(execution_parameters["total"]))
    print("Total processing time -- (%d min %f sec)\n" % (minutes, sec))

def execute(execution_parameters):
    p = Pool(int(execution_parameters["jobs"]))
    start_time = time.time()
    print('\nStart date & time --- (%s)\n' % time.asctime(time.localtime(time.time())))
    print("User Input:")
    print("-----------")
    print("input:   " + execution_parameters["input"])
    print("output:  " + execution_parameters["output"])
    print("feature: " + execution_parameters["feature"])
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
    
    count = 0
    # task parralelism
    if dir_processing:
        paramslist = []
        i = 0
        while i < len(im_list):
            paramslist.append({"input":im_list[i],
                              "output":execution_parameters["output"],
                              "scale": execution_parameters["scale"],
                              "block":execution_parameters["block"],
                              "box_size":execution_parameters["box_size"],
                              "prop":execution_parameters["prop"],
                              "stat":execution_parameters["stat"],
                              "postprocess":execution_parameters["postprocess"],
                              "lac_type":execution_parameters["lac_type"],
                              "slide_style":execution_parameters["slide_style"],
                              "feature":execution_parameters["feature"],
                              "count": i+1,
                              "total": len(im_list)})
            i+=1
        p.map(__multi_process, paramslist)
    else:
        execution_parameters["count"] = 1
        execution_parameters["total"] = 1
        __multi_process(execution_parameters)
    
    tot_sec = time.time() - start_time
    minutes = int(tot_sec // 60)
    sec = tot_sec % 60
    print('\nEnd data & time -- (%s)\nTotal processing time -- (%d min %f sec)\n' %
        (time.asctime(time.localtime(time.time())), minutes, sec))
    print("----------------------- End ------------------------------")

def __get_tif_images(directory):
    ims = []
    dir_contents = os.listdir(directory)
    for n in dir_contents:
        if n[-4:] == ".tif":
            ims.append(os.path.join(directory, n))
    return ims