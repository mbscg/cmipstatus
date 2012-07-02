from django.shortcuts import render_to_response
from models import Experiment, Member, People, get_tupa_data
from forms import FormEditProfile, FormPassword
from django.template import RequestContext
from os.path import join, exists
from os import listdir
import settings
from django.http import Http404
from django.contrib.auth.decorators import login_required
import yaml
import requests


@login_required
def home(request):
    return render_to_response("cmiphome.html", {})

@login_required
def explist(request):
    running_exps = list(Experiment.objects.all())
    tupa_data = get_tupa_data()
    exps_errors, total_errors = experror_util(tupa_data)
    finish_exps, finish_ab_exps, total_aborted = expfinished_util(tupa_data)
    [running_exps.remove(exp) for exp in exps_errors] 
    [running_exps.remove(exp) for exp in finish_exps]
    [running_exps.remove(exp) for exp in finish_ab_exps]
    return render_to_response("cmipexplist.html", 
                              {'exps':running_exps, 'exps_errors': exps_errors,
                              'total_errors':total_errors,
                              'finished_exps':finish_exps,
                              'finished_aborted_exps': finish_ab_exps, 
                              'total_aborted':total_aborted,
                              'general_list':True})

@login_required
def peoplelist(request):
    people = People.objects.all()
    return render_to_response("cmipproflist.html", {'people': people})


@login_required
def expview(request, expname):
    info = expview_util(expname, get_tupa_data())
    return  render_to_response("cmipexpview.html", info)


def expview_util(expname, tupa_data):
    exp = Experiment.objects.get(name=expname)
    members = Member.objects.all().filter(exp=exp)
    exp = [exp]
    runinfo = []
    info = {'exp':exp}
    page_errors = 0

    if members:
        exp = members

    for member in exp:
        done, total, nerrors, last_ok, current = member.get_status(tupa_data)
        finished_prog = float(done) / float(total)
        finished_years = float(done)/12
        total_years = total/12
        run_fraction = 1. / total
        minfo = {'member':current[1].split('_',1)[-1], 'last':done, 
                 'current':done, 'total':total, 'errors': not(nerrors == 0)}
        minfo['aborted'] = (nerrors < 0)
        if minfo['aborted']:
            nerrors *= -1
        page_errors += nerrors
        minfo['total_errors'] = nerrors
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
        runinfo.append(minfo)
    info['title'] = expname
    info['page_errors'] = page_errors
    info['minfo'] = runinfo
    return info


@login_required
def expvalview(request, expname):
    pure_expname = expname
    if '_' not in expname:
        expname += '_1'
    else:
        pure_expname = pure_expname.split('_')[0]
    FIGS_URL = settings.server_configs['imgs_info']['figs_url'].format(expname)
    FIGS_LOG = settings.server_configs['imgs_info']['figs_log'].format(expname)
    request_info = requests.get(FIGS_LOG)
    if request_info.status_code == 200:
        yaml_log = yaml.load(request_info.text)
        use_backup_imgs = False
    else:
        yaml_log = {'start_date':'unknown', 'end_date':'unknown'}
        use_backup_imgs = True

    imgs = []
    regions = settings.server_configs['imgs_info']['regions']
    types = settings.server_configs['imgs_info']['infotype']
    for typ in types:
        type_imgs = []
        for region in regions:
            gif = settings.server_configs['imgs_info']['figs_file']
            gif = gif.format(region, typ, pure_expname, yaml_log['start_date'],
                             yaml_log['end_date'])
            type_imgs.append(FIGS_URL + gif)
        imgs.append([typ, type_imgs])

    return render_to_response("cmipexpvalview.html", 
                             {'imgs':imgs, 'expname':expname, 'log':yaml_log})



def experror_util(tupa_data):
    all_experiments = Experiment.objects.all()
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


def expfinished_util(tupa_data):
    all_experiments = Experiment.objects.all()
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
def profview(request, profid):
    prof = People.objects.get(id=profid)
    user_prof = People.objects.get(username=request.user)
    editable = prof == user_prof
    return render_to_response("cmipprofview.html", 
                              {'prof':prof, 'editable':editable})


@login_required
def profedit(request):
    profile = People.objects.get(username=request.user)

    if request.method == 'POST':
        form = FormEditProfile(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return render_to_response("cmipsuccess.html", {})
    else:
        form = FormEditProfile(instance=profile)

    return render_to_response("cmipprofedit.html", {'form':form},
                context_instance=RequestContext(request))


@login_required
def passwedit(request):
    if request.method == 'POST':
        profile = People.objects.get(username=request.user)
        form = FormPassword(request.POST, request.FILES)
        if form.is_valid():
            curr_passw = form.cleaned_data['current_passw']
            if request.user.check_password(curr_passw):
                new_passw = form.cleaned_data['new_passw']
                request.user.set_password(new_passw)
                request.user.save()
                return render_to_response("cmipsuccess.html", {})
            else:
                context = RequestContext(request)
                return render_to_response("cmipchangepassw.html", 
                                          {'form':form, 'erro':True},
                                          context_instance=context)

    else:
        form = FormPassword()

    context = RequestContext(request)
    return render_to_response("cmipchangepassw.html", {'form':form},
                              context_instance=context)
    
