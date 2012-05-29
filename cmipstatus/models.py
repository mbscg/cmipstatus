from django.db import models
from fabric.api import run, env, settings
from datetime import datetime

class Experiment(models.Model):
    name = models.CharField(max_length=15)

    def check_status(self, tupa_data):        
        if tupa_data:
            lines = tupa_data.split('\n')
            lines.pop(0)
            for line in lines:
                columns = line.split()
                if len(columns) > 0 and self.name in columns[1]:
                    return columns
        return None

    def __unicode__(self):
        return self.name


class TupaQuery(models.Model):
    name = models.CharField(max_length=5)
    query_result = models.CharField(max_length=10240)
    last_checked = models.DateTimeField()
    refresh_time = models.IntegerField()

    def get_data(self):
        #should refresh?
        if (datetime.now() - self.last_checked).seconds > self.refresh_time:
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
