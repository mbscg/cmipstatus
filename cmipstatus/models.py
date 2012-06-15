from django.db import models
from datetime import datetime
from os.path import join
from cmip_fig_gen import get_restart_list, gen_figures


class Experiment(models.Model):
    name = models.CharField(max_length=15)

    def get_status(self, tupa_data):
        done, total = check_restart_list(self.name, '')
        current = check_status(self.name, '', tupa_data)
        return done, total, current

    def get_figures(self):
        #gen_figures(self.name)
        pass

    def __unicode__(self):
        return self.name


class Member(models.Model):
    name = models.CharField(max_length=3)
    exp = models.ForeignKey('Experiment')

    def get_status(self,tupa_data):
        done, total = check_restart_list(self.exp.name, self.name)
        current = check_status(self.exp.name, self.name, tupa_data)
        return done, total, current

    def get_figures(self):
        #gen_figures(self.exp, member=self.name)
        pass

    def __unicode__(self):
        return self.name


def check_restart_list(exp_name, member_name):
    print "checking restart count..."
    restart_list = open(join('cmipstatus', 'fetched_data', "RESTARTLIST.{0}.tmp".format(exp_name+member_name)), 'r')
    restarts = 0
    done = 0
    for line in restart_list:
        restarts += 1
        if 'END' in line:
            done += 1
    return done, restarts


def check_status(exp_name, member_name, tupa_data):
    print "checking runnning stats"
    if tupa_data:
        lines = tupa_data.split('\n')
        lines.pop(0)
        for line in lines:
            columns = line.split()
            if len(columns) > 0 and columns[1].endswith(exp_name+member_name):
                return columns
    return [None, 'M_'+exp_name+member_name, None, None, '0%']


def get_tupa_data():
    f = open(join('cmipstatus', 'fetched_data', 'running_stats.txt'), 'r')
    query_result = f.read()
    f.close()
    return query_result
    

class TupaQuery(models.Model):
    name = models.CharField(max_length=5)
    query_result = models.CharField(max_length=10240)
    last_checked = models.DateTimeField()
    refresh_time = models.IntegerField()

    def get_data(self):
        pass
