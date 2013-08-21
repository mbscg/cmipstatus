from pupynere import netcdf_file
from errorcodes import LOADERR

def run(filename):
    try:
        data = netcdf_file(filename)
    except:
        return LOADERR, None
    return 0, data
