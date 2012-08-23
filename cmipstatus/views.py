from django.shortcuts import render_to_response, get_object_or_404
from models import Experiment, Member, People, Comment, ReportChangeLog, get_tupa_data
from models import ConvReport
from forms import FormComment
from django.template import RequestContext
from os.path import join, exists
import os
import settings
from django.http import Http404
from django.contrib.auth.decorators import login_required
import yaml
import requests
import glob


#STATUS
RUNNING_WITH_ABORTED = 0
RUNNING_WITH_ERRORS = 1
RUNNING_OK = 2
FINISHED_WITH_ABORTED = 3
FINISHED_OK = 4

def home(request):
    user = request.user
    return render_to_response("cmiphome.html", {'user':user})


def forcefeed():
    # to be called via django cron
    all_exps = list(Experiment.objects.order_by('name'))
    tupa_data = get_tupa_data()
    for exp in all_exps:
        expview_util(exp.name, tupa_data, forcing=True)
    outputs_util(forcing=True)


@login_required
def explist(request):
    user = request.user
    all_exps = list(Experiment.objects.order_by('name'))
    tupa_data = get_tupa_data()
    classified = {RUNNING_WITH_ABORTED:[], RUNNING_WITH_ERRORS:[], RUNNING_OK:[],
                  FINISHED_WITH_ABORTED:[], FINISHED_OK:[]}
    total_aborted = 0
    total_error = 0
    for exp in all_exps:
        status, error, aborted = expstatus_util(tupa_data, exp.name)
        info = expview_util(exp.name, tupa_data)
        total_aborted += aborted
        total_error += error
        classified[status].append([exp, info])

    return render_to_response("cmipexplist.html",
                              {'running':classified[RUNNING_OK],
                               'running_errors':classified[RUNNING_WITH_ERRORS],
                               'running_aborted':classified[RUNNING_WITH_ABORTED],
                               'finished':classified[FINISHED_OK],
                               'finished_aborted':classified[FINISHED_WITH_ABORTED],
                               'total_errors':total_error,
                               'total_aborted':total_aborted,
                               'user':user})

@login_required
def peoplelist(request):
    people = People.objects.order_by('name')
    user = request.user
    return render_to_response("cmipproflist.html", {'people': people, 'user':user})


@login_required
def expview(request, expname):
    suser = request.user
    info = expview_util(expname, get_tupa_data())
    user = People.objects.get(username=request.user)
    exp = Experiment.objects.get(name=expname)
    info['comments'] = Comment.objects.all().filter(exp=exp)

    if request.method == 'POST':
        form = FormComment(request.POST, request.FILES)
        if form.is_valid():
            text = form.cleaned_data['comment']
            new_comment = Comment(author=user, exp=exp, text=text)
            new_comment.save()
            form = FormComment()
            info['form'] = form
    else:
        form = FormComment()
        info['form'] = form

    info['logged'] = (user is not None)
    info['user'] = suser
    context = RequestContext(request)
    return  render_to_response("cmipexpview.html", info, 
                               context_instance=context)


def expview_util(expname, tupa_data, forcing=False):
    exp = Experiment.objects.get(name=expname)
    members = Member.objects.all().filter(exp=exp) #no ordering!
    exp = [exp]
    runinfo = []
    info = {'exp':exp}
    page_errors = 0

    if members:
        exp = members

    if expname in settings.server_configs['CO2_info']['fixed']:
        info['co2'] = 'Fixed'
    elif expname in settings.server_configs['CO2_info']['increment']:
        info['co2'] = '1% incr.'
    elif expname in settings.server_configs['CO2_info']['mauna-loa']:
        info['co2'] = 'Mauna Loa'
    else:
        info['co2'] = 'No info'

    for member in exp:
        minfo = member.get_status(tupa_data, forcing=forcing)
        page_errors += minfo['total_errors']
        runinfo.append(minfo)
    info['title'] = expname
    info['page_errors'] = page_errors
    info['minfo'] = runinfo
    return info


