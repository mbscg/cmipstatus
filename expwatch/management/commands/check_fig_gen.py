from django.core.management.base import BaseCommand, CommandError
from cmipsite.expwatch.models import MemberConfig
import json
from datetime import datetime
from check_gen_config import ORIGIN_PREFIX


class Command(BaseCommand):
    help = 'check members current year and compare to configs'

    def handle(self, *args, **kwargs):
        for config in MemberConfig.objects.all():
            self.stdout.write("CONFIG" + str(config) + '\n')
            if config.check_need():
                req = config.create_requisition()
                req_filename = '_'.join([ORIGIN_PREFIX, req['exp'], req['member'], 'order.json'])
                req_file = open(req_filename, 'w')
                json.dump(req, req_file)
                req_file.close()

            


