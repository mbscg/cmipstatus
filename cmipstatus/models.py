from django.db import models
from fabric.api import run, env, settings
from datetime import datetime

class Experiment(models.Model):
    name = models.CharField(max_length=15)

    def check_status(self, tupa_data):
        #check for itself
        if tupa_data:
            lines = tupa_data.split('\n')
            lines.pop(0)
            for line in lines:
                columns = line.split()
                if len(columns) > 0 and columns[1].endswith(self.name):
                    return [columns]
        #if not itself, check for member
        members = Member.objects.all().filter(exp=self)
        if not members: #no members, no go
            return None
        members_data = []
        for member in members:
            members_data.append(member.check_status(tupa_data))
        return members_data

    def __unicode__(self):
        return self.name


class Member(models.Model):
    name = models.CharField(max_length=2)
    exp = models.ForeignKey('Experiment')

    def check_status(self, tupa_data):
        print "searching", self.exp.name + self.name
        if tupa_data:
            lines = tupa_data.split('\n')
            lines.pop(0)
            for line in lines:
                columns = line.split()
                if len(columns) > 0 and columns[1].endswith(self.exp.name + self.name):
                    print "found", columns
                    return columns
        print "not found"
        return [None, self.exp.name+self.name, None, None, '0%']

    def __unicode__(self):
        return self.name


class TupaQuery(models.Model):
    name = models.CharField(max_length=5)
    query_result = models.CharField(max_length=10240)
    last_checked = models.DateTimeField()
    refresh_time = models.IntegerField()

    def get_data(self):
        #should refresh?
        now = datetime.now()
        print "now - last, refresh", (now - self.last_checked).seconds, self.refresh_time
        if (now - self.last_checked).seconds > self.refresh_time:
            print "refreshing data"
            with settings(host_string='ocean@tupa', warn_only=True):
                results = run('stat_cpld manoel.baptista')
            if results.succeeded:
                self.query_result = results
                self.last_checked = datetime.now()
            else:
                print "Failed to refresh data"
            self.save()
        return self.query_result
