import numpy as np
import numpy.ma as ma
from pupynere import netcdf_file
from errorcodes import ALLZERO


FILL_VALUE = 1e+20

def run(data, var):
    """
    returns ALLZERO error if nonzero masked data is empty
    """
    try:
        nz = ma.array(data.variables[var][:]).nonzero()
        if not nz:
            #TODO log
            return ALLZERO
    except:
        pass
    
    return 0
