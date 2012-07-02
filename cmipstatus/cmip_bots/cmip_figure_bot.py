import yaml
import os
import stat
import glob
import subprocess
import datetime
import random
import multiprocessing
import time


#this will run directly on tupa!
all_info = yaml.load(open('exp_info.yaml', 'r'))


def get_running_dates(expname, member):
    disk = 'online2'
    if member > 4 or expname == 'cmp003':
        disk = 'online12'
    member_index = str(member)
    if member < 0:
        member_index = '*'
    elif member < 10:
        member_index = '0' + member_index
    output_dir = all_info['paths']['tupa_exp_output']
    output_dir = output_dir.format(disk, expname, member_index)
    try:
        lsresult = os.listdir(glob.glob(output_dir)[0])
    except:
        return None
    filtered_ls = [result for result in lsresult if 'fms' in result]
    filtered_ls.sort()
    dates = [line.split('.')[0]+'00' for line in filtered_ls]
    if len(dates) > 3:
        return dates[1], dates[-2]
    else:
        return None


def gen_figures(exp, member=None):
    member_index = '01'
    disk = 'online2'
    if member:
        if member > 4:
            disk = 'online12'
        if member < 10:
            member_index = '0' + str(member)
        else:
            member_index = str(member)
        incomplete_dir = all_info['paths']['tupa_exp_cgcm']
        incomplete_dir = incomplete_dir.format(disk, exp, member_index)
        running_dates = get_running_dates(exp, member)
    else:
        member = 1
        if exp == 'cmp003':
            disk = 'online12'
        incomplete_dir = all_info['paths']['tupa_exp_cgcm']
        incomplete_dir = incomplete_dir.format(disk, exp, '*')
        running_dates = get_running_dates(exp, -1)
    if not running_dates:
        return
    log_file = all_info['paths']['tupa_log_template'].format(exp, str(member))
    if os.path.exists(log_file):
        log = yaml.load(open(log_file, 'r'))
        logged_dates = (log['start_date'], log['end_date'])
        if logged_dates == running_dates:
            print "no changes in graphics for ", exp, str(member)
            return
    complete_dir = glob.glob(incomplete_dir)[0]
    regions = ['SA', 'SH', 'GT', 'NH', 'GB', 'TP', 'TA']
    random.shuffle(regions)
    for region in regions:
        #generate
        args = [running_dates[0], running_dates[1], region, exp, str(member),
                complete_dir]
        try:
            subprocess.call([all_info['scripts']['leo_eval_script']] + args)
        except:
            print "Error generating for ", args
            print "Next..."
    #clean old
    new_dir = all_info['paths']['tupa_figs_dir'].format(exp, str(member))
    old_dir = os.path.dirname(new_dir)
    if os.path.exists(old_dir):
        [os.remove(old_fig) 
         for old_fig in glob.glob(os.path.join(old_dir, '*')) 
         if not os.path.isdir(old_fig)]
    #bring new to place
    if os.path.exists(new_dir):
        [os.rename(new_fig, os.path.join(old_dir, os.path.split(new_fig)[1]))\
         for new_fig in glob.glob(os.path.join(new_dir, '*'))]
    #log
    log_info = {'start_date':running_dates[0], 'end_date':running_dates[1],
                'last_generated':str(datetime.datetime.now())}
    yaml.dump(log_info, open(log_file, 'w'))
    #grant permissions
    permissions = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP\
                  | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH
    os.chmod(os.path.dirname(old_dir), permissions)
    os.chmod(old_dir, permissions)
    [os.chmod(f, permissions) for f in glob.glob(os.path.join(old_dir, '*'))]


if __name__ == "__main__":
    while True:
        exps = all_info['exps']['no-members']
        random.shuffle(exps)
        [gen_figures(exp) for exp in exps]
        exps = all_info['exps']['with-members']
        random.shuffle(exps)
        for member in range (1,11):
            [gen_figures(exp, member) for exp in exps]
