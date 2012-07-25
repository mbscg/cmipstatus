from django.shortcuts import render_to_response
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
def newsview(request):
    logs = ReportChangeLog.objects.order_by('-when')
    user = request.user
    return render_to_response('cmipnews.html', {'logs':logs, 'user':user})



@login_required
def expvalview(request, expname):
    user = request.user
    is_member = False
    if '_' not in expname:
        pure_expname = expname 
        expname += '_1'
    else:
        pure_expname = expname.split('_')[0]
        member = expname.split('_')[1]
        is_member = True
    FIGS_URL = settings.server_configs['imgs_info']['local_figs'].format(expname)
    FIGS_LOG = settings.server_configs['imgs_info']['local_logs'].format(expname)
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
            gif = gif.format(region, typ, pure_expname, yaml_log['start_date'],
                             yaml_log['end_date'])
            type_imgs.append(os.path.join(FIGS_URL, gif))
        imgs.append([typ, type_imgs])


    media_figs_dir = settings.server_configs['imgs_info']['local_new_figs'].format(pure_expname)
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
            ensemble_figs.append([variable, var_figs])
        scalar_figs = []
        for scalar in settings.server_configs['imgs_info']['ensembled']['scalars']:
            for fig in figs:
                if scalar in fig:
                    scalar_figs.append(fig)
        ensemble_figs.append(['other scalar stats', scalar_figs])
        
        
    return render_to_response("cmipexpvalview.html", 
                             {'imgs':imgs, 'expname':expname, 'log':yaml_log,
                              'ensemble_figs': ensemble_figs, 'has_figs':has_new_figs,
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
    info = []
    conversion_log.sort()

    for line in conversion_log:
        split_line = line.split()
        decade = split_line[0]
        try:
            report = ConvReport.objects.get(member=decade)
        except:
            report = ConvReport(member=decade, status='UNK')
        status = 'UNK'
        if len(split_line) < 4: # ERROR LINE
            info.append({'decade':decade, 'error':True})
            status = 'ERR'
        else:
            current = float(split_line[1])
            expected = float(split_line[2])
            count_error = (current > expected)
            progress = float(current) / float(expected)
            text_progress = '%3.2f' % (100 * progress) + '%'
            info.append({'decade':decade, 'current':int(current), 'expected':int(expected),
                        'progress':progress, 'text_progress':text_progress,
                        'finished':(current == expected), 'error':False,
                        'count_error':count_error})
            if current == expected:
                status = 'END'
            else:
                status = 'RUN'
        if forcing:
            if report and not report.status == status:
                old_status = report.status
                report.status = status
                report.save()
                message = 'Decade {0} changed from {1} to {2}'.format(decade, old_status, status)
                new_log = ReportChangeLog(message=message)
                new_log.save()
    return info
