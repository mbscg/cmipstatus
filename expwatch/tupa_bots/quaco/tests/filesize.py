import os

MIN_FILESIZE = 100 #bytes

def run(filename):
    statinfo = os.stat(filename)
    if statinfo.st_size < 100:
        return bin(1)
    else:
        return 0
