from ..features.hog import *
from ..features.glcm import *
from ..features.lac import *
from ..features.mbi import *

def execute(execution_parameters):
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

    elif execution_parameters[2] == "MBI":