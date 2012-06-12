from django.db import models
from fabric.api import run, env, settings, get
from datetime import datetime

RESTART_LIST_TEMPLATE = '/stornext/online2/ocean/simulations/{0}/experiment_design/RESTARTLIST.{1}.tmp'

class Experiment(models.Model):
    name = models.CharField(max_length=15)

    def get_status(self, tupa_data):
        done, total = check_restart_list(self.name, '')
        current = check_status(self.name, '', tupa_data)
        print "done, total", done, total
        return done, total, current

    '''
    def check_status(self, tupa_data):
        members = Member.objects.all().filter(exp=self)
        if not members: #no members, check itself
            #check for itself
            if tupa_data:
                lines = tupa_data.split('\n')
                lines.pop(0)
                for line in lines:
                    columns = line.split()
                    if len(columns) > 0 and columns[1].endswith(self.name):
                        return [columns]
        else:
            members_data = []
            for member in members:
                members_data.append(member.check_status(tupa_data))
                member.check_restart_list()
            return members_data
        return None #last case
    '''
    def __unicode__(self):
        return self.name


class Member(models.Model):
    name = models.CharField(max_length=2)
    exp = models.ForeignKey('Experiment')

    def get_status(self,tupa_data):
        done, total = check_restart_list(self.exp.name, self.name)
        current = check_status(self.exp.name, self.name, tupa_data)
        print "done, total", done, total
        return done, total, current

    def __unicode__(self):
        return self.name


def check_restart_list(exp_name, member_name):
    file_to_read = RESTART_LIST_TEMPLATE.format(exp_name, exp_name+member_name)
    with settings(host_string='ocean@tupa', warn_only=True):
        get(file_to_read, '.')
        print "getting..."
        restart_list = open("RESTARTLIST.{0}.tmp".format(exp_name+member_name), 'r')
        restarts = 0.
        done = 0.
        for line in restart_list:
            restarts += 1
            if 'END' in line:
                done += 1
        return done, restarts


def check_status(exp_name, member_name, tupa_data):
    print "searching", exp_name+member_name
    if tupa_data:
        lines = tupa_data.split('\n')
        lines.pop(0)
        for line in lines:
            columns = line.split()
            if len(columns) > 0 and columns[1].endswith(exp_name+member_name):
                print "found", columns
                return columns
    print "not found"
    return [None, exp_name+member_name, None, None, '0%']


class TupaQuery(models.Model):
    name = models.CharField(max_length=5)
    query_result = models.CharField(max_length=10240)
    last_checked = models.DateTimeField()
    refresh_time = models.IntegerField()

    def get_data(self):
        #should refresh?
        now = datetime.now()
        print "now - last, refresh", (now - self.last_checked).seconds, self.refresh_time
        if (now - self.last_checked).seconds > self.refresh_time:
            print "refreshing data"
            with settings(host_string='ocean@tupa', warn_only=True):
                results = run('stat_cpld manoel.baptista')
            if results.succeeded:
                self.query_result = results
                self.last_checked = datetime.now()
            else:
                print "Failed to refresh data"
            self.save()
        return self.query_result


