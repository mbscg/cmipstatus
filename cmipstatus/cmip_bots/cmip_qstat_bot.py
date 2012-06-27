from fabric.api import run, env, settings, get, put, cd
from time import sleep
from os.path import join


#OK!
ANTARES_STATS_DIR = '/home/opendap/cmipsite/cmipstatus/fetched_data/'

def get_running_stats():
    env.use_ssh_config = True
    with settings(host_string='ocean@tupa', warn_only=True):
        results = run('stat_cpld manoel.baptista')
    if results.succeeded:
        stats_file = join('fetched_data', 'running_stats.txt')
        f = open(stats_file, 'w')
        f.writelines(results)
        f.writelines(['\n'])
        f.close()
        #send to antares
        with settings(host_string='opendap@antares', warn_only=True):
            print "sending to antares"
            put(stats_file, ANTARES_STATS_DIR)
    else:
        print "Failed to refresh data"


if __name__ == "__main__":
    while True:
        print "refreshing"
        get_running_stats()
        sleep(900)
