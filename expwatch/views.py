from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator

from models import Exp, ExpMember, Alert
from forms import FormIncludeExp, FormExcludeExp
from officeboy import get_tupa_data

class Home(View):
    template_name = 'expshome.html'

    def get(self, request):
        user = request.user
        return render(request, self.template_name, {'user':user})


class ExpList(View):
    template_name = 'expslist.html'

    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        all_exps = Exp.objects.all().order_by('name')
        open_alerts = Alert.objects.filter(dismissed=False).order_by('when')
        classified = {'RUN_OK': [], 'RUN_ERR': [],
                      'RUN_ABO': [], 'END_OK': [],
                      'END_ABO': []}
        total_aborted, total_errors = 0, 0
        for exp in all_exps:
            try:
                status, error, aborted = exp.parse_exp_overview()
                info = exp.parse_exp_info()
                total_aborted += aborted
                total_errors += error
                classified[status].append([exp, info])
            except:
                #what to do if the exp doesn't exist?
                # ALERT! And this alert never ever goes away
                alert = Alert.objects.filter(exp=exp).filter(message='NOT FOUND').filter(dismissed=False)
                if not alert:
                    alert = Alert(exp=exp, message='NOT FOUND')
                    alert.save()
            

        return render(request, self.template_name, 
            {'user':user, 'alerts': open_alerts, 'classified':classified,
             'total_errors': total_errors, 'total_aborted': total_aborted})


class ExpView(View):
    template_name = 'expsview.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        user = request.user
        exp = get_object_or_404(Exp, id=kwargs['expid'])
        try:
            info = exp.parse_exp_info()
        except:
            info = {}
        try:
            readme = exp.parse_exp_readme()
        except:
            readme = {}
        return render(request, self.template_name,
            {'user':user,'exp':exp, 'info':info, 'readme':readme})


class IncludeNewExp(View):
    template_name = 'expsinclude.html'

    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        form = FormIncludeExp()
        return render(request, self.template_name, 
            {'user':user, 'form':form},
            context_instance=RequestContext(request))


    @method_decorator(login_required)
    def post(self, request):
        user = request.user
        form = FormIncludeExp(request.POST, request.FILES)
        if form.is_valid():
            exp = form.instance
            exp.save()
            for i in range(1,form.instance.members + 1):
                new_member = ExpMember(exp=exp, member=i)
                new_member.save()
            return render(request, 'expsok.html', {'user':user})
        return render(request, self.template_name, 
            {'user':user, 'form':form},
            context_instance=RequestContext(request))


class ExcludeExp(View):
    template_name = 'expsexclude.html'

    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        form = FormExcludeExp()
        return render(request, self.template_name, 
            {'user':user, 'form':form},
            context_instance=RequestContext(request))


    @method_decorator(login_required)
    def post(self, request):
        user = request.user
        form = FormExcludeExp(request.POST, request.FILES)
        if form.is_valid():
            exp = form.cleaned_data['exp']
            exp.delete()
            return render(request, 'expsok.html', {'user':user})
        return render(request, self.template_name, 
            {'user':user, 'form':form},
            context_instance=RequestContext(request))


class AlertView(View):
    template_name = 'expsalertview.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        user = request.user
        alert = get_object_or_404(Alert, id=kwargs['alertid'])
        return render(request, self.template_name,
            {'user':user, 'alert': alert})


class AlertDismiss(View):
    template_name = 'expsok.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        user = request.user
        alert = get_object_or_404(Alert, id=kwargs['alertid'])
        alert.dismissed = True
        alert.save()
        return render(request, self.template_name,
            {'user':user})

class MemberView(View):
    template_name = 'expsmemberview.html'

    @method_decorator(login_required)
    def get(self, request, *args,  **kwargs):
        user = request.user
        member = get_object_or_404(ExpMember, id=kwargs['memberid'])
        return render(request, self.template_name,
            {'member':member, 'user':user})
