from fabric.api import run, env, settings, get, put, cd, prefix
from time import sleep
from os.path import join, exists
from os import makedirs, listdir, remove
import datetime
from random import shuffle

#OK!

def get_running_dates(expname, member):
    disk = 'online2'
    if member > 4:
        disk = 'online12'
    member_index = str(member)
    if member < 10:
        member_index = '0' + member_index
    output_dir = '/stornext/{0}/ocean/simulations/{1}/dataout/*/*/{2}/output'.format(disk, expname, member_index)
    with settings(host_string='ocean@tupa', warn_only=True):
        lsresult = run('ls {0} | grep fms'.format(output_dir)).split('\n')
        dates = []
        for line in lsresult:
            dates.append(line.split('.')[0]+'00')
        if len(dates) > 3:
            return dates[1], dates[-1]
        else:
            return None


TUPA_OUTPUT_DIR_TEMPLATE = '/stornext/{0}/ocean/simulations/{1}/dataout/*/*/{2}/ocean/CGCM/'
SCRIPT_LINE = "cmip_base_eval_gg.bash {0} {1} {2} {3} {4} '{5}'"
TUPA_FIGS_DIR = '/scratchin/grupos/ocean/home/ocean/cmip_evaluation/{0}_{1}/*'
PAPERA_FIGS_DIR = '/home/gabriel/cmipsite/media/images/{0}_{1}'
ANTARES_FIGS_DIR = '/home/opendap/cmipsite/media/images/'
PAPERA_LOG_FILE = '/home/gabriel/cmipsite/cmipstatus/fetched_data/logs/{0}'
ANTARES_LOGS_DIR = '/home/opendap/cmipsite/cmipstatus/fetched_data/logs/'

def gen_figures(exp, member=None):
    env.use_ssh_config = True
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
                incomplete_dir = TUPA_OUTPUT_DIR_TEMPLATE.format(disk, exp, member_index)
            else: #only one dir
                incomplete_dir = TUPA_OUTPUT_DIR_TEMPLATE.format('online2', exp, '01')
            running_dates = get_running_dates(exp, member)
            LOG_FILE = PAPERA_LOG_FILE.format(exp+'_'+str(member)+'log.txt')
            if not running_dates:
                return
            if exists(LOG_FILE):
                log_lines = open(LOG_FILE, 'r').readlines()
                dates = log_lines[0][:-1].split(', ')
                logged_dates = (dates[0].split(': ')[-1], dates[1].split(': ')[-1])
                if logged_dates == running_dates:
                    print "no changes in graphics, skipping", exp, str(member)
                    return
            complete_dir = run('find {0} -type d'.format(incomplete_dir))
            regions = ['SA', 'SH', 'GT', 'NH', 'GB', 'TP', 'TA']
            shuffle(regions)
            with prefix('module load grads'):
                run('rm -rf {0}'.format(join(TUPA_FIGS_DIR.format(exp, str(member)))))
                for region in regions:
                    #clean old figs
                    run(SCRIPT_LINE.format(running_dates[0], running_dates[1], region, exp, str(member), complete_dir))
        #bring them all
        print "getting",  exp, member
        figs_dir = TUPA_FIGS_DIR.format(exp, str(member))
        dest_dir = PAPERA_FIGS_DIR.format(exp, str(member))
        #clean local dir
        old_figs = listdir(join(dest_dir, 'figures'))
        for old_fig in old_figs:
            remove(join(dest_dir, 'figures', old_fig))
        #get news figs
        get(figs_dir, dest_dir)
        loginfo = 'start date: {0}, end date: {1}\n'.format(running_dates[0], running_dates[1])
        loginfo += 'last generated: {0}\n'.format(str(datetime.datetime.now()))
        log_file = PAPERA_LOG_FILE.format(exp+'_'+str(member)+'log.txt')
        log = open(log_file, 'w')
        log.write(loginfo)
        log.close()
    #send them all
    print "sending", exp, member
    with settings(host_string='opendap@antares', warn_only=True):
        #clean remote dir
        exp_fig_dirname = exp+'_'+str(member)
        run('rm -rf {0}'.format(join(ANTARES_FIGS_DIR, exp_fig_dirname)))
        #copy new figs
        put(PAPERA_FIGS_DIR.format(exp, str(member)), ANTARES_FIGS_DIR) #.format(exp, str(member)))
        put(PAPERA_LOG_FILE.format(exp+'_'+str(member)+'log.txt'), ANTARES_LOGS_DIR)


if __name__ == "__main__":
    restart_interval = 60
    exps_with_members = ['008', '016', '004', '006','010','012','014', '018','022','023']
    shuffle(exps_with_members)
    exps_no_members = ['001','002','005','007','009','011','013','015','017','019','020','021']
    shuffle(exps_no_members)
    while True:
        print "refresh figures"
        for exp in exps_with_members:
            for m in range(1,11):
                gen_figures('cmp'+exp, m)
        for exp in exps_no_members:
            gen_figures('cmp'+exp, 1)
        sleep(restart_interval)
