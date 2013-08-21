import numpy as np
from pupynere import netcdf_file
from errorcodes import MINVALUE

THRESHOLD = 9e+36

def run(data):
    has_error = False
    for v in data.variables:
        try:
            vmin = np.min(data.variables[v][:])
            if vmin > THRESHOLD:
                #TODO log
                has_error = True
        except:
            has_error = True
    
    if has_error:
        return MINVALUE

    return 0
