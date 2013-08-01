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


    def __unicode__(self):
        return 'Exp {}, with {} members'.format(self.name, self.members)




class ExpMember(models.Model):
    exp = models.ForeignKey('Exp')
    member = models.IntegerField(default=0)
    restart_list = models.CharField(max_length=1024, default=RESTART_LIST_DEFAULT)
    description = models.TextField(max_length=1024, default=' ')

    def get_fancy_name(self):
        if self.exp.members == 1:
            return self.exp.name
        return '{}_{}'.format(self.exp.name, str(self.member))

    def parse_member_status(self, tupa_data):
        done, total, errors, last_ok = self.check_restart_list()
        current = self.check_status()

        finished_prog = float(done) / float(total)
        finished_years = done / 12.0
        total_years = total/12
        run_fraction = 1. / total
        member_info = {'member':current[1].split('_', 1)[-1], 'last':done,
                       'current':done, 'total':total, 'errors': (errors != 0),
                       'aborted': (errors < 0)}

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
        print "checking restart list for", self
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
        return done, restarts, error, last_ok


    def check_status(self):
        fancy_name = '{}_{}'.format
        tupa_data = officeboy.get_tupa_data()
        tupa_data.pop(0)
        for line in tupa_data:
            columns = line.split()
            exp_name = self.exp.name
            member_name = str(self.member)
            if len(columns) > 2 and columns[1].endswith(self.get_fancy_name()):
                return columns
        return [None, 'M_'+self.get_fancy_name(), None, None, '0%']


    def __unicode__(self):
        return 'Member {} from Exp {}'.format(self.member, self.exp.name)
