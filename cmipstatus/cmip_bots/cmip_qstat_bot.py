from fabric.api import settings, run
import yaml
import time
import os
import stat

all_info = yaml.load(open('exp_info.yaml', 'r'))
permissions = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH

def get_running_stats():
    with settings(host_string='g.marcondes@tupa', warn_only=True):
        results = run('stat_cpld manoel.baptista')
        stats_file = all_info['paths']['qstat_log']
        f = open(stats_file, 'w')
        f.writelines(results)
        f.writelines(['\n'])
        f.close()
        os.chmod(stats_file, permissions)


if __name__ == "__main__":
    interval = 900
    while True:
        print "refreshing"
        get_running_stats()
        time.sleep(interval)
