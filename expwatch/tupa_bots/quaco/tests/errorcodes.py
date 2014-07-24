FILESIZE = 1
MINVALUE = 2
LOADERR = 4
ALLZERO = 8
STD0ERR = 16


descriptions = {
    FILESIZE: 'file size too small',
    MINVALUE: 'min value too high (possibly all undefined)',
    LOADERR: 'could not open file',
    ALLZERO: 'all values zero',
    STD0ERR: 'standard deviation is zero',
}


def decode(code):
    error_list = [code & error for error in descriptions.keys()]
    desc_list = [descriptions[error] for error in error_list if error]
    return desc_list
