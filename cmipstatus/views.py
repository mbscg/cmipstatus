from django.shortcuts import render_to_response
from models import Experiment, TupaQuery

def home(request):
    return render_to_response("cmiphome.html", {})


def explist(request):
    experiments = Experiment.objects.all()
    return render_to_response("cmipexplist.html", {'exps': experiments})


def expview(request, expname):
    exp = Experiment.objects.get(name=expname)
    tupa_data = TupaQuery.objects.get(name='query').get_data()
    runinfo = exp.check_status(tupa_data)
    info = {'exp':exp}
    if runinfo:
        info['job_id'] = runinfo[0]
        if 'aux' in info['job_id']:
            info['status'] = "Post-processing"
        else:
            info['status'] = runinfo[-1]
    return  render_to_response("cmipexpview.html", info)
