from django.db import models
from datetime import datetime
from os.path import join
from django.contrib.auth.models import User
from django.contrib.syndication.views import Feed
import settings
import requests
import yaml
import os
import glob


REPORT_CHOICES = (
    ('UNK', 'Unknown'),
    ('RUN', 'Running'), 
    ('END', 'Finished'),
    ('ABO', 'Aborted'),
    ('ERR', 'Error'))

CONVERT_CHOICES = (
    ('UNK', 'Unknown'),
    ('RUN', 'Running'),
    ('END', 'Finished'),
    ('ERR', 'Error'))


class People(User):
    name = models.CharField(max_length=100, verbose_name="Nome")
    about = models.TextField(default='INPE GMAO Researcher', verbose_name="Sobre")
    photo = models.ImageField(max_length=1048, upload_to='media', 
        default='profile_default.png', verbose_name="Foto")

    def __unicode__(self):
        return self.name


class Experiment(models.Model):
    name = models.CharField(max_length=15)

    def get_status(self, tupa_data, forcing=False):
        done, total, errors, last_ok = check_restart_list(self.name, '')
        current = check_status(self.name, '', tupa_data)
        try:
            report = ExpReport.objects.get(exp=self)
        except:
            report = ExpReport(status='UNK', exp=self)
            report.save()

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

        if forcing:
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


    def get_validation_data(self, member=None):
        expname = self.name
        if member:
            is_member = True
            screen_name = expname + member
        else:
            is_member = False
            member = '_1'
            screen_name = expname

        FIGS_URL = settings.server_configs['imgs_info']['local_figs'].format(expname+member)
        FIGS_LOG = settings.server_configs['imgs_info']['local_logs'].format(expname+member)
        FIGS_LOG = os.path.join(settings.server_configs['site_root'], FIGS_LOG)
        if os.path.exists(FIGS_LOG):
            yaml_log = yaml.load(open(FIGS_LOG, 'r'))
        else:
            yaml_log = {'start_date':'unknown', 'end_date':'unknown'}

        imgs = []
        regions = settings.server_configs['imgs_info']['regions']
        types = settings.server_configs['imgs_info']['infotype']
        for typ in types:
            type_imgs = []
            for region in regions:
                gif = settings.server_configs['imgs_info']['figs_file']
                gif = gif.format(region, typ, expname, yaml_log['start_date'],
                                 yaml_log['end_date'])
                type_imgs.append(os.path.join(FIGS_URL, gif))
            imgs.append([typ, type_imgs])
    
    
        media_figs_dir = settings.server_configs['imgs_info']['local_new_figs'].format(expname)
        new_figs_dir = os.path.join(settings.server_configs['site_root'], media_figs_dir)
        if is_member:
            candidate = glob.glob(os.path.join(new_figs_dir, '*'+member))
            if candidate:
                new_figs_dir = candidate[0]
                media_figs_dir = os.path.join(media_figs_dir, os.path.split(new_figs_dir)[1])
        has_new_figs = os.path.exists(new_figs_dir) and [f for f in os.listdir(new_figs_dir) if '.jpg' in f]
        ensemble_figs = []
    
        if has_new_figs:
            figs = os.listdir(new_figs_dir)
            figs = [os.path.join('/', media_figs_dir, f) for f in figs if '.jpg' in f]
            figs.sort()
            for variable in settings.server_configs['imgs_info']['ensembled']['variables']:
                var_figs = []
                for fig in figs:
                    if '_'+variable+'_' in fig or '_'+variable+'.' in fig:
                        var_figs.append(fig)
            scalar_figs = []
            for scalar in settings.server_configs['imgs_info']['ensembled']['scalars']:
                for fig in figs:
                    if scalar in fig:
                        scalar_figs.append(fig)
            ensemble_figs.append(['other', scalar_figs])
            imgs = ensemble_figs

        return imgs, screen_name, yaml_log



    def __unicode__(self):
        return self.name


class Member(models.Model):
    name = models.CharField(max_length=3)
    exp = models.ForeignKey('Experiment')

    def get_status(self,tupa_data, forcing=False):
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
        
        if forcing:
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


class ConvReport(models.Model):
    status = models.CharField(max_length=3, choices=CONVERT_CHOICES)
    member = models.CharField(max_length=64)


class ReportChangeLog(models.Model):
    message = models.CharField(max_length=512)
    when = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        text = '{0}\n(on {1})'.format(self.message, self.when)
        return text

    def get_absolute_url(self):
        return 'http://antares.ccst.inpe.br/cmip/log/' + str(self.id)


class FeedFetcher(Feed):
    title = "CMIP5 Status Site News"
    link = "http://antares.ccst.inpe.br/cmip/news/"
    description = "Latest changes in exp status"

    def items(self):
        return ReportChangeLog.objects.order_by('-when')[:50]

    def item_title(self, item):
        return item.message

    def item_description(self, item):
        return item



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
