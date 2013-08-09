from fabric.api import settings, run
import yaml
import time
import os
import stat

config = yaml.load(open('running_stats.config', 'r'))
permissions = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP |\
              stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH


 
def get_running_stats():
    with settings(host_string='ocean@tupa', warn_only=True):
        results = run('stat_cpld ocean')
        stats_file = config['qstat_log']
        f = open(stats_file, 'w')
        f.writelines(results)
        f.writelines(['\n'])
        f.close()
        os.chmod(stats_file, permissions)
        print "saved into", stats_file


if __name__ == "__main__":
    print "getting running stats"
    get_running_stats()
