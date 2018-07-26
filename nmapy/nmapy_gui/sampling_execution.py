import time
import pprint

from ..sampling.create_image_chips import create_training_chips
from ..sampling.create_training_plots import create_training_plots
from ..sampling.create_training_points import create_random_points

def execute(execution_parameters):
    start_time = time.time()
    print('\nStart date & time --- (%s)\n' % time.asctime(time.localtime(time.time())))
    print("User Input:")
    print("-----------")
    pp = pprint.PrettyPrinter(indent=4,width=5)
    pp.pprint(execution_parameters)
    print()
    
    __process(execution_parameters)

    tot_sec = time.time() - start_time
    minutes = int(tot_sec // 60)
    sec = tot_sec % 60
    print('\nEnd data & time -- (%s)\nTotal processing time -- (%d min %f sec)\n' %
        (time.asctime(time.localtime(time.time())), minutes, sec))
    print("----------------------- End ------------------------------")

def __process(execution_parameters):
    if execution_parameters['sample_type'] == "Random points":
        print("sample type:      " + execution_parameters['sample_type'])
        print("input shapefile:  " + execution_parameters["input_shp"])
        print("output shapefile: " + execution_parameters["output_shp"])
        print("points per class: " + execution_parameters["ppc"])
        print()
        create_random_points(execution_parameters["input_shp"],
                             execution_parameters["output_shp"],
                             int(execution_parameters["ppc"]))

    elif execution_parameters['sample_type'] == "Image chips":
        print("sample type:          " + execution_parameters['sample_type'])
        print("input shapefile:      " + execution_parameters["input_shp"])
        print("input directory:      " + execution_parameters["input_imdir"])
        print("output directory:     " + execution_parameters["output_imdir"])
        print("chips per feature:    " + execution_parameters["cpf"])
        print("image chip dimension: " + execution_parameters["dim"] + "x" + execution_parameters["dim"])
        print("number of trials:     " + execution_parameters["trials"])
        print()
        create_training_chips(execution_parameters["input_shp"],
                              execution_parameters["input_imdir"],
                              execution_parameters["output_imdir"],
                              int(execution_parameters["cpf"]),
                              int(execution_parameters["dim"]),
                              int(execution_parameters["trials"]))

    elif execution_parameters['sample_type'] == "Square boxes":
        print("sample type:       " + execution_parameters['sample_type'])
        print("input shapefile:   " + execution_parameters["input_shp"])
        print("output shapefile:  " + execution_parameters["output_shp"])
        print("plots per feature: " + execution_parameters["ppf"])
        print("plot dimension:    " + execution_parameters["dim"] + "x" + execution_parameters["dim"])
        print("number of trials:  " + execution_parameters["trials"])
        print()
        create_training_plots(execution_parameters["input_shp"],
                              execution_parameters["output_shp"],
                              int(execution_parameters["ppf"]),
                              int(execution_parameters["dim"]),
                              int(execution_parameters["trials"]))