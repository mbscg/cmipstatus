from django.db import models
from datetime import datetime
from os.path import join
from django.contrib.auth.models import User
from django.contrib.syndication.views import Feed
import settings
import requests

REPORT_CHOICES = (
    ('UNK', 'Unknown'),
    ('RUN', 'Running'), 
    ('END', 'Finished'),
    ('ABO', 'Aborted'),
    ('ERR', 'Error'))

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
        report = ExpReport.objects.get(exp=self)

        finished_prog = float(done) / float(total)
        finished_years = float(done)/12
        total_years = total/12
        run_fraction = 1. / total
        minfo = {'member':current[1].split('_',1)[-1], 'last':done,
                 'current':done, 'total':total, 'errors': not(errors == 0)}
        minfo['aborted'] = (errors < 0)
        if minfo['aborted']:
            errors *= -1
        minfo['total_errors'] = errors
        minfo['error'] = not last_ok
        minfo['complete'] = (done == total) or minfo['aborted']
        minfo['running'] = (current[0] is not None)
        minfo['prog'] = finished_prog
        if minfo['running']:
            minfo['job_id'] = current[0]
            if 'aux' in minfo['job_id']:
                minfo['post'] = True
                minfo['text_run'] = 100
                minfo['prog'] += run_fraction
            else:
                minfo['post'] = False
                minfo['text_run'] = current[-1][:-1]
                minfo['prog'] += float(minfo['text_run'])/100.0 * run_fraction
        minfo['finished_years'] = '%3.2f' % (minfo['prog'] * total_years)
        minfo['total_years'] = total_years
        minfo['text_total'] = "%3.2f" % (minfo['prog']*100)

        new_status = None
        if minfo['complete']:
            new_status = 'END'
        elif minfo['error']:
            new_status = 'ERR'
        elif minfo['aborted']:
            new_status = 'ABO'
        else: # minfo['running'] or waiting
            new_status = 'RUN'
        if new_status and not new_status == report.status:
            message = '{0} has changed from {1} to {2}'.format(self.name, report.status, new_status)
            report.status = new_status
            report.save()
            change_log = ReportChangeLog(message=message)
            change_log.save()
        return minfo

    def __unicode__(self):
        return self.name


class Member(models.Model):
    name = models.CharField(max_length=3)
    exp = models.ForeignKey('Experiment')

    def get_status(self,tupa_data):
        done, total, errors, last_ok = check_restart_list(self.exp.name, self.name)
        current = check_status(self.exp.name, self.name, tupa_data)
        report = MemberReport.objects.get(member=self)
        
        finished_prog = float(done) / float(total)
        finished_years = float(done)/12
        total_years = total/12
        run_fraction = 1. / total
        minfo = {'member':current[1].split('_',1)[-1], 'last':done,
                 'current':done, 'total':total, 'errors': not(errors == 0)}
        minfo['aborted'] = (errors < 0)
        if minfo['aborted']:
            errors *= -1
        minfo['total_errors'] = errors
        minfo['error'] = not last_ok
        minfo['complete'] = (done == total) or minfo['aborted']
        minfo['running'] = (current[0] is not None)
        minfo['prog'] = finished_prog
        if minfo['running']:
            minfo['job_id'] = current[0]
            if 'aux' in minfo['job_id']:
                minfo['post'] = True
                minfo['text_run'] = 100
                minfo['prog'] += run_fraction
            else:
                minfo['post'] = False
                minfo['text_run'] = current[-1][:-1]
                minfo['prog'] += float(minfo['text_run'])/100.0 * run_fraction
        minfo['finished_years'] = '%3.2f' % (minfo['prog'] * total_years)
        minfo['total_years'] = total_years
        minfo['text_total'] = "%3.2f" % (minfo['prog']*100)
        minfo['report'] = report.status
        
        new_status = None
        if minfo['complete']:
            new_status = 'END'
        elif minfo['error']:
            new_status = 'ERR'
        elif minfo['aborted']:
            new_status = 'ABO'
        else: # minfo['running'] or waiting
            new_status = 'RUN'
        if new_status and not new_status == report.status:
            message = '{0} member {1} has changed from {2} to {3}'.format(self.exp.name, self.name, report.status, new_status)
            report.status = new_status
            report.save()
            change_log = ReportChangeLog(message=message)
            change_log.save()
        return minfo

    def __unicode__(self):
        return self.name


class Comment(models.Model):
    exp = models.ForeignKey('Experiment')
    author = models.ForeignKey('People')
    text = models.TextField(max_length=2048, default='')


class ExpReport(models.Model):
    status = models.CharField(max_length=3, choices=REPORT_CHOICES)
    exp = models.ForeignKey('Experiment')


class MemberReport(models.Model):
    status = models.CharField(max_length=3, choices=REPORT_CHOICES)
    member = models.ForeignKey('Member')


class ReportChangeLog(models.Model):
    message = models.CharField(max_length=512)
    when = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        text = '{0}\n(on {1})'.format(self.message, self.when)
        return text

    def get_absolute_url(self):
        return 'http://antares.ccst.inpe.br/cmip/list'


class FeedFetcher(Feed):
    title = "CMIP5 Status Site News"
    link = "/news/"
    description = "Latest changes in exp status"

    def items(self):
        return ReportChangeLog.objects.order_by('-when')[:100]

    def item_title(self, item):
        return item.message

    def item_description(self, item):
        return ' '.join(item.message, '\n', item.when)



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
