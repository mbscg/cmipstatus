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
    members_info = exp.check_status(tupa_data)
    runinfo = []
    info = {'exp':exp}

    if members_info:
        for member_info in members_info:
            print "showing", member_info
            minfo = {'member':member_info[1].split('_')[-1]}
            if member_info[0] == None: #no job, no job_id
                 minfo['submitted'] = False
            else:
                minfo['submitted'] = True
                minfo['job_id'] = member_info[0]
                if 'aux' in minfo['job_id']:
                    minfo['post'] = True
                    minfo['status'] = 1.0
                else:   
                    minfo['post'] = False
                    print "status", member_info[-1][:-1]
                    minfo['status'] = float(member_info[-1][:-1])/100
            runinfo.append(minfo)
        info['minfo'] = runinfo
    else:
        info['minfo'] = None

    return  render_to_response("cmipexpview.html", info)
