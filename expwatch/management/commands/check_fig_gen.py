from django.core.management.base import BaseCommand, CommandError
from cmipsite.expwatch.models import MemberConfig
import json
from datetime import datetime


class Command(BaseCommand):
    help = 'check members current year and compare to configs'

    def handle(self, *args, **kwargs):
        for config in MemberConfig.objects.all():
            self.stdout.write("CONFIG" + str(config) + '\n')
            if config.check_need():
                req = config.create_requisition()
                req_file = open(datetime.isoformat(datetime.now()), 'w')
                req_file.write(json.dumps(req))
                req_file.close()
                # TODO send to tupa


