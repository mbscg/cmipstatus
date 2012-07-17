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

if __name__ == "__main__":
    restart_interval = 1200
    while True:
        for exp in all_info['exps']['no-members']:
            get_restart_list(exp, '')
        for member in range(1,11):
            for exp in all_info['exps']['with-members']:            
                get_restart_list(exp, '_'+str(member))
        [os.chmod(restart, permissions) for restart
         in glob.glob(os.path.join(all_info['paths']['ftp_root'],'RESTART*'))]
        time.sleep(restart_interval)
