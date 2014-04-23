FILESIZE = 1
MINVALUE = 2
LOADERR = 4
ALLZERO = 8


descriptions = {
    FILESIZE: 'file size too small',
    MINVALUE: 'min value too high (possibly all undefined)',
    LOADERR: 'could not open file',
    ALLZERO: 'all values zero',
}


def decode(code):
    error_list = [code & error for error in [1,2,4,8]]
    desc_list = [descriptions[error] for error in error_list if error]
    return desc_list
