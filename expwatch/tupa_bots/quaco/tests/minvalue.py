import numpy as np
from pupynere import netcdf_file
from errorcodes import MINVALUE

THRESHOLD = 9e+36

def run(data, var):
    """
    returns MINVALUE error if the min value is UNDEFINED
    """
    try:
        vmin = np.min(data.variables[var][:])
        if vmin > THRESHOLD:
            #TODO log
            return MINVALUE
    except:
        pass
    
    return 0
