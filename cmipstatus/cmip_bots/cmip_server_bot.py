#from fabric.api import run, env, settings, get, put, cd
#from time import sleep
#from os.path import join
import urllib
import yaml
import os
import time

all_info = yaml.load(open('exp_info.yaml', 'r'))

DESTINATION = 'fetched_data'

def get_running_stats():
    urllib.urlretrieve (all_info['paths']['web_runstats'], 'fetched_data/running_info.txt')

def get_restart_list(expname):
    restart_name = 'RESTARTLIST.{0}.tmp'.format(expname)
    urllib.urlretrieve (all_info['paths']['web_restartlist'].format(expname), 
                        os.path.join('fetched_data', restart_name))
    

if __name__ == "__main__":
    while True:
        print "refreshing"
        get_running_stats()
        print "no members"
        [get_restart_list(exp) for exp in  all_info['exps']['no-members']]
        for member in range(1,11):
            print "member", member
            [get_restart_list(exp+'_'+str(member)) for exp in all_info['exps']['with-members']]
        time.sleep(900)
