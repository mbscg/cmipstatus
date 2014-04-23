import sqlite3
import os
import stat
import glob
from datetime import datetime
import time
import quaco_db

from tests import loading, filesize, minvalue, zerovalue
from tests.errorcodes import LOADERR

from quaco_settings import DB_NAME, DIR_STRUCTURES

permissions = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP |\
              stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH

NAME_COL = 0
ERR_COL = 1
ACK_COL = 2
N_WORKERS = int(os.getenv('quaco_npes'))


def check_list(filelist):
    # shrink the list to the files it really needs to check
    con = quaco_db.connect()
    new_list = []
    for filename in filelist:
        if not filename: # may be None
            continue
        arq = quaco_db.get(con, filename)
        #print "checking", arq
        if arq:
            #checked
            if arq.ack == 2:
                #recheck needed
                #print "marked to recheck"
                new_list.append(filename)
            else:
                #print "no need to check"
                pass
        else:
            #never checked
            #print "never checked"
            new_list.append(filename)
    con.close()
    return new_list


def inspect_files(filelist, name, dump):
    print "inspecting from w", name
    print "actual size of list", len(filelist)
    dump_list = [','.join([filename, str(run_tests(filename)) + '\n' ]) for filename in filelist]
    print "dumping"
    dump.writelines(dump_list)


def confirm_files():
    con = quaco_db.connect()
    dump_files = glob.glob('dumps/dump*')
    for d in dump_files:
        #print "confirming", d
        dump_file = open(d, 'r')
        sqls = dump_file.readlines()
        dump_file.close()
        for sql in sqls:
            values = sql.split(',')
            if len(values) == 2:
                info = {'name':values[0], 'error':int(values[1])}
                quaco_db.include(con, info)
        con.commit()
    con.close()


def gen_report():
    con = quaco_db.connect()
    msgs = quaco_db.gen_report(con)
    con.commit()
    con.close()
    report = open('dumps/report', 'a')
    for m in msgs:
        report.write(','.join(m))
        report.write('\n')
    report.close()
    os.chmod('dumps/report', permissions)


class Verifier():
    def __init__(self, id, chunk):
        # chunk is (index, data_list)
        self.id = id
        self.file_list = chunk
        self.dump_file = open('dumps/dump{0}'.format(self.id), 'w')
        print "starting worker", self.id

    def run(self):
        #check its list
        self.file_list = check_list(self.file_list)
        #do the work
        inspect_files(self.file_list, self.id, self.dump_file)
        self.dump_file.close()


def do_chunk(inp, size):
    return map(None, *([iter(inp)] * size))


def capataz(id, file_list):
    print "file list size", len(file_list)
    chunks = do_chunk(sorted(file_list), len(file_list)/N_WORKERS)
    process_chunk = chunks[id-1]
    print "worker", id, "working with", len(process_chunk), "files"
    verifier = Verifier(id, process_chunk)
    verifier.run()
 

def run_tests(filename):
    total_errors = 0
    var_name = os.path.basename(filename).split('_')[0]

    # loading and filesize need filepath
    load_result, data = loading.run(filename)
    if load_result == LOADERR:
        # won't go ahead
        return load_result
    total_errors += filesize.run(filename)

    # from now on, tests work on variables
    total_errors += minvalue.run(data, var_name)
    total_errors += zerovalue.run(data, var_name)
    return total_errors


def cmip_crawler(id, decades=['1960', '1980', '2005'], rip='*'):
    print "verifying decades", decades, "rip", rip
    for decada in decades:
        cmip_exp = DIR_STRUCTURES['cmip_root'].format(decada)
        files = glob.glob(os.path.join(cmip_exp, DIR_STRUCTURES['cmip_files'].format(rip)))
        capataz(id, files)

"""
ack STATUS CODES
0 checked, stored
1 dumped
2 recheck ready
"""        

import sys
# quaco.py worker_number decada rip

if __name__ == "__main__":
    id = int(sys.argv[1])
    print "starting worker", id
    if id == -1:
        print "confirming dumps"
        confirm_files()
        gen_report()
    elif len(sys.argv) == 2:
        cmip_crawler(id)
    elif len(sys.argv) == 3:
        cmip_crawler(id, decades=[sys.argv[2]])
    elif len(sys.argv) == 4:
        cmip_crawler(id, decades=[sys.argv[2]], rip=sys.argv[3])
