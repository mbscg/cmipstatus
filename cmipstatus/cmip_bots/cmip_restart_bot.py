import time
import os
import shutil
import stat
import glob
import yaml

all_info = yaml.load(open('exp_info.yaml', 'r'))
permissions = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP |\
              stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH

def get_restart_list(exp_name, member_name):
    if '_' in member_name:
        member_index = int(member_name.split('_')[-1])
    RESTART_FILE = all_info['paths']['restartlist_origin']
    RESTART_FILE = RESTART_FILE.format(exp_name + member_name)
    RESTART_FILE_DEST = all_info['paths']['ftp_root']
    if os.path.exists(RESTART_FILE):
        shutil.copy(RESTART_FILE, RESTART_FILE_DEST)

def get_conversion_status():
    decades30 = ['decadal1960', 'decadal1980', 'decadal2005']
    decades10 = ['decadal1965', 'decadal1970', 'decadal1975', 'decadal1985', 
                 'decadal1990', 'decadal1995', 'decadal2000']
    decades = decades30 + decades10

    #root = '/stornext/online13/ocean/simulations/cmip5/CMIP5/output/INPE/INPE-OA2-3/'
    root = '/stornext/online13/ocean/simulations/CMIP/CMIP5/output/INPE/BESM-OA2-3/'
    frequency = 'mon'
    condition = 'r{0}i1p1'
    variables = [('atmos', 'tas', 40), ('ocean', 'tos', 42), ('land', 'mrsos', 2)]

    text_lines = []

    total_weights = 40 + 42 + 2
    for decade in decades:
        decade_total = 0
        variables_read = 0
        for variable in variables:
            var_total = 0
            conditions_read = 0
            for cond in range(1,11):
                c = condition.format(str(cond))
                directory = os.path.join(root, decade, frequency, variable[0], variable[1], c)
                try:
                    ls = os.listdir(directory)
                    var_total += len(ls)
                    conditions_read += 1
                except:
                    pass
                print "cond, var, decade, len(ls)", cond, variable, decade, len(ls)
            if conditions_read > 0:
                var_average = float(var_total) / conditions_read
            else:
                var_average = 0
            decade_total += var_average * variable[2]/total_weights
            variables_read += 1
        if variables_read == 0:
            text_lines.append(' '.join([decade, 'NOT FOUND', '\n']))
            continue

        expected = 120.0
        if decade in decades30:
            expected = 360.0
        current = float(decade_total)
        print "decade total, expected", decade_total, expected
        progress = current/expected
        text_lines.append(' '.join([decade, str(current), str(expected), 
                          str(progress), '\n']))

    DEST_PATH = os.path.join(all_info['paths']['ftp_root'], 'conversion.txt')
    DEST_FILE = open(DEST_PATH, 'w')
    DEST_FILE.writelines(text_lines)
    DEST_FILE.close()
    os.chmod(DEST_PATH, permissions)


if __name__ == "__main__":
    get_conversion_status()
    for exp in all_info['exps']['no-members']:
        get_restart_list(exp, '')
    for member in range(1,11):
        for exp in all_info['exps']['with-members']:            
            get_restart_list(exp, '_'+str(member))
    [os.chmod(restart, permissions) for restart
     in glob.glob(os.path.join(all_info['paths']['ftp_root'],'RESTART*'))]
