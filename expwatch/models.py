from django.db import models
import officeboy

RESTART_LIST_DEFAULT = ' '


class Exp(models.Model):
    name = models.CharField(max_length=15)
    members = models.IntegerField(default=1)

    def parse_exp_info(self):
        tupa_data = officeboy.get_tupa_data()
        members = ExpMember.objects.filter(exp=self)
        meta_info = {'exp': self}
        run_info = []
        page_errors = 0

        for member in members:
            member_info = member.parse_member_status(tupa_data)
            page_errors += member_info['total_errors']
            run_info.append(member_info)

        meta_info['title'] = self.name
        meta_info['page_errors'] = page_errors
        meta_info['run_info'] = run_info

        return meta_info


    def parse_exp_overview(self):
        info = self.parse_exp_info()
        error, aborted, finished, running = 0, 0, 0, 0
        status = 'RUN_OK'
        for member in info['run_info']:
            if member['complete']:
                if member['aborted']:
                    aborted += 1
                else:
                    finished += 1
            else:
                if member['error']:
                    error += 1
                else:
                    running += 1

        if running > 0:
            if aborted > 0:
                status = 'RUN_ABO'
            elif error > 0:
                status = 'RUN_ERR'
            else:
                status = 'RUN_OK'
        elif running == 0:
            if aborted > 0:
                status = 'END_ABO'
            else:
                status = 'END_OK'

        return status, error, aborted


    def parse_exp_readme(self):
        readme = officeboy.get_readme()
        relevant = []
        state = 'ignore'
        for line in readme:
            l = line.decode('latin-1')
            if self.name in l:
                state = 'accept'
            if state == 'accept':
                relevant.append(l)
                if 'diretorio: ' in l:
                    state = 'ignore'
        return relevant


    def __unicode__(self):
        return 'Exp {0}, with {1} members'.format(self.name, str(self.members))




class ExpMember(models.Model):
    exp = models.ForeignKey('Exp')
    member = models.IntegerField(default=0)
    restart_list = models.CharField(max_length=1024, default=RESTART_LIST_DEFAULT)
    description = models.TextField(max_length=1024, default=' ')

    def get_fancy_name(self):
        if self.exp.members == 1:
            return self.exp.name
        return '{0}_{1}'.format(self.exp.name, str(self.member))

    def parse_member_status(self, tupa_data):
        done, total, errors, last_ok, last_complete_year = self.check_restart_list()
        current = self.check_status()

        finished_prog = float(done) / float(total)
        finished_years = done / 12.0
        total_years = total/12
        run_fraction = 1. / total
        member_info = {'member':current[1].split('_', 1)[-1], 'id':self.id,
                       'last':done, 'current':done, 'total':total,
                       'last_complete_year': last_complete_year,
                       'errors': (errors != 0), 'aborted': (errors < 0)}

        if member_info['aborted']:
            errors *= -1
        member_info['total_errors'] = errors
        member_info['error'] = not last_ok
        member_info['complete'] = (done == total) or member_info['aborted']
        member_info['running'] = (current[0] is not None)
        member_info['prog'] = finished_prog
        if member_info['running']:
            member_info['job_id'] = current[0]
            if 'aux' in member_info['job_id']:
                member_info['post'] = True
                member_info['text_run'] = 100
                member_info['prog'] += run_fraction
            else:
                member_info['post'] = False
                member_info['text_run'] = current[-1][:-1]
                member_info['prog'] += float(member_info['text_run'])/100.0 * run_fraction
        member_info['finished_years'] = '%3.2f' % (member_info['prog'] * total_years)
        member_info['total_years'] = total_years
        member_info['text_total'] = '%3.2f' % (member_info['prog'] * 100)

        return member_info
    
 
    def check_restart_list(self):
        fancy_name = self.get_fancy_name()
        restart_list = officeboy.get_restart_list(fancy_name)
        restarts, done, error = 0, 0, 0
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
        try:
            last_month = line.split()[2][:6]
            if last_month.endswith('12'):
                last_complete_year = last_month[:4]
            else:
                last_complete_year = str(int(last_month[:4]) - 1)
        except:
            last_complete_year = None
        return done, restarts, error, last_ok, last_complete_year


    def check_status(self):
        tupa_data = officeboy.get_tupa_data()
        tupa_data.pop(0)
        for line in tupa_data:
            columns = line.split()
            exp_name = self.exp.name
            member_name = str(self.member)
            if len(columns) > 2 and columns[1].endswith(self.get_fancy_name()):
                return columns
        return [None, 'M_'+self.get_fancy_name(), None, None, '0%']


    def get_config(self):
        try: 
            config = MemberConfig.objects.get(member=self)
        except:
            config = MemberConfig(member=self, variables='', interval=0, active=False)
            config.save()
        return config


    def __unicode__(self):
        return 'Member {0} from Exp {1}'.format(str(self.member), self.exp.name)


class Alert(models.Model):
    exp = models.ForeignKey('Exp')
    message = models.TextField(default='')
    when = models.DateTimeField(auto_now_add=True)
    dismissed = models.BooleanField(default=False)

    def __unicode__(self):
        return "alert for {0}".format(self.exp.name)


class MemberConfig(models.Model):
    member = models.ForeignKey('ExpMember')
    variables = models.TextField()
    interval = models.IntegerField()
    active = models.BooleanField()
    last_gen = models.IntegerField(default=-1)
    compare_to = models.TextField(default='')


    def __unicode__(self):
        return "orders for " + str(self.member)


    def check_need(self):
        member_info = self.member.parse_member_status(officeboy.get_tupa_data())
        finished = int(float(member_info['last_complete_year']))
        if self.active and finished:
            if self.last_gen == -1 or (finished - self.last_gen > self.interval):
                # need
                self.last_gen = finished
                self.save()
                return True
            else:
                # no need
                return False


    def create_requisition(self):
        req = {
            'final_year':'2010',
            'exp':self.member.exp.name, 
            'member':'%02d' % self.member.member,
            'variables': self.variables,
            'comp_to': self.compare_to,
        }
        return req
