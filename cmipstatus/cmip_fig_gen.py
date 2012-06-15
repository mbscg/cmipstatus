from fabric.api import run, env, settings, get, cd, prefix
from time import sleep
from os.path import join
from os import makedirs
import glob

RESTART_LIST_TEMPLATE = '/stornext/{0}/ocean/simulations/{1}/experiment_design/RESTARTLIST.{2}.tmp'

def get_restart_list(exp_name, member_name):
    disk = "online2"
    if '_' in member_name:
        member_index = int(member_name.split('_')[-1])
        if member_index > 4:
            disk = "online12"
    file_to_read = RESTART_LIST_TEMPLATE.format(disk, exp_name, exp_name+member_name)
    with settings(host_string='ocean@tupa', warn_only=True):
        get(file_to_read, join('fetched_data'))


OUTPUT_DIR_TEMPLATE = '/stornext/{0}/ocean/simulations/{1}/dataout/*/*/{2}/ocean/CGCM/'
SCRIPT_LINE = "cmip_base_eval_gg.bash {0} {1} {2} {3} {4} '{5}'"
FIGS_DIR = '/scratchin/grupos/ocean/home/ocean/cmip_evaluation/{0}_{1}/*'
DEST_DIR = 'fetched_data/images/{0}_{1}'

def gen_figures(exp, member=None):
    with settings(host_string='ocean@tupa', warn_only=True):
        with cd('cmipstatus_scripts'):
            member_index = '01'
            if member:
                if member > 4:
                    disk = 'online12'
                else:
                    disk = 'online2'
                if member < 10:
                    member_index = '0' + str(member)
                else:
                    member_index = str(member)
                incomplete_dir = OUTPUT_DIR_TEMPLATE.format(disk, exp, member_index)
            else: #only one dir
                cmp007_i = '1966010100'
                cmp007_f = '1975120100'
                #cmp007_r = 'SA'
                #cmp007_n = 'cmp007'
                incomplete_dir = OUTPUT_DIR_TEMPLATE.format('online2', exp, '01')
            complete_dir = run('find {0} -type d'.format(incomplete_dir))
            print complete_dir
            regions = ['SA', 'SH', 'GT', 'NH', 'GB', 'TP', 'TA']
            with prefix('module load grads'):
                for region in regions:
                    pass
                    #run(SCRIPT_LINE.format('1', 'last', region, exp, str(member), complete_dir))
                    #run(SCRIPT_LINE.format('1981010100', '19820101000', region, exp, str(member), complete_dir))
        #bring them all
        figs_dir = FIGS_DIR.format(exp, str(member))
        dest_dir = DEST_DIR.format(exp, str(member))
        print "or, dest", figs_dir, dest_dir
        get(figs_dir, dest_dir)


if __name__ == "__main__":
    restart_interval = 900
    restart_count = 0
    exps_with_members = ['004', '006','008','010','012','014','016', '018','022','023']
    exps_no_members = ['001','002','003','005','007','009','011','013','015','017','019','020','021']
    while True:
        for exp in exps_with_members:
            for m in range(1,11):
                get_restart_list('cmp'+exp, '_'+str(m))
                #if restart_count == 0:
                #    gen_figures('cmp'+exp, member=m) 
        for exp in exps_no_members:
            get_restart_list('cmp'+exp, '')
            #if restart_count == 0:
            #   gen_figures('cmp'+exp)
        restart_count = (restart_count + 1) % 10 
        sleep(restart_interval)
        #Testing
        #gen_figures('cmp012', member=1)
        #gen_figures('cmp012', member=4)
        #gen_figures('cmp007')
        break
             

