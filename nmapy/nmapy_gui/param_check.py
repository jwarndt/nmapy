import os
import sys


def check_input(input_param):
    return NotImplemented

def check_output(output_param):
    return NotImplemented

def validate_and_adjust_texture_params(params):
    if params["feature"] != "MBI" and params["feature"] != "SIFT":
        scale_list = params["scale"].strip().split(',')
        scale_list = [int(n) for n in scale_list]
    else:
        if params["feature"] == "SIFT" and params["sift_mode"] == 2:
            scale_list = params["scale"].strip().split(',')
            scale_list = [int(n) for n in scale_list]
        else:
            scale_list = [None]

    params["scale"] = scale_list

    if params["feature"] == "SIFT" and params["sift_mode"] == 1:
        im_dir_list = params["input"].strip().split(',')
        params["input"] = im_dir_list

    if params["feature"] == "LBP":
        radius_list = params["radius"].strip().split(',')
        radius_list = [int(n) for n in radius_list]
        point_list = params["n_points"].strip().split(',')
        point_list = [int(n) for n in point_list]
        params["radius"] = radius_list
        params["n_points"] = point_list

    if params["stat"] == "None":
        params["stat"] = None
    if params["prop"] == "None":
        params["prop"] = None
    if params["postprocess"] == 'True':
        params["postprocess"] = True
    elif params["postprocess"] == 'False':
        params["postprocess"] = False
    return params