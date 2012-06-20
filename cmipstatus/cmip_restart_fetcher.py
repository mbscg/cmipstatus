from fabric.api import run, env, settings, get, put, cd, prefix
from time import sleep
from os.path import join
from os import makedirs
import datetime
from random import shuffle

RESTART_LIST_FILE = 'RESTARTLIST.{0}.tmp'
RESTART_LIST_BLEEDING = '/stornext/home/manoel.baptista/exp_repos/exp/cpld/RESTARTLIST/{0}'
ANTARES_RESTARTS_DIR = '/home/opendap/cmipsite/cmipstatus/fetched_data/'

def get_restart_list(exp_name, member_name):
    disk = "online2"
    env.use_ssh_config = True
    if '_' in member_name:
        member_index = int(member_name.split('_')[-1])
        if member_index > 4:
            disk = "online12"
    #file_to_read = RESTART_LIST_TEMPLATE.format(disk, exp_name, exp_name+member_name)
    restart_filename = RESTART_LIST_FILE.format(exp_name+member_name)
    file_to_read = RESTART_LIST_BLEEDING.format(restart_filename)
    with settings(host_string='ocean@tupa', warn_only=True):
        get(file_to_read, join('fetched_data'))
    with settings(host_string='opendap@antares', warn_only=True):
        put(join('fetched_data', restart_filename), ANTARES_RESTARTS_DIR)

if __name__ == "__main__":
    restart_interval = 600
    exps_with_members = ['016', '004', '006','008','010','012','014', '018','022','023']
    shuffle(exps_with_members)
    exps_no_members = ['001','002','005','007','009','011','013','015','017','019','020','021']
    shuffle(exps_no_members)
    while True:
        print "refresh status"
        for exp in exps_with_members:
            for m in range(1,11):
                get_restart_list('cmp'+exp, '_'+str(m))
        for exp in exps_no_members:
            get_restart_list('cmp'+exp, '')
        sleep(restart_interval)
