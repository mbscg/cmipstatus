import os
from errorcodes import FILESIZE

MIN_FILESIZE = 100 #bytes

def run(filename):
    statinfo = os.stat(filename)
    if statinfo.st_size < MIN_FILESIZE:
        return FILESIZE
    else:
        return 0
