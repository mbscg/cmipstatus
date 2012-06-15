from fabric.api import run, env, settings, get, cd
from time import sleep
from os.path import join

def get_running_stats():
    with settings(host_string='ocean@tupa', warn_only=True):
        results = run('stat_cpld manoel.baptista')
    if results.succeeded:
        f = open(join('fetched_data', 'running_stats.txt'), 'w')
        f.writelines(results)
        f.writelines(['\n'])
        f.close()
    else:
        print "Failed to refresh data"


if __name__ == "__main__":
    while True:
        print "refreshing"
        get_running_stats()
        sleep(900)
