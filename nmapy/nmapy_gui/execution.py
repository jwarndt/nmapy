from ..features.hog import *
from ..features.glcm import *
from ..features.lac import *
from ..features.mbi import *

def execute(execution_parameters):
    print("executing...")
    return
    if execution_parameters[2] == "HOG":
        hog_feature(execution_parameters["input"],
                    execution_parameters["block"],
                    execution_parameters["scale"],
                    output=execution_parameters["output"],
                    stat=execution_parameters["stat"])
    elif execution_parameters[2] == "GLCM":
        glcm_feature(execution_parameters["input"],
                    execution_parameters["block"],
                    execution_parameters["scale"],
                    output=execution_parameters["output"],
                    prop=execution_parameters["prop"],
                    stat=execution_parameters["stat"])
    elif execution_parameters[2] == "Pantex":
        pantex_feature(execution_parameters["input"],
                       execution_parameters["block"],
                       execution_parameters["scale"],
                       output=execution_parameters["output"])
    elif execution_parameters[2] == "Lacunarity":
        lacunarity_feature(execution_parameters["input"],
                           execution_parameters["block"],
                           execution_parameters["scale"],
                           box_size=execution_parameters["box_size"],
                           output=execution_parameters["output"],
                           slide_style=execution_parameters["slide_style"],
                           lac_type=execution_parameters["lac_type"])
    elif execution_parameters[2] == "MBI":
        mbi_feature(execution_parameters["input"],
                    output=execution_parameters["output"],
                    postprocess=execution_parameters["postprocess"])