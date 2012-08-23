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

    root = '/stornext/online13/ocean/simulations/CMIP/CMIP5/output/INPE/BESM-OA2-3/'
    frequency = 'mon'
    condition = 'r{0}i1p{1}'
    fmt_condition = 'r{0} i1 p{1}'
    variables = [('atmos', 'tas', 40), ('ocean', 'tos', 42), ('land', 'mrsos', 2)]

    text_lines = []

    for decade in decades:
        decade_expected = 120.
        if decade_expected in decades30:
            decade_expected = 360.
        for r in range(1,11): #r1 a r10
            for p in range(1,3): #p1 e p2
                cond = condition.format(r, p)
                fmt_cond = fmt_condition.format(r, p)
                cond_total = 0.
                cond_weights = 0.
                for var in variables:
                    directory = os.path.join(root, decade, frequency, var[0], var[1], cond)
                    try:
                        ls = os.listdir(directory)
                    except:
                        continue
                    else:
                        var_total = len(ls)
                        progress = str(var_total / decade_expected)
                        line = ' '.join([decade, fmt_cond, str(var_total), str(decade_expected), progress, '\n'])
                        text_lines.append(line)


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
