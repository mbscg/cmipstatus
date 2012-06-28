from django.db import models
from datetime import datetime
from os.path import join
from django.contrib.auth.models import User
import settings
import requests

class People(User):
    name = models.CharField(max_length=100)
    about = models.TextField(default='INPE GMAO Researcher')
    photo = models.ImageField(max_length=1048, upload_to='media', default='profile_default.png')

    def __unicode__(self):
        return self.name


class Experiment(models.Model):
    name = models.CharField(max_length=15)

    def get_status(self, tupa_data):
        done, total, errors, last_ok = check_restart_list(self.name, '')
        current = check_status(self.name, '', tupa_data)
        return done, total, errors, last_ok, current

    def __unicode__(self):
        return self.name


class Member(models.Model):
    name = models.CharField(max_length=3)
    exp = models.ForeignKey('Experiment')

    def get_status(self,tupa_data):
        done, total, errors, last_ok = check_restart_list(self.exp.name, self.name)
        current = check_status(self.exp.name, self.name, tupa_data)
        return done, total, errors, last_ok, current

    def __unicode__(self):
        return self.name


def check_restart_list(exp_name, member_name):
    print "getting restart list"
    RESTART_FILE = open(settings.server_configs['restartlist_template'].format(exp_name + member_name), 'r')
    restart_list = RESTART_FILE.readlines()
    restarts = 0
    done = 0
    error = 0
    last_ok = True
    for line in restart_list:
        restarts += 1
        if 'END' in line:
            done += 1
            last_ok = True
        elif 'ERR' in line:
            error += 1
            last_ok = False
            restarts -= 1
        elif 'ABO' in line:
            last_ok = False
            error += 1
            error *= -1
    return done, restarts, error, last_ok


def check_status(exp_name, member_name, tupa_data):
    if tupa_data:
        lines = tupa_data.split('\n')
        lines.pop(0)
        for line in lines:
            columns = line.split()
            if len(columns) > 2 and columns[1].endswith(exp_name+member_name):
                return columns
    return [None, 'M_'+exp_name+member_name, None, None, '0%']


def get_tupa_data():
    QSTAT_FILE = open(settings.server_configs['qstat_log'])
    tupa_data = QSTAT_FILE.read()
    QSTAT_FILE.close()
    return tupa_data