@login_required
def newslist(request):
    logs = ReportChangeLog.objects.order_by('-when')
    user = request.user
    return render_to_response('cmipnews.html', {'logs':logs, 'user':user})



@login_required
def expvalview(request, expname, member):
    user = request.user
    exp = get_object_or_404(Experiment, name=expname)
    imgs, screen_name, log = exp.get_validation_data(member=member)
        
    return render_to_response("cmipexpvalview.html", 
                             {'imgs':imgs, 'expname':screen_name, 'log':log,
                              'user':user})



def expstatus_util(tupa_data, expname):
    exp_info = expview_util(expname, tupa_data)
    error_members = 0
    aborted_members = 0
    finished_members = 0
    running_members = 0
    status = RUNNING_OK
    for member in exp_info['minfo']:
        if member['complete']:
            if member['aborted']:
                aborted_members += 1
            else:
                finished_members += 1
        else:
            if member['error']:
                error_members += 1
            else:
                running_members += 1
    if running_members > 0:
        if aborted_members > 0:
            status = RUNNING_WITH_ABORTED
        elif error_members > 0:
            status = RUNNING_WITH_ERRORS
        else:
            status = RUNNING_OK
    elif running_members == 0:
        if aborted_members > 0:
            status = FINISHED_WITH_ABORTED
        else:
            status = FINISHED_OK
    return status, error_members, aborted_members


def experror_util(tupa_data):
    all_experiments = Experiment.objects.order_by('name')
    exps_with_errors = []
    total_errors = 0
    for exp in all_experiments:
        exp_info = expview_util(exp.name, tupa_data)
        has_error = False
        for member_info in exp_info['minfo']:
            if member_info['error'] and not member_info['aborted']:
                has_error = True
                total_errors += 1
        if has_error:
            exps_with_errors.append(exp)
    return exps_with_errors, total_errors


def expaborted_util(tupa_data):
    all_experiments = Experiment.objects.order_by('name')
    exps_with_aborted = []
    total_aborted = 0
    total_running = 0
    for exp in all_experiments:
        exp_info = expview_util(exp.name, tupa_data)
        still_running = True
        for member_info in exp_info['minfo']:
            if member_info['complete']:
                if member_info['aborted']:
                    total_aborted += 1
            else:
                total_running += 1
        if total_running > 0 and total_aborted > 0:
            exps_with_aborted.append(exp)
    return exps_with_aborted, total_aborted


def expfinished_util(tupa_data):
    all_experiments = Experiment.objects.order_by('name')
    finished_exps = []
    finished_aborted = []
    total_aborted = 0
    tupa_data = get_tupa_data()
    for exp in all_experiments:
        exp_info = expview_util(exp.name, tupa_data)
        is_complete = True
        any_aborted = False
        local_aborted = 0
        for member_info in exp_info['minfo']:
            if not member_info['complete']:
                is_complete = False
            if member_info['aborted']:
                any_aborted = True
                local_aborted += 1
        if is_complete:
            if not any_aborted:
                finished_exps.append(exp)
            else:
                finished_aborted.append(exp)
                total_aborted += local_aborted
    return finished_exps, finished_aborted, total_aborted


@login_required
def outputsview(request):
    info = outputs_util()
    user = request.user
    return render_to_response("cmipoutputs.html", {'info':info, 'user':user})


def outputs_util(forcing=False):
    conversion_log = open(settings.server_configs['conversion_log']).readlines()
    info = {}
    conversion_log.sort()

    for line in conversion_log:
        decade, cond, comp, current, expected, progress  = line.split()
        if not info.has_key(decade):
            info[decade] = {}
        if info.has_key(decade) and not info[decade].has_key(cond):
            info[decade][cond] = {}
        info[decade][cond][comp] = ['%3.2f' % (100 * float(progress)) + '%', float(progress)]

    #feeds for this will be rewritten later (maybe never)
       
    """
        if forcing:
            if report and not report.status == status:
                old_status = report.status
                report.status = status
                report.save()
                message = 'Decade {0} changed from {1} to {2}'.format(decade, old_status, status)
                new_log = ReportChangeLog(message=message)
                new_log.save()
    """
    return info
