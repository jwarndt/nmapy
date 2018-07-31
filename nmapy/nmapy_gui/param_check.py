import os
import sys


def check_input(input_param):
    return NotImplemented

def check_output(output_param):
    return NotImplemented

def validate_and_adjust_texture_params(params):
    if params["feature"] != "MBI":
        scale_list = params["scale"].strip().split(',')
        scale_list = [int(n) for n in scale_list]
        params["scale"] = scale_list
    else:
        params["scale"] = [None]

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