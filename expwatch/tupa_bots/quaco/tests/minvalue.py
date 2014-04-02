import numpy as np
from pupynere import netcdf_file
from errorcodes import MINVALUE

THRESHOLD = 9e+36

def run(data):
    for v in data.variables:
        try:
            vmin = np.min(data.variables[v][:])
            if vmin > THRESHOLD:
                #TODO log
                return MINVALUE
        except:
            pass
    
    return 0
