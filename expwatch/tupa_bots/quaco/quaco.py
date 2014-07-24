import sqlite3
import os
import stat
import glob
from datetime import datetime
import threading, time
import quaco_db

from tests import loading, filesize, minvalue, stdzero, zerovalue
from tests.errorcodes import LOADERR

from quaco_settings import DB_NAME, DIR_STRUCTURES, EXCLUSION_LIST, dump_file

permissions = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP |\
              stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH

NAME_COL = 0
ERR_COL = 1
ACK_COL = 2
N_WORKERS = 15


def inspect_files(filelist, name):
    con = quaco_db.connect()
    dump_file = open('dump{0}'.format(name), 'w')
    for filename in filelist:
        if not filename: # may be None
            continue
        arq = quaco_db.get(con, filename)
        check = False
        if arq:
            #checked
            if arq.ack == 2:
                #recheck needed
                check = True
        else:
            #never checked
            check = True

        if check:
            err = run_tests(filename)
            info = ','.join([filename, str(err)])
            # dumping to file
            dump_file.write(info + '\n')
    dump_file.close()
    print "finished files w{0}".format(name)


def confirm_files(name):
    con = quaco_db.connect()
    dump_file = open('dump{0}'.format(name), 'r')
    sqls = dump_file.readlines()
    dump_file.close()
    for sql in sqls:
        values = sql.split(',')
        if len(values) == 2:
            info = {'name':values[0], 'error':int(values[1])}
            quaco_db.include(con, info)
    con.commit()


class AsyncVerifier(threading.Thread):
    def __init__(self, chunk):
        threading.Thread.__init__(self)
        # chunk is (index, data_list)
        self.file_list = chunk[1]
        self.name = chunk[0]
        print "starting worker {0}".format(self.name)

    def run(self):
        #do the work
        inspect_files(self.file_list, self.name)

    def confirm(self):
        confirm_files(self.name)


def do_chunk(inp, size):
    return map(None, *([iter(inp)] * size))


def capataz(file_list):
    chunks = do_chunk(file_list, len(file_list)/N_WORKERS)
    verifiers = [AsyncVerifier(chunk) for chunk in enumerate(chunks)]
    [v.start() for v in verifiers]
    [v.join() for v in verifiers]
    # sync'ly commit the changes
    [v.confirm() for v in verifiers]
    
    

def run_tests(filename):
    total_errors = 0
    load_result, data = loading.run(filename)
    if load_result == LOADERR:
        # won't go ahead
        return load_result
    total_errors += filesize.run(filename)
    total_errors += minvalue.run(data)
    total_errors += stdzero.run(data, filename)
    #total_errors += zerovalue.run(data)
    return total_errors


def cmip_crawler(var='*', decades=['1960', '1980', '2005'], rip='*'):
    print "working on", decades, "and rips", rip
    for decada in decades:
        cmip_exp = DIR_STRUCTURES['cmip_root'].format(decada)
        print "verifying", cmip_exp
        files = glob.glob(os.path.join(cmip_exp, DIR_STRUCTURES['cmip_files'].format(rip, var)))
        print "total {0} files".format(len(files))
        capataz(files)

"""
ack STATUS CODES
0 checked, stored
1 dumped
2 recheck ready
"""        

import sys
# quaco.py var decada rip

if __name__ == "__main__":
    print "running inspector"
    if len(sys.argv) == 1:
        cmip_crawler()
    elif len(sys.argv) == 2:
        cmip_crawler(var=sys.argv[1])
    elif len(sys.argv) == 3:
        cmip_crawler(var=sys.argv[1], decades=[sys.argv[2]])
    elif len(sys.argv) == 4:
        cmip_crawler(var=sys.argv[1], decades=[sys.argv[2]], rip=sys.argv[3])
