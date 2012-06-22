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


@login_required
def home(request):
    return render_to_response("cmiphome.html", {})


@login_required
def explist(request):
    experiments = list(Experiment.objects.all())
    exps_errors, total_errors = experror_util()
    finished_exps = expfinished_util()
    [experiments.remove(exp) for exp in exps_errors]
    [experiments.remove(exp) for exp in finished_exps]
    return render_to_response("cmipexplist.html", {'exps': experiments, 'exps_errors': exps_errors, 'total_errors':total_errors,
                              'finished_exps':finished_exps, 'general_list':True})

@login_required
def peoplelist(request):
    people = People.objects.all()
    return render_to_response("cmipproflist.html", {'people': people})


@login_required
def expview(request, expname):
    info = expview_util(expname)
    return  render_to_response("cmipexpview.html", info)


def expview_util(expname):
    exp = Experiment.objects.get(name=expname)
    members = Member.objects.all().filter(exp=exp)
    exp = [exp]
    tupa_data = get_tupa_data()
    runinfo = []
    info = {'exp':exp}
    page_errors = 0

    if members:
        exp = members

    for member in exp:
        done, total, nerrors, last_ok, current = member.get_status(tupa_data)
        page_errors += nerrors
        finished_prog = float(done) / float(total)
        finished_years = float(done)/12
        total_years = total/12
        run_fraction = 1. / total
        error = not last_ok
        #if error:
        #    done *= -1
        minfo = {'member':current[1].split('_',1)[-1], 'last':done, 'current':done, 'total':total, 'error':error, 
                 'total_errors':nerrors}
        minfo['complete'] = (done == total)
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


FETCHED_LOGS_DIR = join(settings.server_configs['site_root'], 'cmipstatus', 'fetched_data', 'logs')

@login_required
def expvalview(request, expname):
    #load image classes
    classes_file = open(join(settings.server_configs['site_root'], 'cmipstatus', 'img_classes.yaml'))
    classes = yaml.load(classes_file)
    classes_file.close()

    #load images for exp
    if '_' not in expname:
        expname += '_1'
    FIGS_DIR = join(settings.MEDIA_ROOT, 'images', expname, 'figures')
    if not exists(FIGS_DIR):
        raise Http404
    try:
        logfile = open(join(FETCHED_LOGS_DIR, expname+'log.txt'), 'r')
        log = logfile.read()
        logfile.close()
    except:
        log = 'unknown'

    imgs = []
    for region in classes['regions']:
        region_imgs = []
        for uri in listdir(FIGS_DIR):
            if region in uri.split('_')[0]:
                complete_uri = join(settings.MEDIA_URL, 'images', expname, 'figures', uri)
                region_imgs.append(complete_uri)
        imgs.append([region, region_imgs])

    return render_to_response("cmipexpvalview.html", {'imgs':imgs, 'expname':expname, 'log':log})



def experror_util():
    all_experiments = Experiment.objects.all()
    exps_with_errors = []
    total_errors = 0
    for exp in all_experiments:
        exp_info = expview_util(exp.name)
        has_error = False
        for member_info in exp_info['minfo']:
            if member_info['error']:
                has_error = True
                total_errors += 1
        if has_error:
            exps_with_errors.append(exp)
    return exps_with_errors, total_errors


def expfinished_util():
    all_experiments = Experiment.objects.all()
    finished_exps = []
    for exp in all_experiments:
        exp_info = expview_util(exp.name)
        is_complete = True
        for member_info in exp_info['minfo']:
            if not member_info['complete']:
                is_complete = False
        if is_complete:
            finished_exps.append(exp)
    return finished_exps


@login_required
def profview(request, profid):
    prof = People.objects.get(id=profid)
    user_prof = People.objects.get(username=request.user)
    editable = prof == user_prof
    return render_to_response("cmipprofview.html", {'prof':prof, 'editable':editable})


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
                return render_to_response("cmipchangepassw.html", {'form':form, 'erro':True},
                context_instance=RequestContext(request))

    else:
        form = FormPassword()

    return render_to_response("cmipchangepassw.html", {'form':form},
                context_instance=RequestContext(request))
    
